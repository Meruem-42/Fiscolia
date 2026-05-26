from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

PERSIST_DIR = "./ma_base_chroma"
OLLAMA_BASE_URL = "http://ollama:11434"
OLLAMA_EMBED_MODEL = "nomic-embed-text"


# def run_ingestion():
print("Démarrage de l'ingestion...")

# Modèle d'embeddings
embeddings_model = OllamaEmbeddings(
    model=OLLAMA_EMBED_MODEL,
    base_url=OLLAMA_BASE_URL,
)

# Chargement des PDFs
dossier = Path('./data')
documents_complets = []

for fichier in dossier.iterdir():
    if fichier.suffix.lower() == ".pdf":  # ← filtre les non-PDF
        print(f"  Chargement : {fichier.name}")
        loader = PyPDFLoader(str(fichier))
        documents_complets.extend(loader.load())

if not documents_complets:
    raise ValueError("Aucun document chargé ! Vérifie le dossier ./data")

print(f"{len(documents_complets)} pages chargées.")

# Découpage en chunks (RECOMMANDÉ pour la qualité des recherches)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
chunks = text_splitter.split_documents(documents_complets)
print(f"{len(chunks)} chunks créés.")

# Création et persistance automatique de la base vectorielle
# Pas besoin de .persist() — c'est automatique avec chromadb >= 0.4
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings_model,
    persist_directory=PERSIST_DIR,
    collection_name="ma_collection",
)

count = vectorstore._collection.count()
print(f"✅ Base créée : {count} vecteurs dans {PERSIST_DIR}")
# return vectorstore