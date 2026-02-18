import { useEffect, useMemo, useState } from 'react';
import { getCsrfToken } from '../utils/csrf';
import '../styles/historyPage.css';
import { PARCA_LISTESI_KODLU } from '../constants/partOptions';

function HistoryPage({ onBack, onLogout }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState({});

  // Parça kodu -> isim sözlüğü
  const parcaKodToAd = useMemo(() => {
    const map = {};
    PARCA_LISTESI_KODLU.forEach((p) => {
      map[p.kod] = p.ad;
    });
    return map;
  }, []);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      const userId = localStorage.getItem('userId');
      const csrfToken = getCsrfToken();

      const response = await fetch('/api/predictions/history', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken || '',
        },
        body: JSON.stringify(
          userId ? { user_id: Number(userId) } : {}
        ),
      });

      if (!response.ok) {
        throw new Error('Geçmiş tahminler yüklenemedi');
      }

      const data = await response.json();
      setHistory(data.results || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleSection = (id, key) => {
    setExpanded((prev) => ({
      ...prev,
      [id]: {
        ...(prev[id] || {}),
        [key]: !prev[id]?.[key],
      },
    }));
  };

  const formatDate = (dateString) => {
    if (!dateString) return '--';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('tr-TR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  const formatCurrency = (value) => {
    if (!value && value !== 0) return '--';
    return new Intl.NumberFormat('tr-TR', {
      style: 'currency',
      currency: 'TRY',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <div className="history-page">
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

      <div className="history-container">
        <div className="history-header">
          <button
            type="button"
            className="btn-back"
            onClick={onBack}
          >
            ← Geri
          </button>
          <h1>Geçmiş Tahminler</h1>
          <p className="subtitle">
            Daha önce yaptırdığınız tüm tahminleri görüntüleyebilirsiniz
          </p>
        </div>

        {loading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Yükleniyor...</p>
          </div>
        )}

        {error && (
          <div className="error-state">
            <p>{error}</p>
            <button onClick={fetchHistory} className="retry-btn">
              Tekrar Dene
            </button>
          </div>
        )}

        {!loading && !error && history.length === 0 && (
          <div className="empty-state">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <h3>Henüz tahmin yapılmamış</h3>
            <p>İlk tahmininizi yapmak için form sayfasına dönün</p>
          </div>
        )}

        {!loading && !error && history.length > 0 && (
          <div className="history-list">
            {history.map((item) => (
              <div key={item.id} className="history-card">
                <div className="history-card-header">
                  <div className="history-card-title">
                    <h3>
                      {item.marka && item.model
                        ? `${item.marka} ${item.model}`
                        : item.arac_turu || 'Araç Bilgisi Yok'}
                    </h3>
                    {item.arac_yasi != null && (
                      <div className="history-subtitle">
                        Araç yaşı: {item.arac_yasi}
                      </div>
                    )}
                    <span className="history-date">{formatDate(item.created_at)}</span>
                  </div>
                </div>
                <div className="history-card-content">
                  <div className="history-stats">
                    <div className="stat-item">
                      <span className="stat-label">Tahmini Değer Kaybı</span>
                      <span className="stat-value primary">
                        {formatCurrency(item.tahmini)}
                      </span>
                    </div>
                    <div className="stat-row">
                      <div className="stat-item">
                        <span className="stat-label">Min. Değer</span>
                        <span className="stat-value">{formatCurrency(item.min_deger)}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">Max. Değer</span>
                        <span className="stat-value">{formatCurrency(item.max_deger)}</span>
                      </div>
                    </div>
                    <div className="stat-row">
                      <div className="stat-item">
                        <span className="stat-label">Rayiç Bedel</span>
                        <span className="stat-value">{formatCurrency(item.rayic_bedel)}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">Hasar Bedeli</span>
                        <span className="stat-value">{formatCurrency(item.hasar_bedeli)}</span>
                      </div>
                    </div>
                  </div>

                  {/* Onarılan / Değişen parçalar - açılır/kapanır */}
                  <div className="parts-section">
                    <button
                      type="button"
                      className="parts-toggle"
                      onClick={() => toggleSection(item.id, 'onarilan')}
                    >
                      <span>
                        <span className="dot" style={{ color: '#10b981' }}>●</span>
                        Onarılan Parçalar
                      </span>
                      <span className="parts-toggle-icon">
                        {expanded[item.id]?.onarilan ? '▲' : '▼'}
                      </span>
                    </button>
                    {expanded[item.id]?.onarilan && (
                      <ul className="parts-list">
                        {(item.onarilan_parcalar || []).length === 0 && (
                          <li>Kayıtlı onarılan parça yok.</li>
                        )}
                        {(item.onarilan_parcalar || []).map((p, idx) => (
                          (() => {
                            const kod = p.parca_kodu || p.parca;
                            const ad = kod ? parcaKodToAd[kod] : null;
                            return (
                              <li key={idx}>
                                {kod || 'Parça'}
                                {ad ? ` - ${ad}` : ''}
                                {p.islemTuru ? ` · ${p.islemTuru}` : ''}
                                {p.seviye ? ` · ${p.seviye}` : ''}
                              </li>
                            );
                          })()
                        ))}
                      </ul>
                    )}

                    <button
                      type="button"
                      className="parts-toggle"
                      onClick={() => toggleSection(item.id, 'degisen')}
                      style={{ marginTop: 4 }}
                    >
                      <span>
                        <span className="dot" style={{ color: '#f97316' }}>●</span>
                        Değişen Parçalar
                      </span>
                      <span className="parts-toggle-icon">
                        {expanded[item.id]?.degisen ? '▲' : '▼'}
                      </span>
                    </button>
                    {expanded[item.id]?.degisen && (
                      <ul className="parts-list">
                        {(item.degisen_parcalar || []).length === 0 && (
                          <li>Kayıtlı değişen parça yok.</li>
                        )}
                        {(item.degisen_parcalar || []).map((p, idx) => (
                          (() => {
                            const kod = p.parca_kodu || p.parca;
                            const ad = kod ? parcaKodToAd[kod] : null;
                            return (
                              <li key={idx}>
                                {kod || 'Parça'}
                                {ad ? ` - ${ad}` : ''}
                                {p.islemTuru ? ` · ${p.islemTuru}` : ''}
                                {p.seviye ? ` · ${p.seviye}` : ''}
                              </li>
                            );
                          })()
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default HistoryPage;
