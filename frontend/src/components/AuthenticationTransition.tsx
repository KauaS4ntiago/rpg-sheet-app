import { type ReactNode } from 'react';
import { motion } from 'framer-motion';

const authenticationVariants = {
    initial: { 
        y: '-100%',
        opacity: 0
    },
    animate: { 
        y: '0%',
        opacity: 1 
    },
    exit: { 
        y: '100%',
        opacity: 0 
    }
};

interface AuthenticationTransitionProps {
    children: ReactNode;
    className?: string;
}

function AuthenticationTransition({ children, className }: AuthenticationTransitionProps) {
    return (
        <motion.div
            variants={authenticationVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={{ duration: 0.4, ease: 'easeOut' }}
            className={ className }
            style={{ width: '100%', minHeight: '100%' }}
        >
            {children}
        </motion.div>
    );
}

export default AuthenticationTransition;