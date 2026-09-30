import './Profile.css';

import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

import { Mail, User, ChevronLeft, Camera } from 'lucide-react';

import ValidationMessage from '../../components/ValidationMessage/ValidationMessage';
import { useNotification } from '../../contexts/NotificationContext';

interface ProfileProps {
    username: string;
    email: string;
    photoUrl: string;
}

function Profile({ username, email, photoUrl }: ProfileProps) {

    const [isOpen, setIsOpen] = useState(false);
    const Navigate = useNavigate();

    const [formData, setFormData] = useState({
        name: username,
        email: email
    });

    const [selectedPhoto, setSelectedPhoto] = useState<File | null>(null);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);

    const [errors, setErrors] = useState({
        name: '',
        email: ''
    });

    const { showError, showSuccess } = useNotification();

    const fileInputRef = useRef<HTMLInputElement>(null);

    function validateFields(name: string, value: string) {
        switch (name) {
            case 'name':
                if (!value.trim()) {
                    return 'Nome de usuário é obrigatório.';
                }
                break;

            case 'email':
                if (!value.includes('@') || !value.includes('.')) {
                    return 'Email inválido.';
                }
                break;

            default:
                break;
        }

        return '';
    }

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        const { name, value } = e.target;

        setFormData({
            ...formData,
            [name]: value
        });

        const error = validateFields(name, value);

        setErrors(prevErrors => ({
            ...prevErrors,
            [name]: error
        }));
    }

    function handlePhotoChange(e: React.ChangeEvent<HTMLInputElement>) {
        const file = e.target.files?.[0];

        if (file) {
            setSelectedPhoto(file);
            setPreviewUrl(URL.createObjectURL(file));
        }
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
            const response = await fetch(
                'http://127.0.0.1:5000/users',
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: formData.name,
                        email: formData.email
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                showError(data.error);
                return;
            }

            showSuccess(data.message);

        } catch (error) {
            showError(
                'Não foi possível conectar ao servidor, tente novamente mais tarde.'
            );
        }
    }

    return (
        <div className="profile-container">

            {isOpen ? (

                <div
                    className="profile-overlay"
                    onClick={() => setIsOpen(false)}
                >

                    <div
                        className="profile-card-wrapper"
                        onClick={(e) => e.stopPropagation()}
                    >

                        <div className="profile-card">

                            <div className="profile-card-content">

                                <div
                                    className="photo-wrapper"
                                    onClick={() => fileInputRef.current?.click()}
                                >

                                    <img
                                        src={previewUrl ? previewUrl : photoUrl}
                                        alt={formData.name}
                                    />

                                    <div className="photo-overlay">
                                        <Camera size={50} />
                                    </div>

                                    <input
                                        type="file"
                                        ref={fileInputRef}
                                        onChange={handlePhotoChange}
                                        style={{ display: 'none' }}
                                        accept="image/*"
                                    />

                                </div>

                                <div className="input-container">

                                    <form onSubmit={handleSubmit}>

                                        {/* USERNAME */}
                                        <div className="input-group">

                                            <label htmlFor="username">
                                                Username
                                            </label>

                                            <div className="input-wrapper">

                                                <User className="input-icon" />

                                                <input
                                                    type="text"
                                                    id="username"
                                                    name="name"
                                                    placeholder={username}
                                                    value={formData.name}
                                                    onChange={handleChange}
                                                    className="profile-input"
                                                />

                                                <ValidationMessage
                                                    message={errors.name}
                                                />

                                            </div>

                                        </div>

                                        {/* EMAIL */}
                                        <div className="input-group">

                                            <label htmlFor="email">
                                                Email
                                            </label>

                                            <div className="input-wrapper">

                                                <Mail className="input-icon" />

                                                <input
                                                    type="email"
                                                    id="email"
                                                    name="email"
                                                    placeholder={email}
                                                    value={formData.email}
                                                    onChange={handleChange}
                                                    className="profile-input"
                                                />

                                                <ValidationMessage
                                                    message={errors.email}
                                                />

                                            </div>

                                        </div>

                                        {/* SAVE */}
                                        <button
                                            className="submit-button"
                                            type="submit"
                                            disabled={Object.values(errors).some(
                                                error => error !== ''
                                            )}
                                        >
                                            Save
                                        </button>

                                    </form>

                                    {/* RESET PASSWORD */}
                                    <button
                                        className="reset-password-button"
                                        type="button"
                                        onClick={() => Navigate('/reset-password')}
                                    >
                                        Reset password
                                    </button>

                                </div>

                            </div>

                            {/* CLOSE */}
                            <button
                                className="return-button"
                                onClick={() => setIsOpen(false)}
                            >
                                <ChevronLeft size={30} />
                            </button>

                        </div>

                    </div>

                </div>

            ) : (

                <button
                    className="profile-button"
                    onClick={() => setIsOpen(true)}
                >

                    <img
                        src={photoUrl}
                        alt={formData.name}
                    />

                    <h2>{formData.name}</h2>

                </button>

            )}

        </div>
    );
}

export default Profile;