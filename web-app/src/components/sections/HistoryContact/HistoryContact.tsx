import React, { useState } from 'react';
import { Mail, Bell, Code, History } from 'lucide-react';

const HistoryContact: React.FC = () => {
  const [email, setEmail] = useState('');

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Thank you! Subscription request for ${email} has been received.`);
    setEmail('');
  };

  const versions = [
    { date: '2026-04-05', version: 'v1.0.0-beta', changes: 'Initial Open Science Platform launch with interactive DK map and data repository.' },
    { date: '2026-03-20', version: 'v0.9.0-alpha', changes: 'Finalized redox interface detection algorithms and metadata consolidation.' },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-12">
      {/* Contact Section */}
      <section className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
        <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
          <Mail className="text-[#2980b9]" /> Get in Touch
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <p className="text-gray-600 mb-6">
              For scientific inquiries, collaboration proposals, or feedback on the data, please contact one of the two lead scientists.
            </p>
            <div className="space-y-4">
              <a 
                href="mailto:ivan.yelamos@gmail.com" 
                className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors border border-gray-200"
              >
                <Mail className="text-[#2c3e50]" />
                <span className="font-semibold text-[#2c3e50]">ivan.yelamos@gmail.com</span>
              </a>
              <a 
                href="mailto:palle.ejlskov@ejlskov.com" 
                className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors border border-gray-200"
              >
                <Mail className="text-[#2c3e50]" />
                <span className="font-semibold text-[#2c3e50]">palle.ejlskov@ejlskov.com</span>
              </a>
              <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg border border-gray-200">
                <Code className="text-[#2c3e50]" />
                <span className="text-sm text-gray-500">Project hosted on GitHub Open Science</span>
              </div>
            </div>
            <div className="mt-8 pt-6 border-t border-gray-100">
              <p className="text-sm text-gray-500 italic">
                We acknowledge <a href="https://www.geus.dk/" target="_blank" rel="noopener noreferrer" className="text-[#2980b9] hover:underline">GEUS</a> for their valuable contribution to this platform.
              </p>
            </div>
          </div>

          <div className="bg-[#f4f6f9] p-6 rounded-xl">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Bell className="text-[#e67e22]" size={20} /> Subscribe to Updates
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Receive notifications whenever new data, papers, or borehole animations are added to the site.
            </p>
            <form onSubmit={handleSubscribe} className="space-y-3">
              <input 
                type="email" 
                placeholder="your.email@example.com"
                required
                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#2980b9] focus:outline-none"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <button 
                type="submit"
                className="w-full bg-[#2980b9] text-white font-bold py-2 rounded-lg hover:bg-[#1f6391] transition-colors"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* Version History */}
      <section>
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <History className="text-gray-500" /> Version History
        </h2>
        <div className="space-y-4">
          {versions.map((v, i) => (
            <div key={i} className="flex gap-4">
              <div className="flex flex-col items-center">
                <div className="w-3 h-3 bg-[#2980b9] rounded-full"></div>
                {i < versions.length - 1 && <div className="w-0.5 h-full bg-gray-200 my-1"></div>}
              </div>
              <div className="pb-6">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-mono text-sm font-bold text-gray-400">{v.date}</span>
                  <span className="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded-full font-bold">{v.version}</span>
                </div>
                <p className="text-gray-700">{v.changes}</p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default HistoryContact;
