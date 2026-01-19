
function Input({ type = 'text', placeholder, name, value, onChange, required, disabled }) {
    return <input
        type={type}
        placeholder={placeholder}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        disabled={disabled}
    />;
}

export default Input;
