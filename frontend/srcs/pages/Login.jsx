import { Link } from 'react-router-dom'

function Login() {

return (
	<div style={{ textAlign:'center', alignContent:'center'}}>
		<p>Email</p>
		<form action="">
			<input type="text" name="Email" />
		</form>
		<p>Mot de passse</p>
		<form action="">
			<input type="text" name="Mot de passe"/>
		</form>
		<button>
			Connect
		</button>
		<div>
			<Link to="/">
				<button>Return to Home page</button>
			</Link>
		</div>
	</div>
)

}

export default Login