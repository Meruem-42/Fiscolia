import { Link } from 'react-router-dom';
import { useState } from 'react';


function Login() {
  const [message, setMessage] = useState("");
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Données récupérées :", formData);
	// ENVOYER les datas au bon backend
	try {
		const response = await fetch("/api/auth-login", {
			method: 'POST',
			headers: {
    		'Content-Type': 'application/json',
  			},
			body: JSON.stringify(formData)
		});
		const data = response.json();
		if (!data.ok)
		{
			setMessage("ERROR");
			return ;
		}
		setMessage(data.message);
	}
	catch (error) {
		setMessage("ERROR");
		console.log("EROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOR");
	}
	// BACKEND check si login existe ET si il existe check mdp
	// BACKEND renvoie success ou failed
	// SI SUCCESS redirige vers dashboard utilisateur (BIENVENUE {username})
	// SI FAILED message  de fail

  };

  return (
    <div style={{ textAlign: "center", alignContent: "center" }}>
      <form onSubmit={handleSubmit}>
        <p>Email</p>
        <input type="text" name="email" value={formData.email} onChange={handleChange} placeholder="Email" />
        <p>Mot de passe</p>
        <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Password" />
		<p>{message}</p>
        <button type="submit">Connect</button>
      </form>
      <div>
        <Link to="/">
          <button>Return to Home page</button>
        </Link>
      </div>
    </div>
  );
}

// function MonFormulaire() {
//   const [formData, setFormData] = useState({
//     nom: "",
//     email: "",
//   });

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setFormData((prev) => ({ ...prev, [name]: value }));
//   };

//   const handleSubmit = (e) => {
//     e.preventDefault(); // empêche le rechargement de la page
//     console.log("Données récupérées :", formData);
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <input name="nom" value={formData.email} onChange={handleChange} placeholder="Nom" />
//       <input name="email" value={formData.email} onChange={handleChange} placeholder="Email" />
//       <button type="submit">Envoyer</button>
//     </form>
//   );
// }

export default Login