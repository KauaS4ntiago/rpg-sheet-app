import {useState, useEffect} from 'react'
import '../../styles/auth.css'
import logo from '../../assets/logo.svg'
import {Link} from 'react-router-dom'
import { useNavigate } from 'react-router-dom'

function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate()

    const [emailError, setEmailError] = useState('')
    const [passwordError, setPasswordError] = useState('')
    const [nullError, setNullError] = useState('')
    const [generalError, setGeneralError] = useState('')

    function isValidEmail(email: string) {
    return email.includes('@') && email.split('@')[1]?.includes('.')
    }

    useEffect(() => {

    if (email && !isValidEmail(email)) {
        setEmailError('E-mail inválido')
    }
    else setEmailError('')

    }, [email])

    function handleLogin() {
        setPasswordError('')
        setNullError('')
        setGeneralError('')

        let hasError = false

        if (!email.trim() || !password.trim()) {
            setNullError('Preencha todos os campos')
            return
        }

        if (password.length < 8) {
            setPasswordError('A senha deve possuir pelo menos 8 caracteres')
            return
        }

        if (emailError) {
            hasError = true
        }

        if (hasError) return

        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email.trim(),
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
        .catch(() => {
            setGeneralError('Não foi possível realizar o login.')
        })
    }

    return (
        <div className='auth-container'>
            <img className="auth-img" src={logo} alt="RpG Logo"/>
            <div className='auth-card'>
                <h1>Log-in</h1>
                <label htmlFor="email">E-mail</label>
                <input className="auth-input" id="email" type="text" placeholder='Digite seu e-mail' value={email} onChange={e => {setEmail(e.target.value)}}/>
                    {emailError && <p className="auth-error-email">{emailError}</p>}
                <label htmlFor="password">Senha</label>
                <input className="auth-input" id="password" placeholder='Digite sua senha' type="password" value={password} onChange={e => {setPassword(e.target.value)}}/>
                <p>Esqueceu sua senha? <a href="">clique aqui</a></p>
                <button className="auth-button" onClick={() => handleLogin()}>Entrar</button> 
                    {passwordError && <p className="auth-error">{passwordError}</p>}
                    {nullError && <p className="auth-error">{nullError}</p>}
                    {generalError && <p className="auth-error">{generalError}</p>}
            </div>
            <p>Ainda não possui uma conta? <Link to="/register">clique aqui</Link></p>
        </div>
    )
}

export default Login