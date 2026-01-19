import React from "react";
import {
  PARCA_LISTESI_KODLU,
  ISLEM_TURU_DEGISEN,
  ISLEM_TURU_ONARIM,
  ONARIM_SEVIYELERI,
  BOYA_SEVIYELERI,
} from "../constants/partOptions";

export function ParcaSecimRow({
  value,
  onChange,
  isOnarim,
  onRemove,
  aracKodu,
}) {
  // value: { parca, islemTuru, seviye }
  // Filtreli parça listesi (aracKodu ile başlıyorsa)
  const filteredParts = aracKodu
    ? PARCA_LISTESI_KODLU.filter((p) => p.kod.startsWith(aracKodu))
    : PARCA_LISTESI_KODLU;

  return (
    <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
      <select
        value={value.parca || ""}
        onChange={(e) => onChange({ ...value, parca: e.target.value })}
        required
        style={{
          padding: '8px 12px',
          borderRadius: 8,
          border: '1px solid #feb47b',
          fontSize: 16,
          minWidth: 180,
          background: '#fff',
        }}
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
        onChange={(e) => onChange({ ...value, islemTuru: e.target.value, seviye: "" })}
        required
        style={{
          padding: '8px 12px',
          borderRadius: 8,
          border: '1px solid #feb47b',
          fontSize: 16,
          minWidth: 140,
          background: '#fff',
        }}
      >
        <option value="">İşlem Türü</option>
        {(isOnarim ? ISLEM_TURU_ONARIM : ISLEM_TURU_DEGISEN).map((it) => (
          <option key={it.value} value={it.value}>
            {it.label}
          </option>
        ))}
      </select>
      {/* Seviye seçimi */}
      {isOnarim && value.islemTuru === "onarim" && (
        <select
          value={value.seviye || ""}
          onChange={(e) => onChange({ ...value, seviye: e.target.value })}
          required
          style={{
            padding: '8px 12px',
            borderRadius: 8,
            border: '1px solid #feb47b',
            fontSize: 16,
            minWidth: 100,
            background: '#fff',
          }}
        >
          <option value="">Seviye</option>
          {ONARIM_SEVIYELERI.map((s) => (
            <option key={s.value} value={s.value}>
              {s.label}
            </option>
          ))}
        </select>
      )}
      {isOnarim && value.islemTuru === "boya" && (
        <select
          value={value.seviye || ""}
          onChange={(e) => onChange({ ...value, seviye: e.target.value })}
          required
          style={{
            padding: '8px 12px',
            borderRadius: 8,
            border: '1px solid #feb47b',
            fontSize: 16,
            minWidth: 100,
            background: '#fff',
          }}
        >
          <option value="">Boya Türü</option>
          {BOYA_SEVIYELERI.map((s) => (
            <option key={s.value} value={s.value}>
              {s.label}
            </option>
          ))}
        </select>
      )}
      {onRemove && (
        <button type="button" onClick={onRemove} style={{ color: "red" }}>
          Sil
        </button>
      )}
    </div>
  );
}
