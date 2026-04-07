import React, { useEffect, useState, useMemo, useRef } from 'react';
import { getAssetPath } from '../../../utils/assets';
import plotAnimations from '../../../data/plot_animations.json';
import plotAnimationsDissolved from '../../../data/plot_animations_dissolved.json';

interface Props {
  boreholeId: string;
  isDissolved: boolean;
  isPlaying: boolean;
}

interface AnimationLine {
  color: string;
  path: (number[] | null | 'null')[];
}

const BoreholeChart: React.FC<Props> = ({ boreholeId, isDissolved, isPlaying }) => {
  const [frame, setFrame] = useState(0);
  const [isInView, setIsInView] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Normalize ID for lookup
  const baseId = boreholeId.replace('_DISSOLVED', '');
  const animationsSource = isDissolved ? plotAnimationsDissolved : plotAnimations;
  const animKey = isDissolved ? `dissolved_${baseId}` : baseId;
  const animData = useMemo(() => {
    return ((animationsSource as Record<string, AnimationLine[]>)[animKey] || []);
  }, [animationsSource, animKey]);

  const totalFrames = useMemo(() => {
    if (animData.length === 0) return 0;
    return animData[0].path.length;
  }, [animData]);

  // Intersection Observer to detect if the chart is in view
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsInView(entry.isIntersecting);
      },
      { threshold: 0.1 }
    );

    if (containerRef.current) {
      observer.observe(containerRef.current);
    }

    return () => observer.disconnect();
  }, []);

  // Animation Loop - only runs if isPlaying and isInView
  useEffect(() => {
    if (!isPlaying || !isInView || totalFrames === 0) return;

    const timer = setInterval(() => {
      setFrame(prev => (prev + 1) % totalFrames);
    }, 40);

    return () => clearInterval(timer);
  }, [isPlaying, isInView, totalFrames]);

  const imgSrc = getAssetPath(isDissolved ? `/plots/dissolved_${baseId}.png` : `/plots/${baseId}.png`);

  return (
    <div ref={containerRef} className="w-full flex justify-start bg-white min-h-[600px]">
      {/* Standardized Width Container (1500px) */}
      <div className="relative w-[1500px] min-w-[1500px] h-full bg-white">
        {/* The pixel-perfect PNG from notebook */}
        <img 
          src={imgSrc} 
          alt={`Plot for ${boreholeId}`}
          className="block w-full h-auto"
          loading="lazy"
          decoding="async"
        />
        
        {/* SVG Overlay for moving dots - matched exactly to the 1500px image width */}
        {isInView && (
          <svg 
            className="absolute inset-0 w-full h-full pointer-events-none"
            viewBox="0 0 100 100" 
            preserveAspectRatio="none"
          >
            {animData.map((line, i) => {
              const pos = line.path[frame];
              if (!pos || pos === 'null' || !Array.isArray(pos) || pos[0] === null) return null;
              
              // pos[0] is x-fraction (0 to 1), pos[1] is y-fraction (0 to 1)
              const x = pos[0] * 100;
              const y = (1 - pos[1]) * 100; 

              return (
                <g key={i}>
                  <circle 
                    cx={x} 
                    cy={y} 
                    r="0.8" 
                    fill={line.color} 
                    opacity="0.4"
                  />
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
        )}
      </div>
    </div>
  );
};

export default BoreholeChart;
