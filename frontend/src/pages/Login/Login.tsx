import {useState} from 'react'
import '../../styles/auth.css'
import logo from '../../assets/logo.svg'
import {Link} from 'react-router-dom'
import { useNavigate } from 'react-router-dom'

function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate()

    function handleLogin() {
        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if(data.token) {
                localStorage.setItem('token', data.token)
                localStorage.setItem('user_id', data.user_id)
                navigate('/dashboard')
            } else {
                alert(data.error)
            }
        })
    }

    return (
        <div className='auth-container'>
            <img className="auth-img" src={logo} alt="RpG Logo"/>
            <div className='auth-card'>
                <h1>Log-in</h1>
                <label htmlFor="email">E-mail</label>
                <input className="auth-input" id="email" type="text" placeholder='Digite seu e-mail' value={email} onChange={e => {setEmail(e.target.value)}}/>
                <label htmlFor="password">Senha</label>
                <input className="auth-input" id="password" placeholder='Digite sua senha' type="password" value={password} onChange={e => {setPassword(e.target.value)}}/>
                <p>Esqueceu sua senha? <a href="">clique aqui</a></p>
                <button className="auth-button" onClick={() => handleLogin()}>Entrar</button> 
            </div>
            <p>Ainda não possui uma conta? <Link to="/register">clique aqui</Link></p>
        </div>
    )
}

export default Login