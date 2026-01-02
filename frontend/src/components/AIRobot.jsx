export default function AIRobot() {
  return (
    <svg
      width="320"
      height="420"
      viewBox="0 0 320 420"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="drop-shadow-[0_0_40px_rgba(56,189,248,0.7)]"
    >
      {/* Head */}
      <rect x="80" y="20" rx="40" ry="40" width="160" height="120" fill="#0f172a" stroke="#38bdf8" strokeWidth="3"/>
      <circle cx="130" cy="80" r="10" fill="#38bdf8"/>
      <circle cx="190" cy="80" r="10" fill="#38bdf8"/>

      {/* Body */}
      <rect x="90" y="150" rx="30" width="140" height="160" fill="#020617" stroke="#38bdf8" strokeWidth="3"/>

      {/* Core */}
      <circle cx="160" cy="230" r="22" fill="url(#coreGlow)"/>

      {/* Arms */}
      <rect x="40" y="170" rx="18" width="40" height="120" fill="#020617" stroke="#38bdf8" strokeWidth="3"/>
      <rect x="240" y="170" rx="18" width="40" height="120" fill="#020617" stroke="#38bdf8" strokeWidth="3"/>

      {/* Legs */}
      <rect x="110" y="320" rx="16" width="40" height="80" fill="#020617" stroke="#38bdf8" strokeWidth="3"/>
      <rect x="170" y="320" rx="16" width="40" height="80" fill="#020617" stroke="#38bdf8" strokeWidth="3"/>

      {/* Glow */}
      <defs>
        <radialGradient id="coreGlow">
          <stop offset="0%" stopColor="#38bdf8"/>
          <stop offset="100%" stopColor="#020617"/>
        </radialGradient>
      </defs>
    </svg>
  );
}
