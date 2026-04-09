import React from 'react';
import { getAssetPath } from '../../../utils/assets';

const Home: React.FC = () => {
  return (
    <div className="space-y-12">
      <header className="text-center space-y-4">
        <h1 className="text-5xl font-black text-slate-800 tracking-tight">Redox Probe Open Science Platform</h1>
        <p className="text-xl text-slate-500 max-w-2xl mx-auto italic">
          Measuring electron activity directly underground
        </p>
      </header>
      
      <div className="relative mx-auto w-full max-w-6xl aspect-[1.1/1] bg-slate-900 rounded-3xl shadow-2xl overflow-hidden border-8 border-white">
        <img 
          src={getAssetPath('/map-example.png')} 
          alt="Research Map of Denmark" 
          className="absolute inset-0 w-full h-full object-cover"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 hover:shadow-lg transition-shadow">
          <div className="w-12 h-12 bg-action-blue/10 rounded-2xl flex items-center justify-center text-action-blue mb-6">
             <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
          </div>
          <h3 className="text-xl font-black text-slate-800 mb-4">Open Data Access</h3>
          <p className="text-slate-500 text-sm leading-relaxed">
            Every borehole animation on this platform provides direct access to the raw CSV datasets, promoting transparency and reproducibility in soil science.
          </p>
        </div>
        <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 hover:shadow-lg transition-shadow">
          <div className="w-12 h-12 bg-emerald-100 rounded-2xl flex items-center justify-center text-emerald-600 mb-6">
             <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
          </div>
          <h3 className="text-xl font-black text-slate-800 mb-4">Algorithmic Precision</h3>
          <p className="text-slate-500 text-sm leading-relaxed">
            We utilize high-resolution inserts to eliminate subjective bias, standardizing the detection of redox boundaries across diverse geological settings.
          </p>
        </div>
        <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 hover:shadow-lg transition-shadow">
          <div className="w-12 h-12 bg-amber-100 rounded-2xl flex items-center justify-center text-amber-600 mb-6">
             <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
          </div>
          <h3 className="text-xl font-black text-slate-800 mb-4">Collaborative Effort</h3>
          <p className="text-slate-500 text-sm leading-relaxed">
            This platform facilitates a shared understanding of the differences between the instrument determined FRI and the inferred FRI from other parameters
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
