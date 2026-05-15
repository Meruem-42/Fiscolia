import {Link} from 'react-router-dom'

export const Header = () => {
    return (
        <div
            style={{
                width: '100%',
                height: '7vh',
                backgroundColor: 'white',
                display: 'flex',
                alignItems: 'right',
                justifyContent: 'flex-end'
            }}>
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
				height: '7vh',
				backgroundColor: '#cbd4db',
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'space-around'
			}}>
			<p>Contact</p>
		</div>
    )
}