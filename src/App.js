import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import PatientProfile from './components/PatientProfile';
import KatzADL from './assessments/KatzADL';
import BarthelIndex from './assessments/BarthelIndex';
import FIM from './assessments/FIM';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [selectedAssessment, setSelectedAssessment] = useState(null);

  const navigateTo = (view, data = null) => {
    setCurrentView(view);
    if (view === 'patient-profile') {
      setSelectedPatient(data);
    } else if (view === 'katz-adl' || view === 'barthel' || view === 'fim') {
      setSelectedAssessment(view);
    }
  };

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard onNavigate={navigateTo} />;
      case 'patient-profile':
        return <PatientProfile patient={selectedPatient} onBack={() => navigateTo('dashboard')} />;
      case 'katz-adl':
        return <KatzADL onBack={() => navigateTo('dashboard')} />;
      case 'barthel':
        return <BarthelIndex onBack={() => navigateTo('dashboard')} />;
      case 'fim':
        return <FIM onBack={() => navigateTo('dashboard')} />;
      default:
        return <Dashboard onNavigate={navigateTo} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {renderView()}
    </div>
  );
}

export default App;
