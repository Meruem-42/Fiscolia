
import {Link} from 'react-router-dom'
import './Homepage.css'
import logo from '../../assets/logo.png'
import '../../index.css'

function Home() {

	return (	
		<div className="default-background">

			<div className="intro-logo-homepage">
				<img src={logo} alt="logo" className="intro-logo-homepage-animation" />
			</div>
			
			<div className="main-body-style">
				<p>Un projet, une vision</p>
				<h1>Fiscolia</h1>
			</div>
			
		</div>
	)

}

export default Home