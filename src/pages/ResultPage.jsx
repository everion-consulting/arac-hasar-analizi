import '../styles/resultPage.css';




function ResultPage({ onReset, result }) {
  // rayiç bedelini tahmini değerle aynı payloaddan alıyoruz
  // min = tahmini - rayic_bedel * 0.005
  // max = tahmini + rayic_bedel * 0.005
  const tahmini = result?.tahmini ?? null;
  const rayic = result?.rayic_bedel ?? null;
  let min = '--';
  let max = '--';
  if (tahmini !== null && rayic !== null) {
    min = Math.max(0, Math.round(tahmini - rayic * 0.005)) + ' ₺';
    max = Math.round(tahmini + rayic * 0.005) + ' ₺';
  }
  return (
    <div className="result-page">
      <div className="result-container">
        <div className="result-header">
          <div className="success-badge">
            <div className="success-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 6L9 17l-5-5" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            Analiz Tamamlandı
          </div>
          <h1>Değerlendirme Sonucu</h1>
          <p className="subtitle">
            Girilen bilgilere göre hesaplanan tahmini değer kaybı aralığı
          </p>
        </div>

        <div className="result-content">
          <div className="result-main" style={{display:'flex', justifyContent:'center', marginBottom:'2rem'}}>
            <div className="result-card" style={{minWidth:'260px', background:'#fff', borderRadius:'20px', boxShadow:'0 2px 12px rgba(0,0,0,0.07)', borderTop:'6px solid #ff9800', padding:'2.5rem 1rem', textAlign:'center'}}>
              <span className="label" style={{fontWeight:'bold', color:'#1a2a3a', fontSize:'1.2rem'}}>TAHMİNİ DEĞER KAYBI</span>
              <div className="value main" style={{fontSize:'2.8rem', fontWeight:'bold', color:'#1a2a3a', marginTop:'0.7rem'}}>
                {tahmini !== null ? tahmini + ' ₺' : '-- ₺'}
              </div>
            </div>
          </div>
          <div className="result-grid" style={{display:'flex', gap:'2rem', justifyContent:'center'}}>
            <div className="result-card" style={{minWidth:'220px', background:'#fff', borderRadius:'20px', boxShadow:'0 2px 12px rgba(0,0,0,0.07)', borderTop:'6px solid #ff9800', padding:'2rem 1rem', textAlign:'center'}}>
              <span className="label" style={{fontWeight:'bold', color:'#1a2a3a', fontSize:'1.1rem'}}>MINIMUM DEĞER KAYBI</span>
              <div className="value" style={{fontSize:'2.2rem', fontWeight:'bold', color:'#1a2a3a', marginTop:'0.5rem'}}>{min}</div>
            </div>
            <div className="result-card" style={{minWidth:'220px', background:'#fff', borderRadius:'20px', boxShadow:'0 2px 12px rgba(0,0,0,0.07)', borderTop:'6px solid #ff9800', padding:'2rem 1rem', textAlign:'center'}}>
              <span className="label" style={{fontWeight:'bold', color:'#1a2a3a', fontSize:'1.1rem'}}>MAKSIMUM DEĞER KAYBI</span>
              <div className="value" style={{fontSize:'2.2rem', fontWeight:'bold', color:'#1a2a3a', marginTop:'0.5rem'}}>{max}</div>
            </div>
          </div>

          <div className="info-card">
            <div className="info-banner">
              <div className="info-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 16v-4m0-4h.01M22 12c0 5.523-4.477 10-10 10S2 17.523 2 12 6.477 2 12 2s10 4.477 10 10z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <div className="info-text">
                Bu sonuçlar ön değerlendirme amaçlıdır. Kesin değer kaybı tutarı, ekspertiz incelemesi sonucunda netleşecektir.
              </div>
            </div>
          </div>

          <div className="action-section">
            <button className="secondary-btn" onClick={onReset}>
              Yeni Değerlendirme
            </button>
            <button className="primary-btn">
              Raporu İndir
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultPage;