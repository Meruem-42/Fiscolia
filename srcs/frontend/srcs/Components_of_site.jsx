import {Link} from 'react-router-dom'
import './index.css'

export const Header = () => {
    return (
        <div className="header">
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
        </div>
    )
};
export const Footer = () => {
    return (
		<div
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
		</div>
    )
}