import React from 'react';

interface HeaderProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
}

const Header: React.FC<HeaderProps> = ({ activeSection, onSectionChange }) => {
  const navItems = [
    { id: 'home', label: 'Welcome' },
    { id: 'borehole-plots', label: 'Borehole Plots' },
    { id: 'nitrate-reduction', label: 'Nitrate Reduction' },
    { id: 'method', label: 'Method' },
    { id: 'history-contact', label: 'History & Contact' },
  ];

  return (
    <header className="bg-[#2c3e50] text-white shadow-md">
      <div className="container mx-auto px-4 py-6 text-center">
        <h1 className="text-3xl font-bold">Redox Probe ability to find FRI (First Redox Interface)</h1>
        <h2 className="text-lg text-[#bdc3c7] mt-1">Geochemical evaluation against various FRI methods with a special focus on Nitrate</h2>
      </div>
      <nav className="bg-[#34495e] flex justify-center py-2 gap-4">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onSectionChange(item.id)}
            className={`px-4 py-2 rounded transition-colors ${
              activeSection === item.id ? 'bg-[#2980b9] text-white' : 'text-gray-300 hover:bg-[#2980b9] hover:text-white'
            }`}
          >
            {item.label}
          </button>
        ))}
      </nav>
    </header>
  );
};

export default Header;
