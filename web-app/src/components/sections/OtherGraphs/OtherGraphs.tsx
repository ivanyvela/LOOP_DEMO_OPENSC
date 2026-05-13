import React from 'react';
import { getAssetPath } from '../../../utils/assets';

const OtherGraphs: React.FC = () => {
  const numPlots = 27;
  const plots = Array.from({ length: numPlots }, (_, i) => getAssetPath(`/plots/eem/eem_plot_${i}.png`));

  return (
    <div className="max-w-[98%] mx-auto space-y-16 pb-24 px-4 mt-8">
      <section className="text-center space-y-6">
        <h2 className="text-4xl md:text-5xl font-black text-slate-800 tracking-tight">Electron Equivalence Balance Plots</h2>
      </section>

      <div className="space-y-12">
        <div className="flex flex-col gap-12">
          {plots.map((plotSrc, index) => (
            <div key={index} className="w-full flex justify-center bg-white p-2 rounded-3xl shadow-xl border border-slate-100">
              <img 
                src={plotSrc} 
                className="w-full h-auto rounded-xl shadow-sm" 
                alt={`Electron Equivalence Balance Plot ${index + 1}`} 
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default OtherGraphs;
