import Input from '../components/Input';
import TextArea from '../components/TextArea';
import Button from '../components/Button';
import '../styles/formPage.css';

import { useState } from 'react';
import { ParcaSecimList } from '../components/ParcaSecimList';
import { ARAC_TURU_LISTESI, MARKA_LISTESI, MODEL_LISTESI } from '../constants/partOptions';
import Select from 'react-select';


function FormPage({ onNext }) {
    const [form, setForm] = useState({
        birinci: '', ikinci: '', ucuncu: '',
        toplamHasar: '',
        marka: '', model: '', km: '', arac_yasi: ''
    });
    const [selectedMarka, setSelectedMarka] = useState('');
    const [selectedModel, setSelectedModel] = useState('');
    const [aracTuru, setAracTuru] = useState(''); // seçili araç türü adı
    const [onarilanList, setOnarilanList] = useState([]); // [{parca, islemTuru, seviye}]
    const [degisenList, setDegisenList] = useState([]); // [{parca, islemTuru, seviye}]
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm(f => ({ ...f, [name]: value }));
    };

    // Marka değişince modeli sıfırla
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
        // 3 rayiç değerinin ortalamasını al
        const rayic_bedel = (
            (Number(form.birinci) + Number(form.ikinci) + Number(form.ucuncu)) / 3
        ).toFixed(2);
        // Modelin beklediği alanlara dönüştür
        // Seçili araç türünün kodunu bul
        const seciliArac = ARAC_TURU_LISTESI.find(t => t.ad === aracTuru);
        const aracKodu = seciliArac ? seciliArac.kod : undefined;

        // Parça listelerini sadece kod olarak gönder
        const mapParcaList = (list) =>
            list.map(item => ({
                parca_kodu: item.parca, // kodu
                islemTuru: item.islemTuru,
                seviye: item.seviye
            }));

        const payload = {
            rayic_bedel: Number(rayic_bedel),
            hasar_bedeli: Number(form.toplamHasar),
            degisen_parca_sayisi: degisenList.length,
            onarilan_parca_sayisi: onarilanList.length,
            arac_kilometresi: Number(form.km),
            arac_yasi: Number(form.arac_yasi),
            marka: selectedMarka,
            model: selectedModel,
            arac_turu: aracTuru,
            arac_kodu: aracKodu,
            degisen_parcalar: mapParcaList(degisenList),
            onarilan_parcalar: mapParcaList(onarilanList)
        };
        // Eğer arac_yasi ve parca_basi_hasar frontend'de hesaplanacaksa burada ekleyin
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) throw new Error('Sunucu hatası');
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
            <div className="form-container">
                <div className="form-header">
                    <div className="brand-badge">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L2 7l10 5 10-5-10-5z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <path d="M2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                        Profesyonel Değerlendirme
                    </div>
                    <h1>Araç Hasar Analizi</h1>
                    <p className="subtitle">
                        Hızlı ve güvenilir hasar değerlendirmesi için bilgilerinizi girin
                    </p>
                </div>

                <div className="form-content">
                    <form onSubmit={handleSubmit}>

                        <div className="form-card">
                            <div className="card-header">
                                <div className="card-number">1</div>
                                <h2>Rayiç Değer Tespiti</h2>
                            </div>
                            <div className="card-content">
                                <div className="grid-3">
                                    <div className="input-group">
                                        <label>Birinci Değer <span className="required">*</span></label>
                                        <Input type="number" placeholder="0.00 ₺" name="birinci" value={form.birinci} onChange={handleChange} required />
                                    </div>
                                    <div className="input-group">
                                        <label>İkinci Değer <span className="required">*</span></label>
                                        <Input type="number" placeholder="0.00 ₺" name="ikinci" value={form.ikinci} onChange={handleChange} required />
                                    </div>
                                    <div className="input-group">
                                        <label>Üçüncü Değer <span className="required">*</span></label>
                                        <Input type="number" placeholder="0.00 ₺" name="ucuncu" value={form.ucuncu} onChange={handleChange} required />
                                    </div>
                                </div>
                                <div className="info-banner">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M12 16v-4m0-4h.01M22 12c0 5.523-4.477 10-10 10S2 17.523 2 12 6.477 2 12 2s10 4.477 10 10z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    </svg>
                                    <span>Sistem otomatik olarak üç değerin ortalamasını alacak ve hesaplamada kullanacaktır.</span>
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
                                        value={aracTuru}
                                        onChange={e => setAracTuru(e.target.value)}
                                        required
                                        style={{
                                            width: '100%',
                                            padding: '14px 18px',
                                            borderRadius: 10,
                                            border: '1.5px solid #feb47b',
                                            fontSize: 18,
                                            background: '#fff',
                                            marginTop: 4,
                                            boxShadow: '0 2px 8px #feb47b22',
                                            color: aracTuru ? '#222' : '#aaa',
                                            fontWeight: 500,
                                            outline: 'none',
                                            transition: 'border 0.2s',
                                        }}
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
                                            styles={{
                                                control: (base) => ({ ...base, minHeight: 48, fontSize: 18, borderRadius: 10, borderColor: '#feb47b', boxShadow: '0 2px 8px #feb47b22' }),
                                                option: (base, state) => ({ ...base, fontSize: 18, color: state.isSelected ? '#fff' : '#222' }),
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
                                            styles={{
                                                control: (base) => ({ ...base, minHeight: 48, fontSize: 18, borderRadius: 10, borderColor: '#feb47b', boxShadow: '0 2px 8px #feb47b22', background: !selectedMarka ? '#f5f5f5' : '#fff' }),
                                                option: (base, state) => ({ ...base, fontSize: 18, color: state.isSelected ? '#fff' : '#222' }),
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
                                        <label>Araç Yaşı <span className="required">*</span></label>
                                        <Input type="number" placeholder="5" name="arac_yasi" value={form.arac_yasi} onChange={handleChange} required />
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