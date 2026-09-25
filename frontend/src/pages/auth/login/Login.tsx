import '../auth.css'
import background_rpg from '../../../assets/background-rpg-vertical.svg'
import { Link } from 'react-router-dom'
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { usePasswordVisibility } from '../../../hooks/usePasswordVisibility';
import AuthenticationTransition from '../../../components/AuthenticationTransition';
import ValidationMessage from '../../../components/ValidationMessage/ValidationMessage';
import { useNotification } from '../../../contexts/NotificationContext';
import { useState } from 'react';

function Login() {
    const passwordInput = usePasswordVisibility();
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [errors, setErrors] = useState({ email: '', password: '' });
    const { showError, showSuccess } = useNotification();

    function validateFields(name: string, value: string) {
        switch (name) {
            case 'email':
                if (!value.includes('@') || !value.includes('.')) return "Email inválido.";
                break;
            case 'password':
                if (value.length < 8) return "A senha deve ter pelo menos 8 caracteres.";
                break;
            default:
                break;
        }
        return '';
    }

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        const { name, value } = e.target;

        setFormData(prevFormData => ({
            ...prevFormData,
            [name]: value
        }));

        const error = validateFields(name, value);

        setErrors(prevErrors => ({
            ...prevErrors,
            [name]: error
        }));
    }

    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();

        const hasErrors = Object.values(errors).some(
            error => error !== ''
        );

        if (hasErrors) {
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'email': formData.email,
                    'password': formData.password
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                showError(data.error);
                return;
            }

            showSuccess(data.message);

        } catch (error) {
            showError('Não foi possível conectar ao servidor, tente novamente mais tarde.');
        }
    }

    return (
        <div className="auth-container">
            <img src={background_rpg} alt="RPG characters" className="auth-image" />
            <AuthenticationTransition className="auth-content">
                <h1>Login</h1>
                <form onSubmit={handleSubmit}>
                    <div className="input-container">
                        <label htmlFor="email">Email</label>
                        <div className="input-wrapper">
                            <Mail className="input-icon" />
                            <input
                                type="email"
                                name="email"
                                id="email"
                                placeholder="you@example.com"
                                value={formData.email}
                                onChange={handleChange}
                                className="auth-input" />
                            <ValidationMessage message={errors.email} />
                        </div>
                        <label htmlFor="password">Password</label>
                        <div className="input-wrapper">
                            <Lock className="input-icon" />
                            <input
                                type={passwordInput.visible ? "text" : "password"}
                                name="password"
                                id="password"
                                placeholder="must have at least 8 characters"
                                value={formData.password}
                                onChange={handleChange}
                                className="auth-input" />
                            <button type="button" className="visibility-toggle" onClick={passwordInput.toggleVisibility}>
                                {passwordInput.visible ? <Eye className="visibility-icon" /> : <EyeOff className="visibility-icon" />}
                            </button>
                            <ValidationMessage message={errors.password} />
                        </div>
                        <Link to="/forgot-password">forgot password?</Link>
                    </div>

                    <button
                        className="input-button"
                        disabled={!formData.email.trim() ||
                            !formData.password.trim() ||
                            Object.values(errors).some(error => error !== '')}>
                        Sign in
                    </button>
                </form>
                <p>Don't have an account? <Link to="/register">Sign up</Link></p>
            </AuthenticationTransition>
        </div>
    );
}

export default Login;