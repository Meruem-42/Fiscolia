"""
Clustering de profils utilisateurs - 3 catégories
Colonnes attendues : état civil, quotient familial, situation spécifique, catégorie socio professionnelle
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# 1. LOAD DATASET
# ─────────────────────────────────────────────

CSV_PATH = "./dataset.csv"
N_CLUSTERS = 3
AUTOENCODER_EPOCHS = 100
BATCH_SIZE = 32
LATENT_DIM = 8

print("=" * 60)
print("  CLUSTERING (3 profiles)")
print("=" * 60)

df = pd.read_csv(CSV_PATH)
print(f"\n✅ Loaded Dataset : {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Columns : {list(df.columns)}\n")
print(df.head())

# ─────────────────────────────────────────────
# 2. Preparation
# ─────────────────────────────────────────────

print("\n── Preparation ──")

# Basic cleanup
df_clean = df.dropna().copy()
print(f"Entry after suppression of NaN : {len(df_clean)}")

# Encoding
encoders = {}
df_encoded = df_clean.copy()

for col in df_clean.columns:
    if df_clean[col].dtype == object or df_clean[col].dtype.name == "category":
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_clean[col].astype(str))
        encoders[col] = le
        print(f"  '{col}' : {len(le.classes_)} categories → {list(le.classes_[:5])}{'...' if len(le.classes_) > 5 else ''}")
    else:
        print(f"  '{col}' : numeric (min={df_clean[col].min():.1f}, max={df_clean[col].max():.1f})")

# Normalisation
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_encoded.values.astype(float))
print(f"\nNormalized data : shape {X_scaled.shape}")

# ─────────────────────────────────────────────
# 3. AUTOENCODEUR
# ─────────────────────────────────────────────

print("\n── Training of the autoencodeur ──")

INPUT_DIM = X_scaled.shape[1]

class Autoencoder(nn.Module):
    def __init__(self, input_dim, latent_dim):
        super().__init__()
        hidden = max(input_dim * 2, latent_dim * 4)
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.BatchNorm1d(hidden),
            nn.Linear(hidden, latent_dim * 2),
            nn.ReLU(),
            nn.Linear(latent_dim * 2, latent_dim),
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, latent_dim * 2),
            nn.ReLU(),
            nn.Linear(latent_dim * 2, hidden),
            nn.ReLU(),
            nn.BatchNorm1d(hidden),
            nn.Linear(hidden, input_dim),
        )

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z), z

X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
dataset   = TensorDataset(X_tensor)
loader    = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

model     = Autoencoder(INPUT_DIM, LATENT_DIM)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()

losses = []
for epoch in range(AUTOENCODER_EPOCHS):
    model.train()
    epoch_loss = 0
    for (batch,) in loader:
        optimizer.zero_grad()
        recon, _ = model(batch)
        loss = criterion(recon, batch)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    avg_loss = epoch_loss / len(loader)
    losses.append(avg_loss)
    if (epoch + 1) % 20 == 0:
        print(f"  Epoch {epoch+1:3d}/{AUTOENCODER_EPOCHS} – Loss: {avg_loss:.5f}")

# Extraction of latent features
model.eval()
with torch.no_grad():
    _, Z = model(X_tensor)
Z_np = Z.numpy()
print(f"\n✅ Extracted latent features : shape {Z_np.shape}")

# ─────────────────────────────────────────────
# 4. CLUSTERING K-MEANS (3 profiles)
# ─────────────────────────────────────────────

print("\n── Clustering K-Means (3 profiles) ──")

kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=20)
labels = kmeans.fit_predict(Z_np)

score = silhouette_score(Z_np, labels)
print(f"silhouette_score : {score:.4f}  (closest of 1 = best scission)")

# Add labels in dataset
df_clean = df_clean.copy()
df_clean["profile"] = [f"Profile {l+1}" for l in labels]

# ─────────────────────────────────────────────
# 5. ANALYZE OF THE PROFILES
# ─────────────────────────────────────────────

print("\n── ANALYZE OF THE 3 PROFILES ──\n")

for p in sorted(df_clean["profile"].unique()):
    subset = df_clean[df_clean["profile"] == p]
    print(f"{'─'*40}")
    print(f"  {p}  –  {len(subset)} entries ({100*len(subset)/len(df_clean):.1f}%)")
    print(f"{'─'*40}")
    for col in df.columns:
        top = subset[col].value_counts().head(3)
        top_str = ", ".join([f"{v} ({c})" for v, c in zip(top.index, top.values)])
        print(f"  {col:35s}: {top_str}")
    print()

# ─────────────────────────────────────────────
# 6. EXPORT OF THE RESULTS
# ─────────────────────────────────────────────

OUTPUT_CSV = "dataset_with_profiles.csv"
df_clean.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Dataset with exported profiles → {OUTPUT_CSV}")

# ─────────────────────────────────────────────
# 7. VISUALIZATION
# ─────────────────────────────────────────────

print("\n── GENERATING VISUALIZATION ──")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Clustering – 3 user profiles", fontsize=14, fontweight="bold")

# 7a. Profiles repartition
counts = df_clean["profile"].value_counts()
colors = ["#4C72B0", "#DD8452", "#55A868"]
axes[0].pie(counts.values, labels=counts.index, autopct="%1.1f%%",
            colors=colors, startangle=90)
axes[0].set_title("Profiles repartition")

# 7b. Loss function
axes[2].plot(losses, color="#4C72B0", linewidth=2)
axes[2].set_title("Loss function")
axes[2].set_xlabel("Epoch")
axes[2].set_ylabel("MSE Loss")
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("clustering_visualisations.png", dpi=150, bbox_inches="tight")
print("✅ Visualization stored → clustering_visualizations.png")
plt.show()

# ─────────────────────────────────────────────
# 8. MODEL SAVING
# ─────────────────────────────────────────────
import joblib, os # joblib allows to convert python object to binary file

os.makedirs("models", exist_ok=True)
torch.save(model.state_dict(), "models/autoencoder.pt") # our backend will have to construct again the autoencodeur
														# state_dict() only extracts trained WEIGHTS from the neural network
                                                        
joblib.dump(kmeans, "models/kmeans.pkl")				# serialize the KMeans object directly, backend can call .predict() directly

joblib.dump(scaler, "models/scaler.pkl")				# save the StandardScaler with his mean values and delta calculated from the dataset
														# when the backend recieve the data from a user, it needs to normalize them with the same scaler !!!

joblib.dump(encoders, "models/encoders.pkl")			# if we decide later to use string values instead of integer, it will automatically convert it to
														# be understandable for our model
print("✅ MODELS STORED → models/")