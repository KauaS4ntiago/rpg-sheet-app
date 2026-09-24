import './forgotPassword.css'
import background_rpg from '../../assets/background-rpg-vertical.svg'
import { ChevronLeft } from 'lucide-react';
import {useNavigate } from 'react-router-dom';
import { useState, useRef } from 'react';

function ForgotPassword() {
    const navigate = useNavigate();
    const [code, setCode] = useState('');
    const codeLength = 6;
    const inputRefs = useRef<HTMLInputElement[]>([]);

    function inputFocus( index:number ) {
        inputRefs.current[index].focus();
    }

    return (
        <div className="forgot-container">
            <img src={background_rpg} alt="RPG characters" className="background-image" />
            <div className='forgot-content'>
                <button className="return-button" type='button' onClick={() => navigate(-1)}><ChevronLeft/></button>
                <h1>Password recovery</h1>
                <span>Enter your registered email to receive the verification code.</span>
                <form>
                    <div className='email-wrapper'>
                        <input type='text' placeholder='you@example.com'/>
                        <button className="resend-button"type="button">Send</button>
                    </div>
                    <div className='otp-container'>
                        { Array.from({ length: codeLength }).map((_, index) => (
                            <input
                                key={ index }
                                type='text'
                                inputMode='numeric'
                                maxLength={1}
                                ref={ (el) => {inputRefs.current[index] = el! } }
                                value={code[index] || ''}
                                // Falta alterações
                                onKeyDown={(e) => {
                                    const key = e.key;
                                    if( key === 'Backspace' && index < codeLength - 1) {
                                        inputFocus( index - 1 );
                                    }
                                }}
                                onChange={(e) => {
                                    const newChar = e.target.value.slice(-1);
                                    const before = code.slice(0, index);
                                    const after = code.slice(index + 1);
                                    setCode(before + newChar + after);
                                    if ( newChar === '') {
                                        return;
                                    }
                                    if (index < codeLength - 1) {
                                        inputFocus( index + 1 );
                                    }
                                }}
                            />
                        )) }
                    </div>
                    <button className="input-button" type="submit">Continue</button>
                </form>
            </div>
        </div>
    )
}

export default ForgotPassword;