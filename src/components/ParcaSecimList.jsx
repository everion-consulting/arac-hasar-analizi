import React from "react";
import { ParcaSecimRow } from "./ParcaSecimRow";
import "../styles/parcaSecim.css";

// aracKodu: "A", "B", ...
export function ParcaSecimList({ value, onChange, isOnarim, label, aracKodu }) {
  // value: array of { parca, islemTuru }
  const handleRowChange = (idx, row) => {
    const newArr = value.slice();
    newArr[idx] = row;
    onChange(newArr);
  };
  const handleAdd = () => {
    onChange([...value, { parca: "", islemTuru: "" }]);
  };
  const handleRemove = (idx) => {
    const newArr = value.slice();
    newArr.splice(idx, 1);
    onChange(newArr);
  };
  return (
    <div className="parca-secim-list">
      <label>{label}</label>
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
        className="btn-add-part"
        onClick={handleAdd}
        disabled={!aracKodu}
      >
        + Parça Ekle
      </button>
    </div>
  );
}
