import { useState } from 'react';
import FormPage from './pages/FormPage';
import ResultPage from './pages/ResultPage';
import LoginPage from './pages/LoginPage';

function App() {
  const [step, setStep] = useState(1);
  const [result, setResult] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(
    () => localStorage.getItem('isLoggedIn') === 'true'
  );

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

  if (!isLoggedIn) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <>
      {step === 1 && <FormPage onNext={handleNext} />}
      {step === 2 && <ResultPage onReset={handleReset} result={result} />}
    </>
  );
}

export default App;
