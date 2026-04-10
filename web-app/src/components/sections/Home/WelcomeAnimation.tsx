import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getAssetPath } from '../../../utils/assets';

interface Scene {
  id: number;
  text: React.ReactNode;
  image: string | null;
  duration: number; // in milliseconds
}

const scenes: Scene[] = [
  {
    id: 1,
    text: <p><strong>Welcome to the Redox Probe Open Science Platform</strong><br/>Let us guide you through what this site is about. After years of development, we published a paper in 2025.</p>,
    image: 'image 1.png',
    duration: 8000,
  },
  {
    id: 2,
    text: <p>The paper shows that measuring soil redox continuously with depth was possible and electrochemically sound.</p>,
    image: 'image 2.png',
    duration: 7000,
  },
  {
    id: 3,
    text: <p>This is done with the Redox Probe.</p>,
    image: 'image 3.png',
    duration: 4000,
  },
  {
    id: 4,
    text: <p>Which is pushed into the soil by a rig, thus rendering its redox signature.</p>,
    image: 'image 4.png',
    duration: 6000,
  },
  {
    id: 5,
    text: <p>In this work, we manually identified three main sections: oxidized, transition, and reduced, and placed the redox boundary at where the transition and reduced zones meet.</p>,
    image: 'image 5.png',
    duration: 9000,
  },
  {
    id: 6,
    text: <p>But in the publication, we did not compare any of the redox logs to the actual geology of the sites. This is what we are doing now, and we are starting by showing it on this site. In the <strong>Borehole Plots</strong> section you can see a myriad of parameters corresponding to a single borehole.</p>,
    image: 'image 6.PNG',
    duration: 12000,
  },
  {
    id: 7,
    text: <p>Specifically, we are highlighting the relation between the measured redox (Eh) by the probe.</p>,
    image: 'image 7.PNG',
    duration: 6000,
  },
  {
    id: 8,
    text: <p>and the nitrate concentration.</p>,
    image: 'image 8.PNG',
    duration: 7000,
  },
  {
    id: 9,
    text: <p>One important aspect of the plots is the placement of interfaces. How each of these interfaces has been determined can be read in detail in the <strong>Method</strong> section. First, let's take a look at the redox interface.</p>,
    image: 'image 9.PNG',
    duration: 10000,
  },
  {
    id: 10,
    text: <p>This interface is no longer placed manually by a human, but automatically by a very simple algorithm that looks at where the biggest changes occur within a couple extra conditions.</p>,
    image: 'image 9_1.png',
    duration: 10000,
  },
  {
    id: 11,
    text: <p>These algorithmic results are almost identical to the ones obtained in the 2025 redox paper.</p>,
    image: 'image 9_2.png',
    duration: 7000,
  },
  {
    id: 12,
    text: <p>Then, we have the color interface.</p>,
    image: 'image 10.PNG',
    duration: 4000,
  },
  {
    id: 13,
    text: <p>This interface has been determined by replicating a paper from GEUS scientist Hyojin Kim from 2025.</p>,
    image: 'image 10_1.png',
    duration: 7000,
  },
  {
    id: 14,
    text: <p>Which we replicated for the boreholes presented here.</p>,
    image: 'image 10_2.png',
    duration: 7000,
  },
  {
    id: 15,
    text: <p>Then there is the GEUS FRI interface.</p>,
    image: 'image 11.PNG',
    duration: 4000,
  },
  {
    id: 16,
    text: <p>This is the depth at which the Geological Survey of Denmark and Greenland (GEUS) has placed the boundary in the FRI map.</p>,
    image: 'image 11_1.png',
    duration: 8000,
  },
  {
    id: 17,
    text: <p>Finally, you can see how good the different boundaries are at passing different nitrate reduction tests in the <strong>Nitrate Reduction</strong> section.</p>,
    image: 'image 12.png',
    duration: 8000,
  }
];

const WelcomeAnimation: React.FC = () => {
  const [currentSceneIndex, setCurrentSceneIndex] = useState(0);

  useEffect(() => {
    const scene = scenes[currentSceneIndex];
    const timer = setTimeout(() => {
      setCurrentSceneIndex((prev) => (prev + 1) % scenes.length);
    }, scene.duration);

    return () => clearTimeout(timer);
  }, [currentSceneIndex]);

  const scene = scenes[currentSceneIndex];

  return (
    <div className="w-full bg-slate-900 rounded-3xl shadow-2xl overflow-hidden border-8 border-slate-800 flex flex-col">
      {/* Text Area (Top) */}
      <div className="w-full bg-slate-800 p-6 md:p-8 flex flex-col justify-center text-slate-200 z-10 border-b border-slate-700 min-h-[140px]">
        <div className="relative w-full text-center max-w-4xl mx-auto flex items-center justify-center min-h-[4rem]">
          <AnimatePresence mode="wait">
            <motion.div
              key={scene.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.4 }}
              className="text-lg md:text-xl leading-relaxed"
            >
              {scene.text}
            </motion.div>
          </AnimatePresence>
        </div>
        
        {/* Progress indicators */}
        <div className="flex gap-1.5 mt-6 max-w-2xl mx-auto w-full">
          {scenes.map((_, idx) => (
            <div 
              key={idx} 
              className={`h-2 flex-1 rounded-full transition-all duration-300 ${idx === currentSceneIndex ? 'bg-[#2980b9] scale-y-125' : 'bg-slate-600 hover:bg-slate-500'}`}
              onClick={() => setCurrentSceneIndex(idx)}
              style={{ cursor: 'pointer' }}
              title={`Scene ${idx + 1}`}
            />
          ))}
        </div>
      </div>

      {/* Image Area (Bottom) */}
      <div className="w-full relative bg-slate-900 flex items-center justify-center p-4 md:p-8 h-[60vh] min-h-[400px] overflow-hidden">
        <AnimatePresence mode="wait">
          {scene.image ? (
            <motion.img
              key={scene.id}
              src={getAssetPath(`/welcome/${scene.image}`)}
              alt={`Scene presentation for slide ${scene.id}`}
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.02 }}
              transition={{ duration: 0.5 }}
              className="object-contain max-w-full max-h-full rounded-xl shadow-lg border border-slate-700/50"
            />
          ) : (
            <motion.div 
              key="empty"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center text-slate-600"
            >
              <div className="w-24 h-24 mb-4 opacity-50">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
              </div>
              <p className="text-xl">Redox Probe Data Platform</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default WelcomeAnimation;