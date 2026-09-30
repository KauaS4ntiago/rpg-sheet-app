import './Welcome.css'
import background_rpg from "../../assets/background-rpg-vertical.svg"
import { Link } from 'react-router-dom';
import VerticalTransition from '../../components/Animations/VerticalTransition';

function Welcome() {

    return (
        <div className="welcome-container">
            <img src={background_rpg} alt="RPG characters" className="welcome-image" />
            <VerticalTransition className="welcome-content" >
                <h1>Welcome!</h1>
                <div className="button-container">
                    <Link to="/login" className="sign-in">Sign in</Link>
                    <span>or</span>
                    <Link to="/register" className="sign-up">Sign up</Link>
                </div>
            </VerticalTransition>
        </div>
    );
}

export default Welcome;