
import {Link} from 'react-router-dom'
import './Homepage.css'
import logo from '../../assets/logo.png'
import '../../index.css'

function Home() {

	return (
		<div className="main-body-style">
			<div className="intro-logo-homepage">
				<img src={logo} alt="logo" className="intro-logo-homepage-animation" />
			</div>
			<p>Un projet, une vision</p>
			<h1>Fiscolia</h1>
		</div>			
	)

}

export default Home