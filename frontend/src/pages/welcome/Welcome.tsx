import './Welcome.css'
import background_rpg from "../../assets/background-rpg-vertical.svg"

function Welcome() {

    return (
        <div className="welcome-container">
        <img src={background_rpg} alt="RPG characters" className="welcome-image" />
        <div className="welcome-content">
            <h1>Welcome!</h1>
            <div className='button-container'>
                <button className="sign-in">Sign in</button>
                    <span>or</span>
                <button className='sign-up'>Sign up</button>
            </div>
        </div>
        </div>
    );
}

export default Welcome;