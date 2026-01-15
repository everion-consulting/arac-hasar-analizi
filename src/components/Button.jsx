function Button({ children, onClick, variant = 'primary' }) {
    return (
        <button className={`${variant}-btn`} onClick={onClick}>
            {children}
        </button>
    );
}

export default Button;
