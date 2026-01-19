import React from 'react';

export default function SearchableSelect({ options, value, onChange, placeholder = '', disabled = false, style = {}, optionLabel = x => x, optionValue = x => x, ...rest }) {
    const [search, setSearch] = React.useState('');
    const filtered = options.filter(opt => optionLabel(opt).toLowerCase().includes(search.toLowerCase()));
    return (
        <div style={{ position: 'relative', width: '100%' }}>
            <input
                type="text"
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder={placeholder}
                disabled={disabled}
                style={{
                    width: '100%',
                    padding: '12px 18px',
                    borderRadius: 10,
                    border: '1.5px solid #feb47b',
                    fontSize: 16,
                    marginBottom: 4,
                    boxShadow: '0 2px 8px #feb47b22',
                    color: '#222',
                    fontWeight: 500,
                    outline: 'none',
                    background: disabled ? '#f5f5f5' : '#fff',
                    ...style
                }}
            />
            <select
                value={value}
                onChange={onChange}
                disabled={disabled}
                style={{
                    width: '100%',
                    padding: '14px 18px',
                    borderRadius: 10,
                    border: '1.5px solid #feb47b',
                    fontSize: 18,
                    background: disabled ? '#f5f5f5' : '#fff',
                    boxShadow: '0 2px 8px #feb47b22',
                    color: value ? '#222' : '#aaa',
                    fontWeight: 500,
                    outline: 'none',
                    transition: 'border 0.2s',
                }}
                {...rest}
            >
                <option value="">{placeholder}</option>
                {filtered.map((opt, idx) => (
                    <option key={idx} value={optionValue(opt)}>{optionLabel(opt)}</option>
                ))}
            </select>
        </div>
    );
}
