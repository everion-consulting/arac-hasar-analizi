import Input from '../components/Input';
import TextArea from '../components/TextArea';
import Button from '../components/Button';
import '../styles/formPage.css';

function FormPage({ onNext }) {
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
                    <form onSubmit={(e) => { e.preventDefault(); onNext(); }}>

                        <div className="form-card">
                            <div className="card-header">
                                <div className="card-number">1</div>
                                <h2>Rayiç Değer Tespiti</h2>
                            </div>
                            <div className="card-content">
                                <div className="grid-3">
                                    <div className="input-group">
                                        <label>Birinci Değer <span className="required">*</span></label>
                                        <Input type="number" placeholder="0.00 ₺" />
                                    </div>
                                    <div className="input-group">
                                        <label>İkinci Değer <span className="required">*</span></label>
                                        <Input type="number" placeholder="0.00 ₺" />
                                    </div>
                                    <div className="input-group">
                                        <label>Üçüncü Değer <span className="required">*</span></label>
                                        <Input type="number" placeholder="0.00 ₺" />
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
                                    <Input type="number" placeholder="0.00 ₺" />
                                </div>

                                <div className="subsection">
                                    <div className="subsection-header">
                                        <div className="subsection-icon"></div>
                                        <h3 className="subsection-title">Onarılan Parçalar</h3>
                                    </div>
                                    <div className="card-content">
                                        <div className="input-group">
                                            <label>Parça Açıklaması</label>
                                            <TextArea placeholder="Ön kaput, sağ ön çamurluk, tampon..." /> 
                                        </div>
                                        <div className="input-group">
                                            <label>Toplam Parça Sayısı</label>
                                            <Input type="number" placeholder="0" />
                                        </div>
                                    </div>
                                </div>

                                <div className="subsection">
                                    <div className="subsection-header">
                                        <div className="subsection-icon"></div>
                                        <h3 className="subsection-title">Değiştirilen Parçalar</h3>
                                    </div>
                                    <div className="card-content">
                                        <div className="input-group">
                                            <label>Parça Açıklaması</label>
                                            <TextArea placeholder="Sağ ön kapı, yan ayna, far..." />
                                        </div>
                                        <div className="input-group">
                                            <label>Toplam Parça Sayısı</label>
                                            <Input type="number" placeholder="0" />
                                        </div>
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
                                        <Input placeholder="Mercedes-Benz" />
                                    </div>
                                    <div className="input-group">
                                        <label>Araç Modeli <span className="required">*</span></label>
                                        <Input placeholder="C 200" />
                                    </div>
                                </div>
                                <div className="input-group">
                                    <label>Kilometre Bilgisi <span className="required">*</span></label>
                                    <Input type="number" placeholder="50000 km" />
                                </div>
                            </div>
                        </div>

                        <div className="action-card">
                            <Button type="submit">Analizi Başlat</Button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default FormPage;