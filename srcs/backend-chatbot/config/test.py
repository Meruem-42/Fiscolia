import ollama
import pymupdf
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from create_vector_db import OLLAMA_EMBED_MODEL, VECTORSTORE

OLLAMA_CHAT_MODEL = "mistral:latest"
client_ollama = ollama.Client("http://ollama:11434")

def	get_agent_answer(user_question):
	print("Test 1")
	resultats = VECTORSTORE.similarity_search(user_question)
	print("Test 2")

	# On itère sur les index (0 à 4)
	# for i in range(len(resultats["ids"][0])):
	# 	print(f"--- RÉSULTAT N°{i+1} ---")
	# 	print(f"ID       : {resultats['ids'][0][i]}")
	# 	print(f"DISTANCE : {resultats['distances'][0][i]:.4f}")
		
	# 	# Vérification sécurisée des métadonnées
	# 	current_meta = resultats['metadatas'][0][i] if resultats['metadatas'] else None
		
	# 	if current_meta is not None:
	# 		print(f"SOURCE   : Page {current_meta.get('page', 'Inconnue')}")
	# 	else:
	# 		print("SOURCE   : Aucune métadonnée disponible")
		
	# 	print(f"CONTENU  : {resultats['documents'][0][i][:200]}...")
	# 	print("\n")

	print("********")

	# # 3. Extraire le texte des chunks retrouvés
	# chunks = resultats["documents"][0]  # liste de strings
	# metas = resultats["metadatas"][0]



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

	# 5. Envoyer à Mistral
	reponse = client_ollama.chat(
		model=OLLAMA_CHAT_MODEL,
		messages=[{"role": "user", "content": prompt}]
	)
	print(reponse["message"]["content"])
	return (reponse["message"]["content"])