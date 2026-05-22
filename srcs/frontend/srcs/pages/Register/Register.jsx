import { Link } from 'react-router-dom';
import { useState } from 'react';
import validator from 'validator';
import style from './Register.module.css';
import '../../index.css'



const getIndicatorStyle = (field, isRuleMet) => {

  return {
    color: field.length === 0 ? "var(--color-gray)" : (isRuleMet? "#0ac900" : "#E1000F"),
    fontSize: "clamp( 0.5rem, 1vw, 0.6rem )",
    marginBottom: "clamp( 0.1rem, 1vw, 0.5rem )",
    fontWeight: "bold",
  };

};

function Register() {

  const [message, setMessage] = useState("");
  const [formData, setFormData] = useState({
    email: "",
    confirm_email: "",
    password: "",
    confirm_password: "",
    firstname: "",
    lastname: "",
  });

  const getValidation = (field, value, data) => {

    switch (field) {
      case "email":
        return {
          not_empty: value.trim() !== "",
          valid: validator.isEmail(value),
          valid_format: /^[a-zA-Z0-9][a-zA-Z0-9._%-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value),
          min_length: value.length >= 5,
          max_length: value.length <= 254,
        };
      case "password":
        return {
          length: value.length >= 8,
          upper: /[A-Z]/.test(value),
          lower: /[a-z]/.test(value),
          digit: /[0-9]/.test(value),
        };
      case "confirm_password":
        return {
          match_pwd:  value === data.password && value != "",
        };
      case "confirm_email":
        return {
          match_email:  value === data.email && value != "",
        };
      default:
        return {};
    }

  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // VERIFICATION DATA
  const fieldsToValidate = ["email", "password", "confirm_password", "firstname", "lastname"];

  // 2. On boucle sur chaque champ
  for (const fieldName of fieldsToValidate) {
    const value = formData[fieldName];
    const rules = getValidation(fieldName, value, formData); // On appelle ta fonction universelle
    
    // On vérifie si TOUTES les règles du champ actuel sont à true
    const isFieldValid = Object.values(rules).every(v => v === true);

    if (!isFieldValid) {
      // Si une règle échoue, on définit le message et on S'ARRÊTE là (return)
      setMessage(`Erreur dans le champ : ${fieldName}`);
      return;
    }
  }

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
			setMessage("Une erreur est survenue");
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
	// BACKEND check si Register existe ET si il existe check mdp
	// BACKEND renvoie success ou failed
	// SI SUCCESS redirige vers dashboard utilisateur (BIENVENUE {username})
	// SI FAILED message  de fail

};
const pwdRules = getValidation("password", formData.password,formData);
const emailRules = getValidation("email", formData.email);
const confirmRulesPwd = getValidation("confirm_password", formData.confirm_password, formData);
const confirmRulesEmail = getValidation("confirm_email", formData.confirm_email, formData);

  return (

    <div className="main-body-style">
      <form className={style.register_form} onSubmit={handleSubmit}>
        <h1 className="auth-page-title">REGISTER</h1>
        <div className="auth-field-container">
          <p className="auth-field-name" >Email</p>
          <input type="text" name="email" value={formData.email} onChange={handleChange} placeholder="Email" />
        </div>
        <div className="auth-field-container">
          <p className="auth-field-name">Retaper votre email</p>
          <div className="auth-rules-verification">
            <span style={getIndicatorStyle(formData.email, confirmRulesEmail.match_email)}>Same email</span>
          </div>
          <input type="email" name="confirm_email" value={formData.confirm_email} onChange={handleChange} placeholder="Confirm Email" />
        </div>
        <div className="auth-field-container">
          <p className="auth-field-name">Mot de passe</p>
          <div className="auth-rules-verification">
            <span style={getIndicatorStyle(formData.password, pwdRules.length)}>8+ chars</span>
            <span style={getIndicatorStyle(formData.password, pwdRules.upper)}>Majuscule</span>
            <span style={getIndicatorStyle(formData.password, pwdRules.lower)}>Minuscule</span>
            <span style={getIndicatorStyle(formData.password, pwdRules.digit)}>Chiffre</span>
          </div>
          <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Password" />
        </div>
        <div className="auth-field-container">
          <p className="auth-field-name">Retaper votre mot de passe</p>
          <div className="auth-rules-verification">
            <span style={getIndicatorStyle(formData.password, confirmRulesPwd.match_pwd)}>Same password</span>
          </div>
          <input type="password" name="confirm_password" value={formData.confirm_password} onChange={handleChange} placeholder="Confirm Password" />
        </div>
        <div className="auth-field-container">
          <p className="auth-field-name">Prenom</p>
          <input type="text" name="firstname" value={formData.firstname} onChange={handleChange} placeholder="Prenom" />
        </div>
        <div className="auth-field-container">
          <p className="auth-field-name">Nom</p>
          <input type="text" name="lastname" value={formData.lastname} onChange={handleChange} placeholder="Nom" />
        </div>
        <div>
		      <div className="auth-error-message">{message}</div>
          <button className="auth-button" type="submit">Create Account</button>
        </div>
        <div>
          <Link to="/">
            <button className="auth-button">Return to Home page</button>
          </Link>
        </div>
      </form>
    </div>
  )

}

export default Register