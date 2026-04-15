import { Link } from 'react-router-dom';
import { useState } from 'react';


function Chatbot() {
  const [message, setMessage] = useState("");
  const [formData, setFormData] = useState({
	question: "",
  });

  const handleChange = (e) => {
	const { name, value } = e.target;
	setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
	e.preventDefault();
	console.log("User question :", formData);
	// ENVOYER les datas au bon backend
	try {
		const response = await fetch("/api/chatbot", {
			method: 'POST',
			headers: {
			'Content-Type': 'application/json',
			},
			body: JSON.stringify(formData)
		});
		console.log(response);
		if (!response.ok)
		{
			setMessage("INVALID USER QUESTION");
			return ;
		}
		const data = await response.json();
		console.log(data);
		setMessage(data.message);
	}
	catch (error) {
		setMessage("ERROR");
		console.log("Something went wrong...");
	}
	// BACKEND check si login existe ET si il existe check mdp
	// BACKEND renvoie success ou failed
	// SI SUCCESS redirige vers dashboard utilisateur (BIENVENUE {username})
	// SI FAILED message  de fail

  };

  return (
	<div style={{ textAlign: "center", alignContent: "center" }}>
	  <h1 style={{ color:"#000091"}}>CHATBOT</h1>
	  <form onSubmit={handleSubmit}>
		<p>Chatbot</p>
		<input type="text" name="question" value={formData.email} onChange={handleChange} placeholder="Question our chatbot" />
		<p>{message}</p>
		<button type="submit">Ask me</button>
	  </form>
	  <div>
		<Link to="/">
		  <button>Return to the home Page</button>
		</Link>
	  </div>
	</div>
  );
}

export default Chatbot