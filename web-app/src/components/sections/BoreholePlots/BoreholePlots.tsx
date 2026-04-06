import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, RotateCcw } from 'lucide-react';
import animationConfig from '../../../data/animationConfig.json';
import metadata from '../../../data/metadata.json';
import BoreholeChart from './BoreholeChart';
import redoxData from '../../../data/redox.json';
import geochemistryData from '../../../data/geochemistry.json';

const BoreholePlots: React.FC = () => {
  // We can default isPlaying to true, but we don't have the Pause All button anymore.
  const [isPlaying] = useState(true);
  const [showComments, setShowComments] = useState<string | null>(null);

  // Correct order as requested: DEMO, LOOP2, LOOP3, LOOP4, LOOP6
  const BOREHOLE_ORDER = [
    'DEMO_D6', 'DEMO_D6_DISSOLVED', 'DEMO_D7', 'DEMO_D7_DISSOLVED',
    'LOOP2_P1', 'LOOP2_P2', 'LOOP2_P2A', 'LOOP2_P3', 'LOOP2_P4',
    'LOOP3_P1', 'LOOP3_P2', 'LOOP3_P3', 'LOOP3_P5', 'LOOP3_P6',
    'LOOP4_GeoW-2', 'LOOP4_IS-1', 'LOOP4_IS-2', 'LOOP4_MS-1', 'LOOP4_MS-2', 'LOOP4_TL-1', 'LOOP4_TL-2',
    'LOOP6_P1', 'LOOP6_P2', 'LOOP6_P2A', 'LOOP6_P3', 'LOOP6_P4', 'LOOP6_P5', 'LOOP6_P6', 'LOOP6_P7'
  ];

  return (
    <div className="space-y-12 pb-24 max-w-[1800px] mx-auto px-4">
      <header className="flex justify-between items-center bg-white p-8 rounded-2xl shadow-sm border border-slate-100">
        <div>
          <h2 className="text-4xl font-black text-slate-800 tracking-tight">Borehole Plots</h2>
          <p className="text-slate-500 mt-2 text-lg italic">Lithology, Color, Groundwater Table  Redox and geochemistry with different redox boundaries</p>
        </div>
      </header>

      <div className="flex flex-col gap-12">
        {BOREHOLE_ORDER.map((id) => {
          const isDissolved = id.includes('_DISSOLVED');
          const baseId = id.replace('_DISSOLVED', '');
          const config = (animationConfig as any)[baseId] || { animate: false };
          const meta = (metadata as any)[baseId] || {};

          return (
            <div key={id} className="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-200 flex flex-col transition-all duration-500 hover:shadow-2xl">
              <div className="bg-slate-900 text-white p-6 flex justify-between items-center border-b border-slate-800">
                <div className="flex items-center gap-6">
                  <div className="flex gap-2">
                    <button 
                        onClick={() => setShowComments(id)}
                        className="p-2.5 bg-slate-800 hover:bg-action-blue rounded-lg transition-colors"
                        title="View Field Notes"
                    >
                        <MessageSquare size={20} />
                    </button>
                    <button 
                        title="Download Raw Dataset"
                        onClick={() => {
                        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify((redoxData as any)[baseId] || (geochemistryData as any)[baseId]));
                        const downloadAnchorNode = document.createElement('a');
                        downloadAnchorNode.setAttribute("href",     dataStr);
                        downloadAnchorNode.setAttribute("download", `${id}_data.json`);
                        document.body.appendChild(downloadAnchorNode);
                        downloadAnchorNode.click();
                        downloadAnchorNode.remove();
                        }}
                        className="p-2.5 bg-slate-800 hover:bg-emerald-600 rounded-lg transition-colors"
                    >
                        <RotateCcw size={20} className="rotate-180" />
                    </button>
                  </div>
                  <div>
                    <h3 className="font-black text-2xl tracking-tight">{id.replace('_DISSOLVED', ' (Dissolved)').replace('_', ' ')}</h3>
                    <p className="text-xs text-slate-500 uppercase tracking-widest font-bold mt-1">DGU Number: {meta.DGU || 'Unknown'}</p>
                  </div>
                </div>
                <div className="flex gap-8 text-sm">
                   <div className="bg-slate-800 px-4 py-2 rounded-lg">
                      <span className="text-slate-500 font-bold uppercase text-[10px] block">Elevation</span>
                      <span className="font-mono font-bold text-slate-200">{meta.Elevation}m</span>
                   </div>
                </div>
              </div>

              <div className="relative bg-white min-h-[600px] overflow-x-auto custom-scrollbar">
                <BoreholeChart 
                   boreholeId={id} 
                   isDissolved={isDissolved} 
                   isPlaying={isPlaying} 
                />

                {/* Overlay for Comments */}
                {showComments === id && (
                  <motion.div 
                    initial={{ opacity: 0, x: 100 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="absolute right-0 top-0 bottom-0 w-96 bg-white/98 z-30 shadow-2xl p-8 border-l border-slate-200 flex flex-col"
                  >
                    <div className="flex justify-between items-center mb-8 border-b border-slate-100 pb-4">
                      <div className="flex items-center gap-3">
                        <MessageSquare className="text-action-blue w-6 h-6" />
                        <h4 className="font-black text-slate-800 text-xl">Field Notes</h4>
                      </div>
                      <button onClick={() => setShowComments(null)} className="text-slate-400 hover:text-rose-500 font-black text-2xl">✕</button>
                    </div>
                    
                    <div className="flex-grow overflow-y-auto space-y-6 mb-8 pr-2 custom-scrollbar">
                      <div className="bg-slate-50 border-l-4 border-action-blue p-6 rounded-r-2xl">
                        <p className="text-xs font-black text-slate-400 uppercase mb-2 tracking-widest">Initial Observation</p>
                        <p className="italic text-slate-700 text-md leading-relaxed">
                          "Strong redox interface observed at {config.interval?.[0] || '?' }m depth. Alignment with lithological color shift confirmed."
                        </p>
                      </div>
                    </div>

                    <div className="space-y-4">
                      <input type="text" placeholder="Scientist Name" className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm font-bold focus:ring-2 focus:ring-action-blue outline-none" />
                      <textarea rows={4} placeholder="Add a comment..." className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-action-blue outline-none resize-none" />
                      <button className="w-full bg-action-blue text-white py-4 rounded-xl font-black tracking-widest hover:bg-blue-600 shadow-lg transition-all">POST COMMENT</button>
                    </div>
                  </motion.div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default BoreholePlots;
