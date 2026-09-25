import '../auth.css'
import background_rpg from '../../../assets/background-rpg-vertical.svg'
import { Mail, Lock, User, Eye, EyeOff } from 'lucide-react';
import { Link } from 'react-router-dom'
import { usePasswordVisibility } from '../../../hooks/usePasswordVisibility';
import AuthenticationTransition from '../../../components/AuthenticationTransition';
import ValidationMessage from '../../../components/ValidationMessage/ValidationMessage';
import { useNotification } from '../../../contexts/NotificationContext';
import { useState } from 'react';

function Register() {
    const passwordInput = usePasswordVisibility();
    const confirmPasswordInput = usePasswordVisibility();
    const [formData, setFormData] = useState({ name: '', email: '', password: '', confirmPassword: '' });
    const [errors, setErrors] = useState({ name: '', email: '', password: '', confirmPassword: '' });
    const { showError, showSuccess } = useNotification();

    function validateFields(name: string, value: string) {
        switch (name) {
            case 'name':
                if (!value.trim()) return 'Nome de usuário é obrigatório.';
                break;
            case 'email':
                if (!value.includes('@') || !value.includes('.')) return 'Email inválido.';
                break;
            case 'password':
                if (value.length < 8) return "A senha deve ter pelo menos 8 caracteres.";
                break;
            case 'confirmPassword':
                if (value !== formData.password) return "Senhas não coincidem.";
                break;
            default:
                break;
        }
        return "";
    }

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        const { name, value } = e.target;

        setFormData({ ...formData, [e.target.name]: e.target.value })

        const error = validateFields(name, value);

        setErrors(prevErrors => {
            if (name === 'password') {
                return {
                    ...prevErrors,
                    password: error,
                    confirmPassword:
                        value !== formData.confirmPassword
                            ? 'Senhas não coincidem.'
                            : ''
                };
            }

            return {
                ...prevErrors,
                [name]: error
            };
        });
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
            const response = await fetch('http://127.0.0.1:5000/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: formData.name,
                    email: formData.email,
                    password: formData.password,
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
                <h1>Register</h1>
                <form onSubmit={handleSubmit}>
                    <div className="input-container">

                        <label htmlFor="username">Username</label>

                        <div className="input-wrapper">
                            <User className="input-icon" />

                            <input
                                type="text"
                                id="username"
                                name="name"
                                placeholder="your username"
                                value={formData.name}
                                onChange={handleChange}
                                className="auth-input"
                            />

                            <ValidationMessage message={errors.name} />
                        </div>


                        <label htmlFor="email">Email</label>

                        <div className="input-wrapper">
                            <Mail className="input-icon" />

                            <input
                                type="email"
                                id="email"
                                name="email"
                                placeholder="you@example.com"
                                value={formData.email}
                                onChange={handleChange}
                                className="auth-input"
                            />

                            <ValidationMessage message={errors.email} />
                        </div>


                        <label htmlFor="password">Password</label>

                        <div className="input-wrapper">
                            <Lock className="input-icon" />

                            <input
                                type={passwordInput.visible ? "text" : "password"}
                                id="password"
                                name="password"
                                placeholder="must have at least 8 characters"
                                value={formData.password}
                                onChange={handleChange}
                                className="auth-input"
                            />

                            <button
                                type="button"
                                className="visibility-toggle"
                                onClick={passwordInput.toggleVisibility}
                            >
                                {passwordInput.visible
                                    ? <Eye className="visibility-icon" />
                                    : <EyeOff className="visibility-icon" />
                                }
                            </button>

                            <ValidationMessage message={errors.password} />
                        </div>


                        <label htmlFor="confirm-password">Confirm Password</label>

                        <div className="input-wrapper">
                            <Lock className="input-icon" />

                            <input
                                type={confirmPasswordInput.visible ? "text" : "password"}
                                id="confirm-password"
                                name="confirmPassword"
                                placeholder="must match the password above"
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                className="auth-input"
                            />

                            <button
                                type="button"
                                className="visibility-toggle"
                                onClick={confirmPasswordInput.toggleVisibility}
                            >
                                {confirmPasswordInput.visible
                                    ? <Eye className="visibility-icon" />
                                    : <EyeOff className="visibility-icon" />
                                }
                            </button>

                            <ValidationMessage message={errors.confirmPassword} />
                        </div>

                    </div>

                    <button
                        className="input-button"
                        disabled={
                            !formData.name.trim() ||
                            !formData.email.trim() ||
                            !formData.password.trim() ||
                            !formData.confirmPassword.trim() ||
                            Object.values(errors).some(error => error !== '')
                        }>
                        Sign up
                    </button>
                </form>
                <p>Already have an account? <Link to="/login">Sign in</Link></p>
            </AuthenticationTransition>
        </div>
    );
}

export default Register;