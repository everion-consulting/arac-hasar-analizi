import { useState } from 'react';
import FormPage from './pages/FormPage';
import ResultPage from './pages/ResultPage';


function App() {
  const [step, setStep] = useState(1);
  const [result, setResult] = useState(null);

  const handleNext = (res) => {
    setResult(res);
    setStep(2);
  };

  const handleReset = () => {
    setResult(null);
    setStep(1);
  };

  return (
    <>
      {step === 1 && <FormPage onNext={handleNext} />}
      {step === 2 && <ResultPage onReset={handleReset} result={result} />}
    </>
  );
}

export default App;
