import { motion } from 'framer-motion';

export const ShowcaseGraphic = () => (
  <motion.div
    initial="hidden"
    animate="visible"
    variants={{
      hidden: { opacity: 0 },
      visible: { opacity: 1, transition: { staggerChildren: 0.1 } },
    }}
    className="relative w-full max-w-lg mx-auto"
  >
    <svg viewBox="0 0 400 400" className="w-full h-full">
      {/* Base Grid and Glow */}
      <defs>
        <filter id="glow">
          <feGaussianBlur stdDeviation="3.5" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        <radialGradient id="grad1" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
          <stop offset="0%" style={{ stopColor: 'var(--color-primary)', stopOpacity: 0.3 }} />
          <stop offset="100%" style={{ stopColor: 'var(--color-background)', stopOpacity: 0 }} />
        </radialGradient>
      </defs>
      <rect width="400" height="400" fill="url(#grad1)" />

      {/* Animated paths representing data flow */}
      <Path d="M 50 350 Q 200 200 350 50" delay={0.2} />
      <Path d="M 50 50 Q 200 200 350 350" delay={0.4} />
      <Path d="M 200 50 Q 100 200 200 350" delay={0.6} />
      <Path d="M 50 200 Q 200 300 350 200" delay={0.8} />

      {/* Nodes representing AI, emails, sheets */}
      <Node cx="50" cy="50" delay={0.3} />
      <Node cx="350" cy="50" delay={0.5} />
      <Node cx="50" cy="350" delay={0.7} />
      <Node cx="350" cy="350" delay={0.9} />
      <Node cx="200" cy="200" r={8} delay={0.1} />
    </svg>
  </motion.div>
);

const Path = ({ d, delay }) => (
  <motion.path
    d={d}
    fill="none"
    stroke="var(--color-primary)"
    strokeWidth="2"
    strokeOpacity="0.4"
    initial={{ pathLength: 0 }}
    animate={{ pathLength: 1 }}
    transition={{ duration: 1.5, ease: "easeInOut", delay }}
  />
);

const Node = ({ cx, cy, r = 5, delay }) => (
  <motion.circle
    cx={cx}
    cy={cy}
    r={r}
    fill="var(--color-primary)"
    style={{ filter: 'url(#glow)' }}
    initial={{ scale: 0 }}
    animate={{ scale: 1 }}
    transition={{ duration: 0.5, ease: "backOut", delay }}
  />
);

// We need to inject the colors as CSS variables for the SVG to use them
export const InjectColors = () => (
  <style>{`
    :root {
      --color-primary: #FF5722;
      --color-background: #F5F5F5;
    }
  `}</style>
); 