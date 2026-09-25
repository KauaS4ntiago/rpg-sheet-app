import './Notification.css'
import { CircleX, TriangleAlert, CircleCheck, Info } from 'lucide-react';

interface NotificationProps{
    type: 'error' | 'success' | 'warning' | 'info';
    message: string;
    onClose: () => void;
}

function Notification({type, message, onClose}: NotificationProps) {

const icons = {
    error: CircleX,
    warning: TriangleAlert,
    success: CircleCheck,
    info: Info
};
const Icon = icons[type];

    return (
        <div  className={`notification ${type}`}>
                <Icon/>
                <span>{message}</span>
            <button onClick={onClose}>×</button>
        </div>
    );
}

export default Notification;