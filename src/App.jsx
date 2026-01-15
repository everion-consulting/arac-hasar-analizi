import { useState } from 'react';
import FormPage from './pages/FormPage';
import ResultPage from './pages/ResultPage';

function App() {
  const [step, setStep] = useState(1);

  return (
    <>
      {step === 1 && <FormPage onNext={() => setStep(2)} />}
      {step === 2 && <ResultPage onReset={() => setStep(1)} />}
    </>
  );
}

export default App;
