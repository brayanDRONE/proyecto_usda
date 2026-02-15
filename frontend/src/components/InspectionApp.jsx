/**
 * InspectionApp - Aplicación de inspección para usuarios de establecimiento
 */

import { useState } from 'react';
import { ThemeProvider } from '../contexts/ThemeContext';
import Header from './Header';
import InspectionForm from './InspectionForm';
import SamplingResultView from './SamplingResultView';
import SubscriptionExpiredView from './SubscriptionExpiredView';

function InspectionAppContent() {
  const [samplingResult, setSamplingResult] = useState(null);
  const [showSubscriptionExpired, setShowSubscriptionExpired] = useState(false);

  const handleSamplingGenerated = (result) => {
    setSamplingResult(result);
    setShowSubscriptionExpired(false);
  };

  const handleSubscriptionError = () => {
    setShowSubscriptionExpired(true);
    setSamplingResult(null);
  };

  const handleNewInspection = () => {
    setSamplingResult(null);
    setShowSubscriptionExpired(false);
  };

  return (
    <div className="app">
      <Header />
      
      <main className="main-container">
        <div className="content-wrapper">
          {showSubscriptionExpired ? (
            <SubscriptionExpiredView />
          ) : samplingResult ? (
            <SamplingResultView 
              result={samplingResult} 
              onNewInspection={handleNewInspection}
            />
          ) : (
            <InspectionForm 
              onSamplingGenerated={handleSamplingGenerated}
              onSubscriptionError={handleSubscriptionError}
            />
          )}
        </div>
      </main>
    </div>
  );
}

function InspectionApp() {
  return (
    <ThemeProvider>
      <InspectionAppContent />
    </ThemeProvider>
  );
}

export default InspectionApp;
