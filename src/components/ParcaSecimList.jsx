import React from "react";
import { ParcaSecimRow } from "./ParcaSecimRow";

// aracKodu: "A", "B", ...
export function ParcaSecimList({ value, onChange, isOnarim, label, aracKodu }) {
  // value: array of { parca, islemTuru, seviye }
  const handleRowChange = (idx, row) => {
    const newArr = value.slice();
    newArr[idx] = row;
    onChange(newArr);
  };
  const handleAdd = () => {
    onChange([...value, { parca: "", islemTuru: "", seviye: "" }]);
  };
  const handleRemove = (idx) => {
    const newArr = value.slice();
    newArr.splice(idx, 1);
    onChange(newArr);
  };
  return (
    <div>
      <label style={{ fontWeight: 600 }}>{label}</label>
      {value.map((row, idx) => (
        <ParcaSecimRow
          key={idx}
          value={row}
          onChange={(rowVal) => handleRowChange(idx, rowVal)}
          isOnarim={isOnarim}
          onRemove={() => handleRemove(idx)}
          aracKodu={aracKodu}
        />
      ))}
      <button
        type="button"
        onClick={handleAdd}
        style={{
          marginTop: 8,
          padding: '10px 24px',
          borderRadius: 8,
          background: aracKodu ? 'linear-gradient(90deg, #ff7e5f, #feb47b)' : '#eee',
          color: aracKodu ? '#fff' : '#aaa',
          fontWeight: 600,
          fontSize: 18,
          border: 'none',
          cursor: aracKodu ? 'pointer' : 'not-allowed',
          boxShadow: aracKodu ? '0 2px 8px #feb47b44' : 'none',
          transition: 'all 0.2s',
        }}
        disabled={!aracKodu}
      >
        + Parça Ekle
      </button>
    </div>
  );
}
