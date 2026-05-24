import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { handleLogout } from './pages/Utils/Logout.jsx'
import './index.css'
import logo from './assets/logo.png'
import github_logo from './assets/github_logo.png'


export const Header = ({ isAuthenticated, setIsAuthenticated }) => {

    const location = useLocation();
    const isHomePage = location.pathname === "/";
    const [menuOpen, setMenuOpen] = useState( false );
    const navigate = useNavigate();

    return (
        <header className="header-style">
            
            <Link to="/" className="link-logo">
                <img
			    	src={logo}
			    	alt="logo"
                    key={ location.pathname }
			    	className={ isHomePage ? "header-logo-animated" : "header-logo"}
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
                    <Link to="/">Home</Link>

                    { isAuthenticated ? (
                        <>
                            <Link to="/session">Mon Profil</Link>
                            <button className="menu-button-logout" type="button" onClick={ () => handleLogout(navigate, setIsAuthenticated) }>
                                Se deconnecter
                            </button>
                        </>
                    ) : (
                        <>
                            <Link to="/login">Login</Link>
                            <Link to="/register">Register</Link>
                        </>
                    )
                    }
                </nav>
            )}

        </header>
    )

}
export default Header;

export const Footer = () => {
    
    return (
		<footer className="footer-style" >
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