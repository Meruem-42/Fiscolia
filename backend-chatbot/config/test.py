import ollama
import pymupdf
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
# import nomic-embed-text


OLLAMA_EMBED_MODEL = "nomic-embed-text"
OLLAMA_CHAT_MODEL = "mistral:latest"
READY_MODELS = set()


def ensure_model(client, model_name):
	if model_name in READY_MODELS:
		return
	client.pull(model=model_name)
	READY_MODELS.add(model_name)


def	get_agent_answer(user_question):
	print("Debug from get agent answer")
	doc = pymupdf.open("data/bofip.pdf")
	texte_complet = ""

	for page in doc:
		texte = page.get_text()
		texte_complet += texte
		# print(texte)

	splitter = RecursiveCharacterTextSplitter(
		chunk_size=500,
		chunk_overlap=50,
		separators=["\n\n", "\n", ".", " "]
	)


	# 2. Créer le client Ollama et générer l'embedding
	client_ollama = ollama.Client("http://ollama:11434")
	ensure_model(client_ollama, OLLAMA_EMBED_MODEL)
	ensure_model(client_ollama, OLLAMA_CHAT_MODEL)
	embeddings = []
	ids = []
	metadatas = []
	chunks = splitter.split_text(texte_complet)
	# chunks est simplement une liste de strings


	for i, chunk in enumerate(chunks):
		# print(f"Chunk {i + 1} :")
		# print(chunk)
		# print("--------------------------------------------------")
		response = client_ollama.embeddings(
			model=OLLAMA_EMBED_MODEL,
			prompt=chunk
		)
		embeddings.append(response["embedding"])
		ids.append(f"doc_{i}")
		metadatas.append({"source": "bofip.pdf", "page": i + 1})

	# 3. Stocker dans ChromaDB
	client_chroma = chromadb.PersistentClient(path="./chroma_db")
	collection = client_chroma.get_or_create_collection("ma_collection")

	collection.add(
		ids=ids,
		embeddings=embeddings,
		documents=chunks,
		metadatas=metadatas
	)

	doc.close()

	# question_user = "Comment remplir sa fiche des impots pour un particulier en France en avril 2026 ?"
	question_user = user_question
	# question_user = data

	embedding_question = client_ollama.embeddings(
		model=OLLAMA_EMBED_MODEL,
		prompt=question_user
	)

	# 2. Chercher les chunks les plus proches dans ChromaDB
	resultats = collection.query(
		query_embeddings=[embedding_question["embedding"]],
		n_results=5  # top-K, tu ajustes selon la qualité des réponses
	)

	# On itère sur les index (0 à 4)
	for i in range(len(resultats["ids"][0])):
		print(f"--- RÉSULTAT N°{i+1} ---")
		print(f"ID       : {resultats['ids'][0][i]}")
		print(f"DISTANCE : {resultats['distances'][0][i]:.4f}")
		
		# Vérification sécurisée des métadonnées
		current_meta = resultats['metadatas'][0][i] if resultats['metadatas'] else None
		
		if current_meta is not None:
			print(f"SOURCE   : Page {current_meta.get('page', 'Inconnue')}")
		else:
			print("SOURCE   : Aucune métadonnée disponible")
		
		print(f"CONTENU  : {resultats['documents'][0][i][:200]}...")
		print("\n")

	print("********")

	# 3. Extraire le texte des chunks retrouvés
	chunks = resultats["documents"][0]  # liste de strings
	metas = resultats["metadatas"][0]



	# 4. Construire le prompt
	contexte = "\n\n---\n\n".join(chunks)
	prompt = f"""Tu es un assistant fiscal français.
	Réponds uniquement en te basant sur le contexte ci-dessous.
	Si la réponse n'est pas dans le contexte, dis-le clairement.

	CONTEXTE :
	{contexte}

	QUESTION :
	{question_user}

	RÉPONSE :"""

	# 5. Envoyer à Mistral
	reponse = client_ollama.chat(
		model=OLLAMA_CHAT_MODEL,
		messages=[{"role": "user", "content": prompt}]
	)

	print(reponse["message"]["content"])
	return (reponse["message"]["content"])