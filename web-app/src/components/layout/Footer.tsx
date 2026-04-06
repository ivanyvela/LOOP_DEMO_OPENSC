import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-[#2c3e50] text-gray-400 py-6 mt-10">
      <div className="container mx-auto px-4 text-center">
        <p>&copy; {new Date().getFullYear()} Redox Probe Research Project. All rights reserved.</p>
        <p className="text-sm mt-2 italic text-[#bdc3c7]">Open Science Platform</p>
      </div>
    </footer>
  );
};

export default Footer;
