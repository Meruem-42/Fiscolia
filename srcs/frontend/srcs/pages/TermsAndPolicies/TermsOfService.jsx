import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { Header, Footer } from '../../Components_of_site.jsx'

function TermsOfService () {

    return (
        <div className="page">
            <Header animatedLogo={false} />
            <div className="default-background">
                This is Terms Of Service
            </div>
            <Footer />
        </div>
    )

}

export default TermsOfService