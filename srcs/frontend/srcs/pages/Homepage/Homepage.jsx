
import {Link} from 'react-router-dom'
import './Homepage.css'
import { Header, Footer } from '../../Components_of_site.jsx'

function Home() {
	return (	
		<div className="page">
			<Header animateLogo={true} />
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
		<div
			style={{
				flex:1,
				display: 'flex',
				flexDirection: 'column',
				justifyContent: 'center',
				alignItems: 'center',
				paddingTop: '80px',
				boxSizing: 'border-box',
				overflowY: 'auto'
			}}>

			<p style={{ fontSize: 'clamp(1rem, 2vw, 2rem)' }}>Un projet, une vision</p>
			<h1 style={{ color: '#000091', fontFamily: 'montserat', fontSize: 'clamp(1rem, 8vw, 4rem)' }}>Fiscolia</h1>
		</div>
	)
}