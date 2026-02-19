import React from "react";
import Select from "react-select";
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

  // react-select için options hazırla
  const parcaOptions = filteredParts.map((p) => ({
    label: p.kod + " - " + p.ad,
    value: p.kod,
  }));

  const islemTuruOptions = (isOnarim ? ISLEM_TURU_ONARIM : ISLEM_TURU_DEGISEN).map((it) => ({
    label: it.label,
    value: it.value,
  }));

  // Seçili değerleri bul
  const selectedParca = parcaOptions.find((opt) => opt.value === value.parca) || null;
  const selectedIslem = islemTuruOptions.find((opt) => opt.value === value.islemTuru) || null;

  return (
    <div className="parca-secim-row">
      <Select
        options={parcaOptions}
        value={selectedParca}
        onChange={(opt) => onChange({ ...value, parca: opt ? opt.value : "" })}
        placeholder="Parça Seçiniz"
        isClearable
        menuPortalTarget={document.body}
        styles={{
          control: (base) => ({
            ...base,
            minHeight: 44,
            fontSize: 14,
            borderRadius: 10,
            borderColor: "#feb47b",
            boxShadow: "0 2px 8px #feb47b22",
            minWidth: "280px",
            flex: 2,
          }),
          option: (base, state) => ({
            ...base,
            fontSize: 14,
            padding: "10px 14px",
            color: state.isSelected ? "#fff" : "#222",
          }),
          menu: (base) => ({
            ...base,
            zIndex: 9999,
          }),
          menuList: (base) => ({
            ...base,
            maxHeight: "300px",
          }),
          menuPortal: (base) => ({
            ...base,
            zIndex: 9999,
          }),
        }}
      />
      <Select
        options={islemTuruOptions}
        value={selectedIslem}
        onChange={(opt) => onChange({ ...value, islemTuru: opt ? opt.value : "" })}
        placeholder="İşlem Türü"
        isClearable
        menuPortalTarget={document.body}
        styles={{
          control: (base) => ({
            ...base,
            minHeight: 44,
            fontSize: 14,
            borderRadius: 10,
            borderColor: "#feb47b",
            boxShadow: "0 2px 8px #feb47b22",
            minWidth: "200px",
            flex: 1,
          }),
          option: (base, state) => ({
            ...base,
            fontSize: 14,
            padding: "10px 14px",
            color: state.isSelected ? "#fff" : "#222",
          }),
          menu: (base) => ({
            ...base,
            zIndex: 9999,
          }),
          menuList: (base) => ({
            ...base,
            maxHeight: "300px",
          }),
          menuPortal: (base) => ({
            ...base,
            zIndex: 9999,
          }),
        }}
      />
      {onRemove && (
        <button type="button" className="btn-remove" onClick={onRemove}>
          Sil
        </button>
      )}
    </div>
  );
}
