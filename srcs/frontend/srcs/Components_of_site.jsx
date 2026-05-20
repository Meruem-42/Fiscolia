import {Link} from 'react-router-dom'
import './index.css'
import logo from './assets/logo.png'
import github_logo from './assets/github_logo.png'


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
}

export const Footer = () => {
    
    return (
		<footer className="footer" >
            <Link to="/privacy_policy" className="terms-and-policies">
                Privacy Policy
            </Link>

            <a
                href="https://github.com/a-herlaud/Fiscolia"
                target="_blank"
                rel="noopener noreferrer"
            >
                <img 
                    src={github_logo} 
                    alt="github logo"
                    className="github-logo"
                />
            </a>

            <Link to="/terms_of_service" className="terms-and-policies">
                Terms of Service
            </Link>
		</footer>
    )

}