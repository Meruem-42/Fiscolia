import {Link} from 'react-router-dom'
import { useState } from 'react';
import './index.css'
import logo from './assets/logo.png'
import github_logo from './assets/github_logo.png'


export const Header = ({ animatedLogo }) => {

    const [menuOpen, setMenuOpen] = useState( false )

    return (
        <header className="header">
            
            <Link to="/" className="link-logo">
                <img
			    	src={logo}
			    	alt="logo"
			    	className={ animatedLogo ? "header-logo-animated" : "header-logo"}
			    />
            </Link>

            <button 
                className="burger-menu-button"
                onClick={() => setMenuOpen( !menuOpen )}
            >

                <span></span>
                <span></span>
                <span></span>
            </button>

            { menuOpen && (
                <nav className={ `burger-menu ${menuOpen ? "open" : "" }`} >
                    <a href="/">Home</a>
                    <a href="/login">Login</a>
                    <a href="/register">Register</a>
                </nav>
            )}

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