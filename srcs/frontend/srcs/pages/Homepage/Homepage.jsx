
import {Link} from 'react-router-dom'
import './Homepage.css'
import img_logo from '../../assets/logo.png'
import img_chatbot from '../../assets/site_screenshots/chatbot.png'
import img_emoji from '../../assets/site_screenshots/emoji.png'
import img_menu from '../../assets/site_screenshots/menu.png'
import img_modify_profil from '../../assets/site_screenshots/modify_profil.png'
import img_watch from '../../assets/watch.jpg'
import img_paix from '../../assets/paix.png'
import '../../index.css'

function Home() {

	return (
		<div className="homepage-body">
			<div className="home-block">
				<div className="text-home-block">
					<h2 className="homepage-h2">Fiscolia</h2>
					<h2 className="homepage-h2">Assistance pour remplir votre</h2>
					<h2 className="homepage-h2">déclaration fiscale</h2>
					<p className="homepage-p">Ça n'a jamais été aussi simple</p>
				</div>
				<div className="photo-emoji-home-block">
					<img src={img_emoji} alt="emoji" />
				</div>
			</div>

			<br />
			<br />
			<br />
			<br />

			<div className="home-block">
				<div className="photo-home-block">
					<img src={img_chatbot} alt="chatbot_page" />
				</div>
				<div className="text-home-block">
					<h2 className="homepage-h2">Déclarez vos impôts simplement et en toute confiance</h2>
					<p className="homepage-p">Notre assistant intelligent analyse des milliers de situations similaires pour vous guider à chaque étape de votre déclaration</p>
				</div>
			</div>

			<br />
			<br />
			<br />
			<br />

			<div className="home-block">
				<div className="photo-home-block">
					<img src={img_watch} alt="watch" />
				</div>
				<div className="text-home-block">
					<h2 className="homepage-h2">Pourquoi choisir une assistance?</h2>
					<p className="homepage-p">🤖 Gagnez du temps grâce à une assistance personnalisée</p>
					<p className="homepage-p">⚡ Réduisez les erreurs en profitant de recommandations adaptées à votre situation</p>
					<p className="homepage-p">📄 Obtenez des suggestions intelligentes basées sur des profils comparables</p>
					<p className="homepage-p">🚀 Remplissez vos formulaires en quelques minutes, sans connaissances fiscales particulières</p>
				</div>
			</div>

			<br />
			<br />
			<br />
			<br />

			<div className="home-block">
				<div className="photo-home-block">
					<img src={img_paix} alt="paix" />
				</div>
				<div className="text-home-block">
					<h2 className="homepage-h2">Moins de stress, plus de clarté</h2>
					<p className="homepage-p">L'IA vous guide, vous gardez le contrôle</p>
				</div>
			</div>
			
			<br />
			<br />
			<br />
			<br />

			<div className="home-block">
				<div className="photo-home-block">
					<img src={img_menu} alt="menu" />
				</div>
				<div className="text-home-block">
					<h2 className="homepage-h2">Passer facilement l'authentification</h2>
					<p className="homepage-p">Cliquez sur le menu et sélectionnez de s'inscrire ou de se connecter</p>
				</div>
			</div>
			<div className="home-block">
				<div className="photo-home-block">
					<img src={img_modify_profil} alt="modify_profil_page" />
				</div>
				<div className="text-home-block">
					<h2 className="homepage-h2">Modifiez facilement votre profil</h2>
					<p className="homepage-p">Cliquez sur le menu et sélectionnez de vous inscrire ou de vous connecter</p>
				</div>
			</div>

			<br />
			<br />


			<div className="home-block">
				<div className="text-home-block">
					<h2 className="homepage-h2">Les articles intéressants à lire</h2>
				</div>
			</div>
			<div className="home-block">
				<div className="link-home-block">
					<a href="https://www.impots.gouv.fr/toutes-les-questions/particulier/puis-je-declarer-en-ligne-pour-ma-premiere-declaration-de-revenus" className="homepage-p">
						Puis-je déclarer en ligne pour ma première déclaration de revenus ?
					</a>
				</div>
				<div className="link-home-block">
					<a href="https://www.service-public.gouv.fr/particuliers/vosdroits/F359" className="homepage-p">
						Quelle est la date limite pour faire sa déclaration de revenus pour les impôts ?
					</a>
				</div>
				<div className="link-home-block">
					<a href="https://www.lemonde.fr/idees/article/2024/03/29/impots-le-combat-pour-une-fiscalite-juste-depasse-la-seule-dimension-economique_6224884_3232.html" className="homepage-p">
						Impôts : « Le combat pour une fiscalité juste dépasse la seule dimension économique »
					</a>
				</div>
			</div>

			{/*<div className="intro-logo-homepage">
				<img src={img_logo} alt="logo" className="intro-logo-homepage-animation" />
			</div>*/}
			{/*<p>Un projet, une vision</p>*/}
			{/*<p>Capture d'ecran</p>
			<br />
			<p>du menu</p>
			<h1>Fiscolia</h1>*/}
		</div>			
	)

}

export default Home