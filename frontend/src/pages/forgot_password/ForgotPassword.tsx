import './forgotPassword.css'
import background_rpg from '../../assets/background-rpg-vertical.svg'
import { ChevronLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import AuthenticationTransition from '../../components/AuthenticationTransition'
import OtpInput from '../../components/OtpInput';

function ForgotPassword() {
    const navigate = useNavigate();
    const [isCodeSent, setIsCodeSent] = useState(false);
    const [resendTimer, setResendTimer] = useState(0);
    const [email, setEmail] = useState('');
    const [sentEmail, setSentEmail] = useState('');
    const [code, setCode] = useState('');

    function handleSendCode(e: React.FormEvent) {
        e.preventDefault();

        if (resendTimer > 0) return;

        setSentEmail(email);
        setIsCodeSent(true);

        const resendAvailableAt = Date.now() + 60_000;

        localStorage.setItem(
            'resendAvailableAt',
            String(resendAvailableAt)
        );
        
        setResendTimer(60);
    }

    // Guarda o timer em caso de saída do site
    useEffect(() => {
        const savedTime = localStorage.getItem('resendAvailableAt');

        if (!savedTime) return;

        const remaining = Math.ceil(
            (Number(savedTime) - Date.now()) / 1000
        );

        if (remaining > 0) {
            setResendTimer(remaining);
            setIsCodeSent(true);
        } else {
            localStorage.removeItem('resendAvailableAt');
        }
    }, []);

    // Cuida do timer
    useEffect(() => {
        if(resendTimer <= 0) return;

        const timer = setInterval(() => {
            setResendTimer((prev) => prev - 1);
        },1000);

        return () => clearInterval(timer);
    },[resendTimer]);

    return (
        <div className="forgot-container">
            <img src={background_rpg} alt="RPG characters" className="background-image" />
            <AuthenticationTransition className='forgot-content'>
                <button className="return-button" type='button' onClick={() => navigate('/login')}><ChevronLeft /></button>
                <h1>Password recovery</h1>
                <span>
                    {isCodeSent ? `A 6-digit verification code has been sent to ${sentEmail}.` : 'Enter your registered email to receive the verification code.'}
                </span>
                <form className='email-wrapper' onSubmit={handleSendCode}>
                    <input type='email' 
                    placeholder='you@example.com' 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)}/>
                    <button 
                    className="send-button" 
                    type="submit" 
                    disabled={!email.trim() || resendTimer > 0}>
                        {isCodeSent ? resendTimer > 0 ? `Resend (${resendTimer})` : 'Resend' : 'Send'}
                    </button>
                </form>
                <form>
                    {isCodeSent && <OtpInput code={code} setCode={setCode}/>}
                    <button className="input-button" type="submit" disabled={!isCodeSent || code.length !== 6}>Continue</button>
                </form>
            </AuthenticationTransition>
        </div>
    )
}

export default ForgotPassword;