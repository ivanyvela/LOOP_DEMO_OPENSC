import React, { useState } from 'react';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Home from './components/sections/Home/Home';
import BoreholePlots from './components/sections/BoreholePlots/BoreholePlots';
import NitrateReduction from './components/sections/NitrateReduction/NitrateReduction';
import Method from './components/sections/Method/Method';
import HistoryContact from './components/sections/HistoryContact/HistoryContact';
import OtherGraphs from './components/sections/OtherGraphs/OtherGraphs';

const App: React.FC = () => {
  const [activeSection, setActiveSection] = useState('home');

  const renderSection = () => {
    switch (activeSection) {
      case 'home':
        return <Home />;
      case 'borehole-plots':
        return <BoreholePlots />;
      case 'nitrate-reduction':
        return <NitrateReduction />;
      case 'method':
        return <Method />;
      case 'other-graphs':
        return <OtherGraphs />;
      case 'history-contact':
        return <HistoryContact />;
      default:
        return <Home />;
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f4f6f9] text-[#333] font-sans">
      <Header activeSection={activeSection} onSectionChange={setActiveSection} />
      <main className="flex-grow container mx-auto p-4">
        {renderSection()}
      </main>
      <Footer />
    </div>
  );
};

export default App;
