
import {Link} from 'react-router-dom'


function Home() {
	return (
	<div>
		<p>Un projet, une vision</p>
		<h1 style={{ color: '#000091', fontFamily: 'montserat'}}>Fiscolia</h1>
	
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
	</div>
	)
  }

export default Home
