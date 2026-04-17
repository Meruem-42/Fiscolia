import pymupdf
import ollama
import chromadb
from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

OLLAMA_EMBED_MODEL = "nomic-embed-text"

def run_ingestion():
	embeddings_model = OllamaEmbeddings(
		model="nomic-embed-text",
		base_url="http://ollama:11434" # Ton URL Docker/Service
	)

	# 1. Définir le chemin du dossier
	# '.' signifie le dossier courant, ou utilise un chemin complet "C:/Dossier" ou "/home/user/"
	dossier = Path('./data')

	documents_complets = []

	# 2. Lister et ouvrir chaque fichier
	for fichier in dossier.iterdir():
		loader = PyPDFLoader(str(fichier))
		documents_complets.extend(loader.load())

	# text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
	# tous_les_chunks = text_splitter.split_documents(documents_complets)

	client_ollama = ollama.Client("http://ollama:11434")

	vectorstore = Chroma.from_documents(
		documents=documents_complets, # LangChain lit .page_content ET .metadata ici
		embedding=embeddings_model,
		persist_directory="./ma_base_chroma"
	)
	print(f"Nombre d'éléments dans la base : {vectorstore._collection.count()}")
	return (vectorstore)
	# La bdd vectorielle est cree

VECTORSTORE = run_ingestion()