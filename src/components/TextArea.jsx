
function TextArea({ placeholder, name, value, onChange }) {
    return <textarea
        placeholder={placeholder}
        name={name}
        value={value}
        onChange={onChange}
    ></textarea>;
}

export default TextArea;
