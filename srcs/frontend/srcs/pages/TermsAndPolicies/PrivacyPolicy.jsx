import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { Header, Footer } from '../../Components/Components_of_site.jsx'

function PrivacyPolicy () {

    return (
        <div className="page">
            <Header animatedLogo={false} />
            <div className="default-background">
                This is Privacy Policy
            </div>
            <Footer />
        </div>
    )

}

export default PrivacyPolicy