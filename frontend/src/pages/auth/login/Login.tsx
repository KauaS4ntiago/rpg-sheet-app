import '../auth.css'
import background_rpg from '../../../assets/background-rpg-vertical.svg'
import { Link } from 'react-router-dom'
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { usePasswordVisibility } from '../../../hooks/usePasswordVisibility';
import AuthenticationTransition from '../../../components/AuthenticationTransition';
import { useState } from 'react';

function Login() {
    const passwordInput = usePasswordVisibility();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    return (
        <div className="auth-container">
            <img src={background_rpg} alt="RPG characters" className="auth-image" />
            <AuthenticationTransition className="auth-content">
                <h1>Login</h1>
                <form>
                    <div className="input-container">
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
                            id="password" 
                            placeholder="must have at least 8 characters" 
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="auth-input" />
                            <button type="button" className="visibility-toggle" onClick={passwordInput.toggleVisibility}>
                                {passwordInput.visible ? <Eye className="visibility-icon" /> : <EyeOff className="visibility-icon" />}
                            </button>
                        </div>
                        <Link to="/forgot-password">forgot password?</Link>
                    </div>
                    
                    <button 
                    className="input-button" 
                    disabled={!email.trim() || !password.trim()}>
                        Sign in
                    </button>                
                </form>
                <p>Don't have an account? <Link to="/register">Sign up</Link></p>
            </AuthenticationTransition>
        </div>
    );
}

export default Login;