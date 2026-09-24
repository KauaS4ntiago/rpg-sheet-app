import '../auth.css'
import background_rpg from '../../../assets/background-rpg-vertical.svg'
import { Mail, Lock, User, Eye, EyeOff} from 'lucide-react';
import { Link } from 'react-router-dom'
import { usePasswordVisibility } from '../../../hooks/usePasswordVisibility';
import AuthenticationTransition from '../../../components/AuthenticationTransition';

function Register() {
    const passwordInput = usePasswordVisibility();
    const confirmPasswordInput = usePasswordVisibility();

    return (
        <div className="auth-container">
            <img src={background_rpg} alt="RPG characters" className="auth-image" />
            <AuthenticationTransition className="auth-content">
                <h1>Register</h1>
                <form>
                    <div className="input-container">
                        <label htmlFor="username">Username</label>
                        <div className="input-wrapper">
                            <User className="input-icon" />
                            <input type="text" id="username" placeholder="your username" className="auth-input" />
                        </div>

                        <label htmlFor="email">Email</label>
                        <div className="input-wrapper">
                            <Mail className="input-icon" />
                            <input type="email" id="email" placeholder="you@example.com" className="auth-input" />
                        </div>

                        <label htmlFor="password">Password</label>
                        <div className="input-wrapper">
                            <Lock className="input-icon" />
                            <input type={passwordInput.visible ? "text" : "password"} id="password" placeholder="must have at least 8 characters" className="auth-input" />
                            <button type="button" className="visibility-toggle" onClick={passwordInput.toggleVisibility}>
                                {passwordInput.visible ? <Eye className="visibility-icon" /> : <EyeOff className="visibility-icon" />}
                            </button>
                        </div>

                        <label htmlFor="confirm-password">Confirm Password</label>
                        <div className="input-wrapper">
                            <Lock className="input-icon" />
                            <input type={confirmPasswordInput.visible ? "text" : "password"} id="confirm-password" placeholder="must match the password above" className="auth-input" />
                            <button type="button" className="visibility-toggle" onClick={confirmPasswordInput.toggleVisibility}>
                                {confirmPasswordInput.visible ? <Eye className="visibility-icon" /> : <EyeOff className="visibility-icon" />}
                            </button>
                        </div>
                    </div>
                    
                    <button className="input-button">Sign up</button>                
                </form>
                <p>Already have an account? <Link to="/login">Sign in</Link></p>
            </AuthenticationTransition>
        </div>
    );
}

export default Register;