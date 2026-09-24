import { useRef } from 'react';

interface OtpInputProps {
    code: String;
    setCode: React.Dispatch<React.SetStateAction<string>>
}

function OtpInput({ code, setCode}: OtpInputProps) {

    const codeLength = 6;
    const inputRefs = useRef<HTMLInputElement[]>([]);

    function inputFocus(index: number) {
        inputRefs.current[index].focus();
    }

    return (
        <div className='otp-container'>
            {Array.from({ length: codeLength }).map((_, index) => (
                <input
                    key={index}
                    type='text'
                    inputMode='numeric'
                    maxLength={1}
                    ref={(el) => { inputRefs.current[index] = el! }}
                    value={code[index] || ''}
                    onKeyDown={(e) => {
                        const key = e.key;
                        if (key === 'Backspace' && !code[index] && index > 0) {
                            inputFocus(index - 1);
                        }
                    }}
                    onChange={(e) => {
                        const newChar = e.target.value.slice(-1);
                        const before = code.slice(0, index);
                        const after = code.slice(index + 1);
                        setCode(before + newChar + after);
                        if (newChar === '') {
                            return;
                        }
                        if (index < codeLength - 1) {
                            inputFocus(index + 1);
                        }
                    }}
                    onPaste={(e) => {
                        e.preventDefault();
                        const pastedText = e.clipboardData.getData('text');
                        const trimmedText = pastedText.slice(0, codeLength);
                        setCode(trimmedText);
                        if (trimmedText.length === codeLength) {
                            inputFocus(trimmedText.length - 1);
                        } else {
                            inputFocus(trimmedText.length);
                        }
                    }}
                />
            ))}
        </div>
    )
}

export default OtpInput;