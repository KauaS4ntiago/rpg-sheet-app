import { createContext, useContext, useState } from 'react';
import Notification from '../components/Notification/Notification';

interface NotificationContextData {
    showError: (message: string) => void;
    showSuccess: (message: string) => void;
    showWarning: (message: string) => void;
    showInfo: (message: string) => void;
}

const NotificationContext = createContext<NotificationContextData | undefined>(undefined);

export function NotificationProvider({ children }: { children: React.ReactNode }) {
    const [notification, setNotification] = useState<{
        type: 'error' | 'success' | 'warning' | 'info';
        message: string;
    } | null>(null);

    function showError(message: string) {
        setNotification({
            type: 'error',
            message
        });
    }

    function showSuccess(message: string) {
        setNotification({
            type: 'success',
            message
        });
    }

    function showWarning(message: string) {
        setNotification({
            type: 'warning',
            message
        });
    }

    function showInfo(message: string) {
        setNotification({
            type: 'info',
            message
        });
    }

    return (
    <NotificationContext.Provider
        value={{
            showError,
            showSuccess,
            showWarning,
            showInfo
        }}
    >
        {children}

        {notification && (
            <Notification
                type={notification.type}
                message={notification.message}
                onClose={() => setNotification(null)}
            />
        )}
    </NotificationContext.Provider>
);
}

export function useNotification() {
    const context = useContext(NotificationContext);

    if (!context) {
        throw new Error(
            'useNotification must be used inside NotificationProvider'
        );
    }

    return context;
}