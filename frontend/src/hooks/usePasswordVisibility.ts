import { useState } from 'react';

function usePasswordVisibility() {
    const [visible, setVisible] = useState(false);

    // Toggle the visibility of the password input field
    const toggleVisibility = () => {
        setVisible(!visible);
    };

    return { visible, toggleVisibility };
}

export { usePasswordVisibility };