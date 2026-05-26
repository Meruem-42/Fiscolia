import ollama
import pymupdf
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

OLLAMA_CHAT_MODEL = "llama3.2:1b"
OLLAMA_BASE_URL = "http://ollama:11434"
PERSIST_DIR = "./ma_base_chroma"
OLLAMA_EMBED_MODEL = "nomic-embed-text"

client_ollama = ollama.Client(OLLAMA_BASE_URL)

def get_agent_answer(user_question):

	embeddings_model = OllamaEmbeddings(
		model=OLLAMA_EMBED_MODEL,
		base_url=OLLAMA_BASE_URL,
	)
	print("Test 1")

	vectorstore = Chroma(
		persist_directory=PERSIST_DIR,
		embedding_function=embeddings_model,
		collection_name="ma_collection",
	)

	print("Test 2")
	resultats = vectorstore.similarity_search(user_question)
	print("Test 3")

	# 4. Construire le prompt
	contexte = "\n\n---\n\n".join([doc.page_content for doc in resultats])
	prompt = f"""Tu es un assistant fiscal français.
	Réponds uniquement en te basant sur le contexte ci-dessous.
	Si la réponse n'est pas dans le contexte, dis-le clairement.

	CONTEXTE :
	{contexte}

	QUESTION :
	{user_question}

	RÉPONSE :"""
	
	return (prompt)