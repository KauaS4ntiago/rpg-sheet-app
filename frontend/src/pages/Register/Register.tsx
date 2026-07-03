import { useState} from 'react'
import '../../styles/auth.css'
import logo from '../../assets/logo.svg'
import { Link, useNavigate } from 'react-router-dom'

function Register() {
    const [email, setEmail] = useState('')
    const [userName, setUserName] = useState('')
    const [password, setPassword] = useState('')
    const [repPassword, setRepPassword] = useState('')

    const [emailError, setEmailError] = useState('') 
    const [passwordError, setPasswordError] = useState('') 
    const [generalError, setGeneralError] = useState('') 
    const [nullError, setNullError] = useState('')

    const navigate = useNavigate()

    function isValidEmail(email: string) {
        return email.includes('@') && email.split('@')[1]?.includes('.')
    }

    function handleRegister() {
        setEmailError('')
        setPasswordError('')
        setGeneralError('')
        setNullError('')

        let hasError = false

        if (
            !userName.trim() ||
            !email.trim() ||
            !password.trim() ||
            !repPassword.trim()
        ) {
            setNullError('Preencha todos os campos')
            hasError = true
        }

        if (!isValidEmail(email)) {
            setEmailError('E-mail inválido')
            hasError = true
        }

        if (password.length < 8) {
            setPasswordError('A senha deve possuir pelo menos 8 caracteres')
            hasError = true
        } 
        else if (password !== repPassword) {
            setPasswordError('Senhas não coincidem')
            hasError = true
        }

        if (hasError) return

        fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: userName,
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                localStorage.setItem('token', data.token)
                localStorage.setItem('user_id', data.user_id)
                navigate('/dashboard')
            } else {
                setGeneralError(data.error)
            }
        })
        .catch(() => setGeneralError('Não foi possível concluir o cadastro.'))
    }

    return (
        <div className='auth-container'>
            <img className="auth-img" src={logo} alt="RpG Logo"/>
            <div className='auth-card'>
                <h1>Cadastro</h1>
                <label htmlFor="username">Nome de Usuário</label>
                <input className="auth-input" id="username" type="text" placeholder='Digite seu nome de usuário' value={userName} onChange={e => setUserName(e.target.value)}/>

                <label htmlFor="email">E-mail</label>
                <input className="auth-input" id="email" type="text" placeholder='Digite seu e-mail' value={email} onChange={e => setEmail(e.target.value)}/>
                    {emailError && <p className="auth-error-email">{emailError}</p>}

                <label htmlFor="password">Senha</label>
                <input className="auth-input" id="password" placeholder='Digite sua senha' type="password" value={password} onChange={e => setPassword(e.target.value)}/>
                <input className="auth-input" id="repPassword" placeholder='Digite novamente sua senha' type="password" value={repPassword} onChange={e => setRepPassword(e.target.value)}/>

                <button className="auth-button" onClick={handleRegister}>Cadastrar</button>
                    {passwordError && <p className="auth-error">{passwordError}</p>}
                    {generalError && <p className="auth-error">{generalError}</p>}
                    {nullError && <p className="auth-error">{nullError}</p>}
            </div>
            <p>Já possui uma conta? <Link to='/'>clique aqui</Link></p>
        </div>
    )
}

export default Register;