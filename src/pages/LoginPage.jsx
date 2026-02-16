import { useState } from 'react';
import { getCsrfToken } from '../utils/csrf';
import '../styles/formPage.css';

function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const csrfToken = getCsrfToken();
      const response = await fetch('/auth/login', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken || '',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || 'Giriş başarısız');
      }

      // Giriş başarılıysa localStorage'a işaret koy ve parent'a haber ver
      localStorage.setItem('isLoggedIn', 'true');
      onLoginSuccess();
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
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 2L2 7l10 5 10-5-10-5z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M2 17l10 5 10-5M2 12l10 5 10-5"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            Yetkili Giriş
          </div>
          <h1>Araç Hasar Analizi - Giriş</h1>
          <p className="subtitle">
            Sisteme erişmek için kullanıcı adı ve şifrenizle giriş yapın.
          </p>
        </div>

        <div className="form-content">
          <form onSubmit={handleSubmit}>
            <div className="form-card">
              <div className="card-header">
                <div className="card-number">1</div>
                <h2>Giriş Bilgileri</h2>
              </div>
              <div className="card-content">
                <div className="input-group">
                  <label>Kullanıcı Adı</label>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
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
                      outline: 'none',
                    }}
                  />
                </div>
                <div className="input-group">
                  <label>Şifre</label>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
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
                      outline: 'none',
                    }}
                  />
                </div>
              </div>
            </div>

            <div className="action-card">
              <button
                type="submit"
                className="primary-btn"
                disabled={loading}
              >
                {loading ? 'Giriş yapılıyor...' : 'Giriş Yap'}
              </button>
            </div>
            {error && <div className="error-message">{error}</div>}
          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;

