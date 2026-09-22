import { type ReactNode } from 'react';
import { motion } from 'framer-motion';

const pageVariants = {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 }
};

interface PageTransitionProps {
    children: ReactNode;
}

function PageTransition({ children }: PageTransitionProps) {
    return (
        <motion.div
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={{ duration: 0.15, ease: 'easeOut' }}
            style={{ width: '100%', minHeight: '100vh' }}
        >
            {children}
        </motion.div>
    );
}

export default PageTransition;