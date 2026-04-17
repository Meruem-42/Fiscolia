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
		const response = await fetch("/api/auth-register", {
			method: 'POST',
			headers: {
    		'Content-Type': 'application/json',
  			},
			body: JSON.stringify(formData)
		});
		console.log(response);
		if (!response.ok)
		{
			setMessage("Invalid email format");
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
      <h1 style={{ color:"#000091"}}>REGISTER</h1>
      <form onSubmit={handleSubmit}>
        <p>Email*</p>
        <input type="text" name="email" value={formData.email} onChange={handleChange} placeholder="Email" />
        <p>Mot de passe*</p>
        <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Password" />
		<p>{message}</p>
        <button type="submit">Create Account</button>
      </form>
      <div>
        <Link to="/">
          <button>Return to Home page</button>
        </Link>
      </div>
    </div>
  );
}

export default Login