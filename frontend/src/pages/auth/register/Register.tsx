import '../auth.css'
import background_rpg from '../../../assets/background-rpg-vertical.svg'
import { Mail, Lock, User, Eye, EyeOff} from 'lucide-react';
import { Link } from 'react-router-dom'
import { usePasswordVisibility } from '../../../hooks/usePasswordVisibility';
import AuthenticationTransition from '../../../components/AuthenticationTransition';
import { useState } from 'react';

function Register() {
    const passwordInput = usePasswordVisibility();
    const confirmPasswordInput = usePasswordVisibility();
    const [userName, setUserName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

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
                            <input 
                            type="text" 
                            id="username" 
                            placeholder="your username" 
                            value={userName}
                            onChange={(e) => setUserName(e.target.value)}
                            className="auth-input" />
                        </div>

                        <label htmlFor="email">Email</label>
                        <div className="input-wrapper">
                            <Mail className="input-icon" />
                            <input 
                            type="email" 
                            id="email" 
                            placeholder="you@example.com" 
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="auth-input" />
                        </div>

                        <label htmlFor="password">Password</label>
                        <div className="input-wrapper">
                            <Lock className="input-icon" />
                            <input 
                            type={passwordInput.visible ? "text" : "password"} 
                            id="password" placeholder="must have at least 8 characters" 
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="auth-input" />
                            <button 
                            type="button" 
                            className="visibility-toggle" 
                            onClick={passwordInput.toggleVisibility}>
                                {passwordInput.visible ? <Eye className="visibility-icon" /> : <EyeOff className="visibility-icon" />}
                            </button>
                        </div>

                        <label htmlFor="confirm-password">Confirm Password</label>
                        <div className="input-wrapper">
                            <Lock className="input-icon" />
                            <input 
                            type={confirmPasswordInput.visible ? "text" : "password"} 
                            id="confirm-password" placeholder="must match the password above" 
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            className="auth-input" />
                            <button 
                            type="button" 
                            className="visibility-toggle" 
                            onClick={confirmPasswordInput.toggleVisibility}>
                                {confirmPasswordInput.visible ? <Eye className="visibility-icon" /> : <EyeOff className="visibility-icon" />}
                            </button>
                        </div>
                    </div>
                    
                    <button 
                    className="input-button" 
                    disabled={!userName.trim() || !email.trim() || !password.trim() || !confirmPassword.trim()}>
                        Sign up
                    </button>                
                </form>
                <p>Already have an account? <Link to="/login">Sign in</Link></p>
            </AuthenticationTransition>
        </div>
    );
}

export default Register;