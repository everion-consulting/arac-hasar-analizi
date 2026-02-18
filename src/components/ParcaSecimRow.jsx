import React from "react";
import {
  PARCA_LISTESI_KODLU,
  ISLEM_TURU_DEGISEN,
  ISLEM_TURU_ONARIM,
} from "../constants/partOptions";
import "../styles/parcaSecim.css";

export function ParcaSecimRow({
  value,
  onChange,
  isOnarim,
  onRemove,
  aracKodu,
}) {
  // value: { parca, islemTuru }
  // Filtreli parça listesi (aracKodu ile başlıyorsa)
  const filteredParts = aracKodu
    ? PARCA_LISTESI_KODLU.filter((p) => p.kod.startsWith(aracKodu))
    : PARCA_LISTESI_KODLU;

  return (
    <div className="parca-secim-row">
      <select
        value={value.parca || ""}
        onChange={(e) => onChange({ ...value, parca: e.target.value })}
        required
      >
        <option value="">Parça Seçiniz</option>
        {filteredParts.map((p) => (
          <option key={p.kod} value={p.kod}>
            {p.kod + " - " + p.ad}
          </option>
        ))}
      </select>
      <select
        value={value.islemTuru || ""}
        onChange={(e) => onChange({ ...value, islemTuru: e.target.value })}
        required
      >
        <option value="">İşlem Türü</option>
        {(isOnarim ? ISLEM_TURU_ONARIM : ISLEM_TURU_DEGISEN).map((it) => (
          <option key={it.value} value={it.value}>
            {it.label}
          </option>
        ))}
      </select>
      {onRemove && (
        <button type="button" className="btn-remove" onClick={onRemove}>
          Sil
        </button>
      )}
    </div>
  );
}
