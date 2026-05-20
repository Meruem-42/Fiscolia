import {Link} from 'react-router-dom'
import './index.css'
import logo from './assets/logo.png'


export const Header = ({ animatedLogo }) => {
    return (
        <header className="header">
            <img
				src={logo}
				alt="logo"
				className={ animatedLogo ? "header-logo-animated" : "header-logo"}
			/>
            <p>         </p>
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
        </header>
    )
};
export const Footer = () => {
    return (
		<footer
			style={{
				width: '100%',
				height: 'clamp(50px, 6vh, 90px)',
                flexShrink: '0',
				backgroundColor: '#cbd4db',
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'space-around'
			}}>
			<p>Contact</p>
		</footer>
    )
}