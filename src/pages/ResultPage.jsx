import '../styles/resultPage.css';

function ResultPage({ onReset }) {
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
          <div className="result-grid">
            <div className="result-card">
              <span className="label">Minimum Değer Kaybı</span>
              <span className="value">-- ₺</span>
            </div>

            <div className="result-card">
              <span className="label">Maksimum Değer Kaybı</span>
              <span className="value">-- ₺</span>
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