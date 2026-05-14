
import {Link} from 'react-router-dom'
import './Homepage.css'
import logo from './assets/logo.png'

function Home() {
	return (
		
	<div 
		/*Background*/
		style={{
			minHeight: '100vh',
			background: 'linear-gradient(to bottom, #05337c, #ebf6ff)',
			display: 'flex',
			flexDirection: 'column',
			color: 'black'
		}}>
		{/**/}

		{/*TOP part: Navigation bar*/}
		<div
			style={{
				width: '100%',
				height: '70px',
				backgroundColor: 'white',
				display: 'flex',
				alignItems: 'right',
				justifyContent: 'space-around'
			}}>
			<p>         </p>
			<div>
				<Link to="/backend">
					<button>BACKEND</button>
				</Link>
			</div>
			<div>
				<Link to="/login">
					<button>LOGIN</button>
				</Link>
			</div>
			<div>
				<Link to="/register">
					<button>REGISTER</button>
				</Link>
			</div>
		</div>
		{/*MAIN part*/}
		<div
			style={{
				flex:1,
				display: 'flex',
				flexDirection: 'column',
				justifyContent: 'center',
				alignItems: 'center'
			}}>
			<img
				src={logo}
				alt="logo"
				className="animated-logo"
			/>
			<p>Un projet, une vision</p>
			<h1 style={{ color: '#000091', fontFamily: 'montserat'}}>Fiscolia</h1>
		</div>
		
		{/*BOTTOM part: footer*/}
		<div
			style={{
				width: '100%',
				height: '70px',
				backgroundColor: '#cbd4db',
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'space-around'
			}}>
			<p>Contact</p>
		</div>
	</div>
	)
  }

export default Home
