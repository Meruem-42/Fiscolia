
import {Link} from 'react-router-dom'
import './Homepage.css'
import { Header, Footer } from '../../Components_of_site.jsx'
import logo from '../../assets/logo.png'
import '../../index.css'

function Home() {

	return (	
		<div className="page">
			<div className="intro-logo-homepage">
				<img src={logo} alt="logo" className="intro-logo-homepage-animation" />
			</div>

			<Header animatedLogo={true} />

			<div className="default-background">
				<MainBody />
			</div>

			<Footer />
		</div>
	)

}

export default Home

const MainBody = () => {

	return (
		<div className="main-body-style">
			<p>Un projet, une vision</p>
			<h1>Fiscolia</h1>
		</div>
	)

}