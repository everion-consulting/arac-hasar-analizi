import { useEffect, useState } from 'react';
import FormPage from './pages/FormPage';
import ResultPage from './pages/ResultPage';
import LoginPage from './pages/LoginPage';
import { getCsrfToken } from './utils/csrf';

function App() {
  const [step, setStep] = useState(1);
  const [result, setResult] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(
    () => localStorage.getItem('isLoggedIn') === 'true'
  );

  // Uygulama ilk yüklendiğinde CSRF cookie'sini al
  useEffect(() => {
    fetch('/auth/csrf', { credentials: 'include' }).catch(() => {
      // sessizce geç; sadece cookie üretmek için çağırıyoruz
    });
  }, []);

  const handleNext = (res) => {
    setResult(res);
    setStep(2);
  };

  const handleReset = () => {
    setResult(null);
    setStep(1);
  };

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = async () => {
    try {
      const csrfToken = getCsrfToken();
      await fetch('/auth/logout', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken || '',
        },
      });
    } catch {
      // hata olsa bile local tarafı temizle
    }
    localStorage.removeItem('isLoggedIn');
    setIsLoggedIn(false);
    setResult(null);
    setStep(1);
  };

  if (!isLoggedIn) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <>
      {step === 1 && <FormPage onNext={handleNext} onLogout={handleLogout} />}
      {step === 2 && (
        <ResultPage onReset={handleReset} onLogout={handleLogout} result={result} />
      )}
    </>
  );
}

export default App;
