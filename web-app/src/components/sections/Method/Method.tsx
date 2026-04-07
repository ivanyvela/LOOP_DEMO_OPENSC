import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FileText, 
  Download, 
  ExternalLink, 
  Cpu, 
  Database, 
  ChevronRight, 
  Info,
  Palette,
  Map as MapIcon,
  Wrench,
  X,
  Maximize2
} from 'lucide-react';
import { getAssetPath } from '../../../utils/assets';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import { algorithmMarkdown } from '../../../data/algorithmMarkdown';

type SubSection = 'probe' | 'data' | 'algorithm' | 'color' | 'geus';

const Method: React.FC = () => {
  const [activeTab, setActiveTab] = useState<SubSection>('probe');
  const [isFlowchartOpen, setIsFlowchartOpen] = useState(false);

  const navItems = [
    { id: 'probe', label: 'The Probe', icon: Wrench },
    { id: 'data', label: 'Raw Data', icon: Database },
    { id: 'algorithm', label: 'Algorithmic Interface', icon: Cpu },
    { id: 'color', label: 'Color FRI', icon: Palette },
    { id: 'geus', label: 'GEUS FRI', icon: MapIcon },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'probe':
        return (
          <motion.div 
            key="probe"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-8"
          >
            <div className="bg-white p-10 rounded-3xl shadow-xl border border-slate-100">
              <h3 className="text-3xl font-black text-slate-800 mb-6 flex items-center gap-3">
                <Wrench className="text-action-blue" size={32} />
                How the Probe Works
              </h3>
              <p className="text-lg text-slate-600 leading-relaxed mb-8">
                The high-resolution subsurface redox probe is designed for rapid, in-situ characterization of geochemical gradients. 
                It utilizes multiple sensors to measure redox potential ($E_H$) and other parameters at a high frequency during insertion.
              </p>
              <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200 flex flex-col md:flex-row items-center justify-between gap-6">
                <div className="space-y-2">
                  <h4 className="font-bold text-slate-800 text-xl">Scientific Publication</h4>
                  <p className="text-slate-500">Read the full paper on the probe's design and validation in ACS ES&T Water.</p>
                </div>
                <a 
                  href="https://pubs.acs.org/doi/10.1021/acsestwater.4c00200" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="bg-action-blue text-white px-8 py-4 rounded-xl font-bold flex items-center gap-2 hover:bg-slate-800 transition-all shadow-lg"
                >
                  View Paper <ExternalLink size={18} />
                </a>
              </div>
            </div>
          </motion.div>
        );
      case 'data':
        return (
          <motion.div 
            key="data"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-8"
          >
            <div className="bg-white p-10 rounded-3xl shadow-xl border border-slate-100">
              <h3 className="text-3xl font-black text-slate-800 mb-6 flex items-center gap-3">
                <Database className="text-action-blue" size={32} />
                Raw Data Repository
              </h3>
              <p className="text-lg text-slate-600 leading-relaxed mb-8">
                Access the complete dataset used in this study, including master geochemistry logs, lithological mappings, and redox index interfaces.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { name: 'Master Geochemistry', filename: 'Master_Geochemistry.csv' },
                  { name: 'Master Lithology', filename: 'Master_Lithology.csv' },
                  { name: 'Lithology Mapping', filename: 'Lithology_mapping.csv' },
                  { name: 'Color Mapping', filename: 'Color_mapping.csv' },
                  { name: 'GWT (Groundwater Table)', filename: 'GWT.csv' },
                  { name: 'Master Redox', filename: 'Master_Redox.csv' },
                  { name: 'Redox Index', filename: 'Redox_Index.csv' },
                  { name: 'Refined Human Interface', filename: 'Refined_Human_Interface.csv' },
                ].map((file) => (
                  <a 
                    key={file.filename} 
                    href={getAssetPath(`/downloads/${file.filename}`)}
                    download
                    className="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-100 hover:border-action-blue hover:bg-white transition-all group"
                  >
                    <span className="font-bold text-slate-700">{file.name}</span>
                    <Download size={20} className="text-slate-400 group-hover:text-action-blue transition-colors" />
                  </a>
                ))}
              </div>

              <div className="mt-8 space-y-4">
                <h4 className="font-black text-slate-800 uppercase tracking-widest text-sm">Geochemistry Reports (GEUS)</h4>
                <div className="flex flex-wrap gap-3">
                  {['DEMO', 'LOOP2', 'LOOP3', 'LOOP4', 'LOOP6'].map(site => (
                    <a 
                      key={site} 
                      href={getAssetPath(`/downloads/GEUS_Geochemistry_${site}.pdf`)}
                      download
                      className="px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-bold text-slate-600 flex items-center gap-2 hover:bg-slate-50 transition-all shadow-sm"
                    >
                      <FileText size={16} className="text-red-500" />
                      GEUS_{site}.pdf
                    </a>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        );
      case 'algorithm':
        return (
          <motion.div 
            key="algorithm"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-12"
          >
            <div className="bg-white p-4 md:p-10 rounded-3xl shadow-xl border border-slate-100 space-y-12">
              <div className="prose prose-slate max-w-none text-slate-800 leading-relaxed overflow-x-auto">
                <ReactMarkdown
                  remarkPlugins={[remarkMath]}
                  rehypePlugins={[rehypeKatex]}
                >
                  {algorithmMarkdown}
                </ReactMarkdown>
              </div>

              <div className="space-y-12">
                <div className="text-center border-b border-slate-100 pb-4">
                  <h4 className="text-2xl md:text-3xl font-black text-slate-800">Human vs. Algorithmic Interface Depth (m)</h4>
                </div>
                <img src={getAssetPath('/plots/method/stats_main_0.png')} className="w-full max-w-full h-auto rounded-2xl shadow-lg border border-slate-200" alt="Stats Plot" />
              </div>

              <div className="space-y-12">
                <div className="text-center border-b border-slate-100 pb-4">
                  <h4 className="text-2xl md:text-3xl font-black text-slate-800">--- LOGS WITH SINGLE INTERFACE (Primary Only) ---</h4>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {Array.from({ length: 6 }).map((_, i) => (
                    <img key={`single_${i}`} src={getAssetPath(`/plots/method/single_interface_${i}.png`)} className="w-full max-w-full h-auto rounded-xl shadow-md border border-slate-200" alt={`Single Interface ${i+1}`} />
                  ))}
                </div>
              </div>

              <div className="space-y-12">
                <div className="text-center border-b border-slate-100 pb-4">
                  <h4 className="text-2xl md:text-3xl font-black text-slate-800">--- LOGS WITH DUAL INTERFACES (Primary and Secondary) ---</h4>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {Array.from({ length: 6 }).map((_, i) => (
                    <img key={`dual_${i}`} src={getAssetPath(`/plots/method/dual_interface_${i}.png`)} className="w-full max-w-full h-auto rounded-xl shadow-md border border-slate-200" alt={`Dual Interface ${i+1}`} />
                  ))}
                </div>
              </div>

              <div className="space-y-12">
                <div className="text-center border-b border-slate-100 pb-4">
                  <h4 className="text-2xl md:text-3xl font-black text-slate-800">Complete set of logs and Algorithmic vs Human interfaces</h4>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {Array.from({ length: 87 }).map((_, i) => (
                    <img key={`all_${i}`} src={getAssetPath(`/plots/method/all_logs_final_${i}.png`)} className="w-full max-w-full h-auto rounded-xl shadow-sm border border-slate-100" alt={`All Logs ${i+1}`} />
                  ))}
                </div>
              </div>

            </div>
          </motion.div>
        );
      case 'color':
        return (
          <motion.div 
            key="color"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-8"
          >
            <div className="bg-white p-10 rounded-3xl shadow-xl border border-slate-100">
              <h3 className="text-3xl font-black text-slate-800 mb-6 flex items-center gap-3">
                <Palette className="text-action-blue" size={32} />
                Color Interface Detection
              </h3>
              <p className="text-lg text-slate-600 leading-relaxed mb-8">
                The color-based First Redox Interface (FRI) is identified following the methodology of Kim et al. (2025), leveraging sediment color as a proxy for redox state.
              </p>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <div className="space-y-6">
                   <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200">
                    <h4 className="font-bold text-slate-800 text-lg mb-2">Methodological Paper</h4>
                    <p className="text-slate-500 text-sm mb-4">Kim et al. 2025: Geochemical and sedimentological controls on redox interfaces.</p>
                    <a 
                      href="https://www.sciencedirect.com/science/article/pii/S0883292725002161" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-action-blue font-bold hover:underline"
                    >
                      Read on ScienceDirect <ExternalLink size={14} />
                    </a>
                  </div>
                  <div className="p-6 bg-white border border-slate-100 rounded-2xl shadow-sm">
                    <h4 className="font-black text-slate-800 uppercase tracking-widest text-xs mb-4">Color Logic</h4>
                    <ul className="space-y-3 text-sm text-slate-600">
                      <li className="flex items-start gap-2">
                        <ChevronRight className="text-action-blue mt-0.5" size={16} />
                        <span>Identification of the shallowest occurrence of reduced sediment colors (e.g., olive, gray, black).</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <ChevronRight className="text-action-blue mt-0.5" size={16} />
                        <span>Exclusion of localized reduced features in otherwise oxidized horizons.</span>
                      </li>
                    </ul>
                  </div>
                </div>
                
                <div className="bg-slate-100 rounded-3xl overflow-hidden border border-slate-200 aspect-square flex items-center justify-center relative group">
                  <div className="absolute inset-0 bg-slate-900/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center z-10 cursor-pointer" onClick={() => setIsFlowchartOpen(true)}>
                    <div className="flex flex-col items-center gap-2 text-white">
                      <Maximize2 size={32} />
                      <span className="font-black uppercase tracking-[0.2em] text-sm">View Full Flowchart</span>
                    </div>
                  </div>
                  <img 
                    src={getAssetPath('/2026_Color_FRI_Algorithm_Flowchart.png')} 
                    alt="Color FRI Algorithm Flowchart" 
                    className="w-full h-full object-contain p-4"
                  />
                </div>
              </div>
            </div>
          </motion.div>
        );
      case 'geus':
        return (
          <motion.div 
            key="geus"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-8"
          >
            <div className="bg-white p-10 rounded-3xl shadow-xl border border-slate-100">
              <h3 className="text-3xl font-black text-slate-800 mb-6 flex items-center gap-3">
                <MapIcon className="text-action-blue" size={32} />
                GEUS FRI (National Map)
              </h3>
              <p className="text-lg text-slate-600 leading-relaxed mb-8">
                The GEUS FRI interface represents the depth to the First Redox Interface as mapped in the Danish National Redox Model.
              </p>

              <div className="bg-slate-50 p-8 rounded-3xl border border-slate-200">
                <div className="flex flex-col md:flex-row gap-8 items-start">
                  <div className="flex-1 space-y-6">
                    <div className="space-y-2">
                      <h4 className="font-bold text-slate-800 text-xl">How was it found?</h4>
                      <p className="text-slate-600">
                        We extracted the FRI values directly from the national grid at the specific coordinates for each borehole shown in this platform. 
                        This allows for a direct comparison between our high-resolution probe results and the existing national-scale mapping.
                      </p>
                    </div>
                    
                    <div className="flex flex-col gap-4">
                      <h5 className="font-black text-slate-800 uppercase tracking-widest text-xs">Reference Paper</h5>
                      <a 
                        href="https://www.sciencedirect.com/science/article/pii/S0048969724046813" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="bg-white border border-slate-200 p-4 rounded-xl flex items-center justify-between hover:shadow-md transition-all group"
                      >
                        <div className="flex items-center gap-3">
                          <FileText className="text-slate-400 group-hover:text-action-blue" />
                          <span className="font-bold text-slate-700">National Redox Mapping Methodology</span>
                        </div>
                        <ExternalLink size={16} className="text-slate-300 group-hover:text-action-blue" />
                      </a>
                    </div>
                  </div>
                  
                  <div className="w-full md:w-64 bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center text-center">
                    <div className="w-16 h-16 bg-blue-100 text-action-blue rounded-full flex items-center justify-center mb-4">
                      <Info size={32} />
                    </div>
                    <h5 className="font-bold text-slate-800 mb-2">Spatial Matching</h5>
                    <p className="text-xs text-slate-500">Coordinate-based extraction from the 2024 National Map grid.</p>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-16 pb-24 px-4">
      {/* Introduction */}
      <section className="text-center space-y-6">
        <h2 className="text-5xl font-black text-slate-800 tracking-tight">Methodology & Transparency</h2>
        <p className="text-xl text-slate-500 max-w-3xl mx-auto leading-relaxed">
          Full transparency on the tools, data, and algorithms used to identify subsurface redox boundaries.
        </p>
      </section>

      {/* Navigation Tabs */}
      <div className="flex justify-center gap-2 md:gap-4 flex-wrap bg-white/50 p-2 rounded-3xl backdrop-blur-sm sticky top-4 z-50 shadow-sm border border-white/20">
        {navItems.map(item => (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id as SubSection)}
            className={`flex items-center gap-2 px-6 py-3 rounded-2xl font-black transition-all ${
              activeTab === item.id 
                ? 'bg-action-blue text-white shadow-xl' 
                : 'text-slate-500 hover:bg-white hover:text-slate-800'
            }`}
          >
            <item.icon size={18} />
            <span className="hidden sm:inline">{item.label}</span>
          </button>
        ))}
      </div>

      {/* Content Area */}
      <div className="min-h-[500px]">
        <AnimatePresence mode="wait">
          {renderContent()}
        </AnimatePresence>
      </div>

      {/* Flowchart Modal */}
      <AnimatePresence>
        {isFlowchartOpen && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-slate-900/95 z-[100] p-4 flex items-center justify-center"
            onClick={() => setIsFlowchartOpen(false)}
          >
            <button 
              className="absolute top-8 right-8 text-white hover:text-action-blue transition-colors"
              onClick={() => setIsFlowchartOpen(false)}
            >
              <X size={48} />
            </button>
            <motion.img 
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              src={getAssetPath('/2026_Color_FRI_Algorithm_Flowchart.png')} 
              className="max-w-full max-h-full object-contain shadow-2xl rounded-lg"
              alt="Color FRI Algorithm Flowchart Full Screen"
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Summary Footer */}
      <div className="bg-slate-900 rounded-[3rem] p-12 text-center text-white relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
          <div className="absolute top-10 left-10 w-64 h-64 bg-blue-500 rounded-full blur-[120px]" />
          <div className="absolute bottom-10 right-10 w-64 h-64 bg-emerald-500 rounded-full blur-[120px]" />
        </div>
        <h4 className="text-2xl font-black mb-4 relative z-10">Data Integrity Statement</h4>
        <p className="text-slate-400 max-w-2xl mx-auto relative z-10">
          All results shown on this platform are derived directly from the documented data sources and algorithms. 
          By providing access to raw logs and scientific foundations, we ensure the replicability and accountability of our findings.
        </p>
      </div>
    </div>
  );
};

export default Method;
