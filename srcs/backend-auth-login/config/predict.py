import torch
import torch.nn as nn
import joblib
import numpy as np
from pathlib import Path
from connect_db import engine

# ─────────────────────────────────────────────
# Même architecture que dans training.py
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
# Chargement des artefacts (une seule fois au démarrage)
# ─────────────────────────────────────────────

INPUT_DIM  = 5   # nombre de features (etat_civil, quotient_familial, etc.)
LATENT_DIM = 8   # même valeur que dans training.py

# Prioritize container mount (/models) and keep a local fallback for dev runs.
MODEL_DIR = Path("/models") if Path("/models").exists() else Path(__file__).resolve().parents[3] / "models"

scaler = None
encoders = None
kmeans = None

def load_models():
	try :
		scaler   = joblib.load(MODEL_DIR / "scaler.pkl")
		encoders = joblib.load(MODEL_DIR / "encoders.pkl")
		kmeans   = joblib.load(MODEL_DIR / "kmeans.pkl")
		print("scaler, encoders and kmeans created")
	except:
		return None, None, None, None

	model = Autoencoder(INPUT_DIM, LATENT_DIM)
	model.load_state_dict(torch.load(MODEL_DIR / "autoencoder.pt", weights_only=True))
	model.eval()  # désactive le dropout/batchnorm en mode training
	return model, scaler, encoders, kmeans

# ─────────────────────────────────────────────
# Fonction principale : données user → profil
# ─────────────────────────────────────────────

def predict_profile(user_data: dict) -> int:
	"""
	user_data = {
		"etat_civil":         0,
		"quotient_familial":  1500,
		"situation_specifique": 0,
		"rni":                25000,
		"csp":                3
	}
	Retourne : 1, 2, ou 3
	"""
	# 1. Load le modele
	model, scaler, encoders, kmeans = load_models()
	if model is None:
		return None

	# 1. Encodage des champs catégoriels (si texte)
	encoded = {}
	for col, value in user_data.items():
		if col in encoders:
			encoded[col] = encoders[col].transform([str(value)])[0]
		else:
			encoded[col] = value

	# 2. Mise en forme + normalisation
	features = np.array(list(encoded.values()), dtype=float).reshape(1, -1)
	print(f"ensemble des features : {features}")
	print(f"ensemble encoded : {encoded}")
	features_scaled = scaler.transform(features)

	# 3. Passage dans l'autoencodeur → vecteur latent
	tensor = torch.tensor(features_scaled, dtype=torch.float32)
	with torch.no_grad():
		_, latent = model(tensor)

	# 4. KMeans → cluster
	cluster = kmeans.predict(latent.numpy())[0]

	print(f"Le modèle ressemble à {model}")

	return int(cluster) + 1  # +1 pour avoir Profil 1/2/3 au lieu de 0/1/2

import sqlalchemy as sa

def describe_profiles():
	"""
	Parcourt la table 'userdata', fait passer chaque user dans le modèle,
	et retourne les moyennes des features par profil.

	Retourne un dict :
	{
		1: {"etat_civil": 0.4, "quotient_familial": 1200.0, ...},
		2: {...},
		3: {...},
	}
	"""
	print("hello describe profile")
	print("T1")

	with engine.connect() as conn:
		rows = conn.execute(
			sa.text(
				"SELECT etat_civil, quotient_familial, situation_specifique, rni, csp "
				"FROM userdata"
			)
		).fetchall()

	if not rows:
		return {}

	FEATURE_KEYS = ["etat_civil", "quotient_familial", "situation_specifique", "rni", "csp"]

	# Accumulation par profil : {profil: {feature: [valeurs...]}}
	from collections import defaultdict
	buckets: dict[int, dict[str, list]] = defaultdict(lambda: defaultdict(list))

	for row in rows:
		user_data = dict(zip(FEATURE_KEYS, row))
		profil = predict_profile(user_data)
		if profil is None:
			continue
		for key, value in user_data.items():
			buckets[profil][key].append(float(value))

	# Calcul des moyennes
	result = {}
	for profil, features in sorted(buckets.items()):
		result[profil] = {
			key: round(sum(vals) / len(vals), 4)
			for key, vals in features.items()
		}

	return result

def extract_profiles_info():
	result = describe_profiles()
	list_of_prompts = []

	if not result:
		return list_of_prompts

	for profile, features in sorted(result.items()):
		prompt_lines = [f"Profil {profile}:"]
		for key, val in features.items():
			prompt_lines.append(f"- {key}: {val}")
		list_of_prompts.append("\n".join(prompt_lines))

	if list_of_prompts:
		print(list_of_prompts[0])

	return list_of_prompts