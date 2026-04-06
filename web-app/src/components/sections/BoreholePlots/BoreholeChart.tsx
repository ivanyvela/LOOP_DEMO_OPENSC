import React, { useEffect, useState, useMemo } from 'react';
import plotAnimations from '../../../data/plot_animations.json';
import plotAnimationsDissolved from '../../../data/plot_animations_dissolved.json';

interface Props {
  boreholeId: string;
  isDissolved: boolean;
  isPlaying: boolean;
}

const BoreholeChart: React.FC<Props> = ({ boreholeId, isDissolved, isPlaying }) => {
  const [frame, setFrame] = useState(0);
  
  // Normalize ID for lookup
  const baseId = boreholeId.replace('_DISSOLVED', '');
  const animationsSource = isDissolved ? plotAnimationsDissolved : plotAnimations;
  const animKey = isDissolved ? `dissolved_${baseId}` : baseId;
  const animData = (animationsSource as any)[animKey] || [];

  const totalFrames = useMemo(() => {
    if (animData.length === 0) return 0;
    return animData[0].path.length;
  }, [animData]);

  // Animation Loop
  useEffect(() => {
    if (!isPlaying || totalFrames === 0) return;

    const timer = setInterval(() => {
      setFrame(prev => (prev + 1) % totalFrames);
    }, 40);

    return () => clearInterval(timer);
  }, [isPlaying, totalFrames]);

  const imgSrc = isDissolved ? `/plots/dissolved_${baseId}.png` : `/plots/${baseId}.png`;

  return (
    <div className="relative w-full h-full overflow-hidden bg-white flex items-center justify-center">
      {/* The pixel-perfect PNG from notebook */}
      <img 
        src={imgSrc} 
        alt={`Plot for ${boreholeId}`}
        className="block max-w-full max-h-full object-contain"
      />
      
      {/* SVG Overlay for moving dots */}
      <svg 
        className="absolute w-full h-full pointer-events-none"
        style={{
          // We need to match the actual displayed image's dimensions if possible, 
          // but for now, we assume the svg fills the container or we use aspect-ratio logic.
          // Using preserveAspectRatio="xMidYMid meet" will help match the image's "object-contain" behavior.
        }}
        viewBox="0 0 100 100" 
        preserveAspectRatio="xMidYMid meet"
      >
        {animData.map((line: any, i: number) => {
          const pos = line.path[frame];
          if (!pos || pos === 'null' || pos[0] === null) return null;
          
          // pos[0] is x-fraction (0 to 1), pos[1] is y-fraction (bottom-up in original, need to flip if needed)
          // The export script likely used 0-1 range. Let's assume they are already normalized to the image.
          // Note: In CSS/SVG, y=0 is top. If notebook used bottom-up, we do 1 - y.
          const x = pos[0] * 100;
          const y = (1 - pos[1]) * 100; 

          return (
            <g key={i}>
              {/* Outer glow */}
              <circle 
                cx={x} 
                cy={y} 
                r="0.8" 
                fill={line.color} 
                opacity="0.4"
              />
              {/* Inner core */}
              <circle 
                cx={x} 
                cy={y} 
                r="0.3" 
                fill="white" 
                stroke={line.color}
                strokeWidth="0.1"
              />
            </g>
          );
        })}
      </svg>
    </div>
  );
};

export default BoreholeChart;
