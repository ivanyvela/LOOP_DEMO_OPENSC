import React, { useState } from 'react';
import { Sliders, Info } from 'lucide-react';
import { getAssetPath } from '../../../utils/assets';

const NitrateReduction: React.FC = () => {
  // Simplified Parameter State
  const [interfaceType, setInterfaceType] = useState('redox_primary');
  const [reductionRatio, setReductionRatio] = useState('50');
  const [threshold, setThreshold] = useState('5_0');

  const interfaceOptions = [
    { id: 'redox_primary', label: 'Redox Primary' },
    { id: 'redox_secondary', label: 'Redox Secondary' },
    { id: 'geus_fri', label: 'GEUS FRI' },
    { id: 'color_with_litho', label: 'Color FRI (Litho)' },
    { id: 'color_without_litho', label: 'Color FRI (No Litho)' }
  ];

  const ratioOptions = [
    { id: '50', label: '50%' },
    { id: '80', label: '80%' }
  ];

  const thresholdOptions = [
    { id: '1_5', label: '1.5' },
    { id: '5_0', label: '5.0' }
  ];

  // Dynamic image path generation based on state
  const imageSuffix = `${interfaceType}_${reductionRatio}_${threshold}`;

  return (
    <div className="space-y-12 pb-24 max-w-[1400px] mx-auto px-4">
      <header className="border-l-8 border-action-blue pl-8 py-4 bg-white rounded-r-2xl shadow-sm">
        <h2 className="text-4xl font-black text-slate-800 tracking-tight">Nitrate Reduction Sensitivity Analysis</h2>
        <p className="text-slate-500 mt-2 text-lg">
          Evaluate the Redox Probe's predictive accuracy under varying geochemical and spatial constraints.
        </p>
      </header>

      {/* Control Panel */}
      <section className="bg-slate-900 rounded-3xl shadow-2xl p-8 text-white space-y-8">
        <div className="flex items-center gap-3 text-action-blue">
          <Sliders className="w-6 h-6" />
          <h3 className="font-black uppercase tracking-[0.2em] text-sm">Parameter Optimization Engine</h3>
        </div>

        {/* Row 1: Boundary to Test */}
        <div className="space-y-4">
          <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
            Type of Interface (BOUNDARY_TO_TEST) <Info className="w-3 h-3 cursor-help" />
          </label>
          <div className="flex flex-wrap gap-2 bg-slate-800 p-1.5 rounded-xl border border-slate-700/50">
            {interfaceOptions.map(opt => (
              <button
                key={opt.id}
                onClick={() => setInterfaceType(opt.id)}
                className={`flex-1 min-w-[140px] py-3 rounded-lg text-xs font-bold transition-all ${
                  interfaceType === opt.id 
                    ? 'bg-action-blue text-white shadow-lg shadow-action-blue/20' 
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        {/* Row 2: Parameters */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pt-4 border-t border-slate-800/80">
          
          {/* Reduction Ratio */}
          <div className="space-y-4">
            <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
              Reduction Percentage (%) ('REDUCTION_RATIO') <Info className="w-3 h-3 cursor-help" />
            </label>
            <div className="flex gap-2 bg-slate-800 p-1.5 rounded-xl border border-slate-700/50 max-w-[300px]">
              {ratioOptions.map(val => (
                <button
                  key={val.id}
                  onClick={() => setReductionRatio(val.id)}
                  className={`flex-1 py-3 rounded-lg text-xs font-black transition-all ${
                    reductionRatio === val.id 
                      ? 'bg-action-blue text-white shadow-lg shadow-action-blue/20' 
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
                  }`}
                >
                  {val.label}
                </button>
              ))}
            </div>
          </div>

          {/* Threshold */}
          <div className="space-y-4">
            <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
              N Depletion Threshold (mg/L) ('NO_NITRATE_THRESHOLD') <Info className="w-3 h-3 cursor-help" />
            </label>
            <div className="flex gap-2 bg-slate-800 p-1.5 rounded-xl border border-slate-700/50 max-w-[300px]">
              {thresholdOptions.map(val => (
                <button
                  key={val.id}
                  onClick={() => setThreshold(val.id)}
                  className={`flex-1 py-3 rounded-lg text-xs font-black transition-all ${
                    threshold === val.id 
                      ? 'bg-action-blue text-white shadow-lg shadow-action-blue/20' 
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
                  }`}
                >
                  {val.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Results Section */}
      <section className="space-y-12">
        <div className="w-full">
          <img 
            src={getAssetPath(`/plots/nitrate_success_rates_${imageSuffix}.png`)} 
            alt={`Success Rates for ${interfaceType}`} 
            className="w-full h-auto rounded-3xl shadow-sm border border-slate-100 transition-opacity duration-300" 
            onError={(e) => (e.currentTarget.style.opacity = '0.5')}
            onLoad={(e) => (e.currentTarget.style.opacity = '1')}
          />
        </div>
        <div className="w-full">
          <img 
            src={getAssetPath(`/plots/nitrate_validation_matrix_${imageSuffix}.png`)} 
            alt={`Validation Matrix for ${interfaceType}`} 
            className="w-full h-auto rounded-3xl shadow-sm border border-slate-100 transition-opacity duration-300"
            onError={(e) => (e.currentTarget.style.opacity = '0.5')}
            onLoad={(e) => (e.currentTarget.style.opacity = '1')} 
          />
        </div>
        <div className="w-full bg-white rounded-3xl shadow-sm border border-slate-100 p-6">
          <img 
            src={getAssetPath(`/plots/nitrate_profiles_${imageSuffix}.png`)} 
            alt={`Nitrate Profiles for ${interfaceType}`} 
            className="w-full h-auto rounded-xl transition-opacity duration-300" 
            onError={(e) => (e.currentTarget.style.opacity = '0.5')}
            onLoad={(e) => (e.currentTarget.style.opacity = '1')}
          />
        </div>
      </section>
    </div>
  );
};

export default NitrateReduction;
