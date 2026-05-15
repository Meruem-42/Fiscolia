
import {Link} from 'react-router-dom'
import './Homepage.css'
import logo from './assets/logo.png'
import { Header, Footer } from '../../Components_of_site.jsx'

function Home() {
	return (		
		<div className="default-background">
			<Header />
			<MainBody />
			<Footer />
		</div>
	)
  }

export default Home

const MainBody = () => {
	return (
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
	)
}