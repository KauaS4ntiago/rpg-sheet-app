import { type ReactNode } from 'react';
import { motion, type MotionStyle } from 'framer-motion';

const pageVariants = {
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

interface VerticalTransitionProps {
    children: ReactNode;
    className?: string;
    style?: MotionStyle; /* Usa o tipo oficial do framer-motion */
}

function VerticalTransition({ children, className, style }: VerticalTransitionProps) {
    return (
        <motion.div
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={{ duration: 0.4, ease: 'easeOut' }}
            className={className}
            style={{ height: '100%', ...style }}
        >
            {children}
        </motion.div>
    );
}

export default VerticalTransition;