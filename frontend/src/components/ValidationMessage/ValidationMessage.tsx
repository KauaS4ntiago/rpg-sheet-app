import { TriangleAlert } from 'lucide-react';
import './ValidationMessage.css';

interface ValidationMessageProps {
    message: string;
}

function ValidationMessage({ message }: ValidationMessageProps) {
    if (!message) return null;

    return (
        <div className="validation-message">
            <TriangleAlert />

            <span>
                {message}
            </span>
        </div>
    );
}

export default ValidationMessage;