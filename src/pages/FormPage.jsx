import Input from '../components/Input';
import TextArea from '../components/TextArea';
import Button from '../components/Button';
import '../styles/formPage.css';

import { useState, useEffect } from 'react';
import { ParcaSecimList } from '../components/ParcaSecimList';
import { ARAC_TURU_LISTESI, MARKA_LISTESI, MODEL_LISTESI } from '../constants/partOptions';
import Select from 'react-select';
import { getCsrfToken } from '../utils/csrf';


function FormPage({ onNext, onLogout, onShowHistory, editData }) {
    const [form, setForm] = useState({
        rayicDeger: '',
        toplamHasar: '',
        marka: '', model: '', km: '', arac_yasi: ''
    });
    const [selectedMarka, setSelectedMarka] = useState('');
    const [selectedModel, setSelectedModel] = useState('');
    const [aracTuru, setAracTuru] = useState('Otomobil'); 
    const [onarilanList, setOnarilanList] = useState([]); 
    const [degisenList, setDegisenList] = useState([]); 
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // editData geldiğinde formu doldur
    useEffect(() => {
        if (editData) {
            console.log('EditData:', editData); // Debug için
            // Araç yaşından model yılını hesapla
            const mevcutYil = new Date().getFullYear();
            const modelYili = editData.arac_yasi ? mevcutYil - editData.arac_yasi : '';

            // Değişen parçaları map et (direkt format)
            const mapDegisenParcalar = (parcalar) => {
                if (!Array.isArray(parcalar)) return [];
                return parcalar.map(p => ({
                    parca: p.parca_kodu || p.parca || '',
                    islemTuru: p.islemTuru || '',
                }));
            };

            // Onarılan parçaları collapse et (backend'den expanded geliyor)
            // Backend: [{parca_kodu: "A.3", islemTuru: "onarim", seviye: "hafif"}, {parca_kodu: "A.3", islemTuru: "boya", seviye: "lokal"}]
            // Frontend: [{parca: "A.3", islemTuru: "hafif_lokal_boya"}]
            const mapOnarilanParcalar = (parcalar) => {
                if (!Array.isArray(parcalar)) return [];
                
                // Parçaları grupla
                const grouped = {};
                parcalar.forEach(p => {
                    const kod = p.parca_kodu || p.parca || '';
                    if (!grouped[kod]) {
                        grouped[kod] = { onarim: null, boya: null };
                    }
                    if (p.islemTuru === 'onarim') {
                        grouped[kod].onarim = p.seviye || null;
                    } else if (p.islemTuru === 'boya') {
                        grouped[kod].boya = p.seviye || null;
                    }
                });

                // Gruplanan parçaları frontend formatına çevir
                const result = [];
                Object.keys(grouped).forEach(kod => {
                    const { onarim, boya } = grouped[kod];
                    
                    if (onarim && boya) {
                        // Hem onarım hem boya var -> "seviye_boyaTuru_boya" formatı
                        result.push({
                            parca: kod,
                            islemTuru: `${onarim}_${boya}_boya`
                        });
                    } else if (onarim && !boya) {
                        // Sadece onarım var -> "boyasiz_onarim"
                        result.push({
                            parca: kod,
                            islemTuru: 'boyasiz_onarim'
                        });
                    }
                });
                
                return result;
            };

            setForm({
                rayicDeger: editData.rayic_bedel ? String(editData.rayic_bedel) : '',
                toplamHasar: editData.hasar_bedeli ? String(editData.hasar_bedeli) : '',
                marka: editData.marka || '',
                model: editData.model || '',
                km: editData.arac_kilometresi ? String(editData.arac_kilometresi) : '',
                arac_yasi: modelYili ? String(modelYili) : ''
            });
            setSelectedMarka(editData.marka || '');
            setSelectedModel(editData.model || '');
            setAracTuru(editData.arac_turu || 'Otomobil');
            setOnarilanList(mapOnarilanParcalar(editData.onarilan_parcalar));
            setDegisenList(mapDegisenParcalar(editData.degisen_parcalar));
        }
    }, [editData]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm(f => ({ ...f, [name]: value }));
    };

    const handleMarkaChange = (e) => {
        setSelectedMarka(e.target.value);
        setSelectedModel('');
        setForm(f => ({ ...f, marka: e.target.value, model: '' }));
    };
    const handleModelChange = (e) => {
        setSelectedModel(e.target.value);
        setForm(f => ({ ...f, model: e.target.value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        // Rayiç değeri al
        const rayic_bedel = Number(form.rayicDeger);
        // Modelin beklediği alanlara dönüştür
        // Seçili araç türünün kodunu bul
        const seciliArac = ARAC_TURU_LISTESI.find(t => t.ad === aracTuru);
        const aracKodu = seciliArac ? seciliArac.kod : undefined;

        // Değişen parçalar listesi - direkt gönder
        const mapDegisenParcaList = (list) =>
            list.map(item => ({
                parca_kodu: item.parca,
                islemTuru: item.islemTuru,
            }));

        // Onarılan parçalar listesi - parse et ve genişlet
        const mapOnarilanParcaList = (list) => {
            const result = [];
            list.forEach(item => {
                const { parca, islemTuru } = item;
                
                if (islemTuru === 'boyasiz_onarim') {
                    // Sadece onarım
                    result.push({
                        parca_kodu: parca,
                        islemTuru: 'onarim',
                        seviye: null
                    });
                } else {
                    // Parse et: "hafif_lokal_boya" -> hafif onarım + lokal boya
                    const parts = islemTuru.split('_'); // ["hafif", "lokal", "boya"]
                    const seviye = parts[0]; // hafif, orta, yuksek
                    const boyaTuru = parts[1]; // lokal, tam
                    
                    // Onarım entry
                    result.push({
                        parca_kodu: parca,
                        islemTuru: 'onarim',
                        seviye: seviye
                    });
                    
                    // Boya entry
                    result.push({
                        parca_kodu: parca,
                        islemTuru: 'boya',
                        seviye: boyaTuru
                    });
                }
            });
            return result;
        };

        // Parça listelerini hesapla
        const degisen_parcalar = mapDegisenParcaList(degisenList);
        const onarilan_parcalar = mapOnarilanParcaList(onarilanList);

        // Model yılından araç yaşını hesapla
        const modelYili = Number(form.arac_yasi);
        const mevcutYil = new Date().getFullYear();
        const hesaplananYas = mevcutYil - modelYili;

        const payload = {
            rayic_bedel: Number(rayic_bedel),
            hasar_bedeli: Number(form.toplamHasar),
            degisen_parca_sayisi: degisen_parcalar.length,
            onarilan_parca_sayisi: onarilan_parcalar.length,
            arac_kilometresi: Number(form.km),
            arac_yasi: hesaplananYas,
            marka: selectedMarka,
            model: selectedModel,
            arac_turu: aracTuru,
            arac_kodu: aracKodu,
            degisen_parcalar: degisen_parcalar,
            onarilan_parcalar: onarilan_parcalar
        };
        // Eğer arac_yasi ve parca_basi_hasar frontend'de hesaplanacaksa burada ekleyin
        try {
            const csrfToken = getCsrfToken();
            const response = await fetch('/predict', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken || '',
                },
                body: JSON.stringify(payload)
            });
            if (!response.ok) throw new Error('Sunucu hatası');
            if (response.status === 401 || response.status === 403) {
                onLogout && onLogout();
                return;
            }
            const result = await response.json();
            onNext(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="form-page">
<button
                    type="button"
                    className="btn-history"
                    onClick={onShowHistory}
                    style={{
                    position: 'absolute',
                    top: 24,
                    left: 24,
                    padding: '6px 14px',
                    borderRadius: 999,
                    border: 'none',
                    background: '#635bff',
                    color: '#fff',
                    fontSize: 13,
                    fontWeight: 600,
                    cursor: 'pointer',
                    boxShadow: '0 2px 6px rgba(0,0,0,0.25)',
                    width: 'auto',
                    minWidth: 'auto',
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '6px',
                    zIndex: 10,
                }}
            >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Geçmiş
            </button>
<button
                    type="button"
                    className="btn-logout"
                    onClick={onLogout}
                    style={{
                    position: 'absolute',
                    top: 24,
                    right: 24,
                    padding: '6px 14px',
                    borderRadius: 999,
                    border: 'none',
                    background: '#e53935',
                    color: '#fff',
                    fontSize: 13,
                    fontWeight: 600,
                    cursor: 'pointer',
                    boxShadow: '0 2px 6px rgba(0,0,0,0.25)',
                    width: 'auto',
                    minWidth: 'auto',
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 10,
                }}
            >
                Çıkış Yap
            </button>
            <div className="form-container">
                <div className="form-header">
                    <div className="brand-badge">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L2 7l10 5 10-5-10-5z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <path d="M2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                        Profesyonel Değerlendirme
                    </div>
                    <div>
                        <h1>Değer Analizi</h1>
                        <p className="subtitle">
                            Hızlı ve güvenilir hasar değerlendirmesi için bilgilerinizi girin
                        </p>
                    </div>
                </div>

                <div className="form-content">
                    <form onSubmit={handleSubmit}>

                        <div className="form-card">
                            <div className="card-header">
                                <div className="card-number">1</div>
                                <h2>Rayiç Değer Tespiti</h2>
                            </div>
                            <div className="card-content">
                                <div className="input-group">
                                    <label>Rayiç Değer <span className="required">*</span></label>
                                    <Input type="number" placeholder="0.00 ₺" name="rayicDeger" value={form.rayicDeger} onChange={handleChange} required />
                                </div>
                                <div className="info-banner">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M12 16v-4m0-4h.01M22 12c0 5.523-4.477 10-10 10S2 17.523 2 12 6.477 2 12 2s10 4.477 10 10z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    </svg>
                                    <span>Aracın piyasa rayiç değerini giriniz.</span>
                                </div>
                            </div>
                        </div>

                        <div className="form-card">
                            <div className="card-header">
                                <div className="card-number">2</div>
                                <h2>Hasar Detayları</h2>
                            </div>
                            <div className="card-content">

                                <div className="input-group">
                                    <label>Toplam Hasar Bedeli <span className="required">*</span></label>
                                    <Input type="number" placeholder="0.00 ₺" name="toplamHasar" value={form.toplamHasar} onChange={handleChange} required />
                                </div>

                                <div className="input-group">
                                    <label>Araç Türü <span className="required">*</span></label>
                                    <select
                                        className="select-arac-turu"
                                        value={aracTuru}
                                        onChange={e => setAracTuru(e.target.value)}
                                        required
                                    >
                                        <option value="">Araç Türü Seçiniz</option>
                                        {ARAC_TURU_LISTESI.map((tur, idx) => (
                                            <option key={idx} value={tur.ad}>{tur.ad}</option>
                                        ))}
                                    </select>
                                </div>

                                <div className="subsection">
                                    <div className="subsection-header">
                                        <div className="subsection-icon"></div>
                                        <h3 className="subsection-title">Onarılan Parçalar</h3>
                                    </div>
                                    <div className="card-content">
                                        <ParcaSecimList
                                            value={onarilanList}
                                            onChange={setOnarilanList}
                                            isOnarim={true}
                                            label="Onarılan Parçalar"
                                            aracKodu={aracTuru ? (ARAC_TURU_LISTESI.find(t => t.ad === aracTuru)?.kod) : undefined}
                                        />
                                    </div>
                                </div>

                                <div className="subsection">
                                    <div className="subsection-header">
                                        <div className="subsection-icon"></div>
                                        <h3 className="subsection-title">Değiştirilen Parçalar</h3>
                                    </div>
                                    <div className="card-content">
                                        <ParcaSecimList
                                            value={degisenList}
                                            onChange={setDegisenList}
                                            isOnarim={false}
                                            label="Değişen Parçalar"
                                            aracKodu={aracTuru ? (ARAC_TURU_LISTESI.find(t => t.ad === aracTuru)?.kod) : undefined}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="form-card">
                            <div className="card-header">
                                <div className="card-number">3</div>
                                <h2>Araç Bilgileri</h2>
                            </div>
                            <div className="card-content">
                                <div className="grid-2">
                                    <div className="input-group">
                                        <label>Araç Markası <span className="required">*</span></label>
                                        <Select
                                            options={MARKA_LISTESI.map(m => ({ label: m, value: m }))}
                                            value={selectedMarka ? { label: selectedMarka, value: selectedMarka } : null}
                                            onChange={opt => {
                                                setSelectedMarka(opt ? opt.value : '');
                                                setSelectedModel('');
                                                setForm(f => ({ ...f, marka: opt ? opt.value : '', model: '' }));
                                            }}
                                            placeholder="Marka Seçiniz"
                                            isClearable
                                            menuPortalTarget={document.body}
                                            styles={{
                                                control: (base) => ({ ...base, minHeight: 48, fontSize: 18, borderRadius: 10, borderColor: '#feb47b', boxShadow: '0 2px 8px #feb47b22' }),
                                                option: (base, state) => ({ ...base, fontSize: 18, padding: '12px 16px', color: state.isSelected ? '#fff' : '#222' }),
                                                menu: (base) => ({ ...base, zIndex: 9999 }),
                                                menuList: (base) => ({ ...base, maxHeight: '300px' }),
                                                menuPortal: (base) => ({ ...base, zIndex: 9999 }),
                                            }}
                                        />
                                    </div>
                                    <div className="input-group">
                                        <label>Araç Modeli <span className="required">*</span></label>
                                        <Select
                                            options={MODEL_LISTESI.filter(m => m.marka === selectedMarka && m.model).map(m => ({ label: m.model, value: m.model }))}
                                            value={selectedModel ? { label: selectedModel, value: selectedModel } : null}
                                            onChange={opt => {
                                                setSelectedModel(opt ? opt.value : '');
                                                setForm(f => ({ ...f, model: opt ? opt.value : '' }));
                                            }}
                                            placeholder="Model Seçiniz"
                                            isClearable
                                            isDisabled={!selectedMarka}
                                            menuPortalTarget={document.body}
                                            styles={{
                                                control: (base) => ({ ...base, minHeight: 48, fontSize: 18, borderRadius: 10, borderColor: '#feb47b', boxShadow: '0 2px 8px #feb47b22', background: !selectedMarka ? '#f5f5f5' : '#fff' }),
                                                option: (base, state) => ({ ...base, fontSize: 18, padding: '12px 16px', color: state.isSelected ? '#fff' : '#222' }),
                                                menu: (base) => ({ ...base, zIndex: 9999 }),
                                                menuList: (base) => ({ ...base, maxHeight: '300px' }),
                                                menuPortal: (base) => ({ ...base, zIndex: 9999 }),
                                            }}
                                        />
                                    </div>
                                </div>
                                <div className="grid-2">
                                    <div className="input-group">
                                        <label>Kilometre Bilgisi <span className="required">*</span></label>
                                        <Input type="number" placeholder="50000 km" name="km" value={form.km} onChange={handleChange} required />
                                    </div>
                                    <div className="input-group">
                                        <label>Model Yılı <span className="required">*</span></label>
                                        <Input type="number" placeholder="2020" name="arac_yasi" value={form.arac_yasi} onChange={handleChange} required />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="action-card">
                            <Button type="submit" disabled={loading}>{loading ? 'Analiz Ediliyor...' : 'Analizi Başlat'}</Button>
                        </div>
                        {error && <div className="error-message">{error}</div>}
                    </form>
                </div>
            </div>
        </div>
    );
}

export default FormPage;