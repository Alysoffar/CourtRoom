COURTROOM_STAGE_CSS = r"""
/* ================= 3D COURTROOM STAGE ================= */
.court-viewport {
    position: relative;
    width: 100%;
    height: 540px;
    border-radius: 20px;
    overflow: hidden;
    border: 2px solid #4a3b28;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.85), inset 0 0 80px rgba(0, 0, 0, 0.75);
    background: #120d0a;
    perspective: 950px;
    user-select: none;
}

/* Back Wall & Pillars */
.court-wall {
    position: absolute;
    inset: 0 0 32% 0;
    background:
        repeating-linear-gradient(
            90deg,
            rgba(255, 255, 255, 0.02) 0px,
            rgba(255, 255, 255, 0.02) 2px,
            transparent 2px,
            transparent 80px
        ),
        linear-gradient(180deg, #1b1512 0%, #2c1e16 55%, #1d140f 100%);
    border-bottom: 6px solid #6b4c2b;
    z-index: 1;
}

.wall-crest {
    position: absolute;
    top: 18px;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    z-index: 2;
}
.wall-crest-circle {
    width: 68px;
    height: 68px;
    margin: 0 auto;
    border-radius: 50%;
    background: radial-gradient(circle, #5e4420 0%, #261b0c 100%);
    border: 3px solid var(--gold);
    box-shadow: 0 0 25px var(--gold-glow);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
}
.wall-crest-title {
    margin-top: 6px;
    font-family: 'Cinzel', serif;
    font-size: 11px;
    letter-spacing: 5px;
    color: var(--gold);
    opacity: 0.85;
}

/* 3D Perspective Floor */
.court-floor {
    position: absolute;
    left: -15%;
    right: -15%;
    bottom: -18%;
    height: 62%;
    background:
        linear-gradient(180deg, rgba(0,0,0,0.65) 0%, transparent 40%),
        repeating-linear-gradient(
            90deg,
            rgba(229, 184, 105, 0.06) 0px,
            rgba(229, 184, 105, 0.06) 2px,
            transparent 2px,
            transparent 90px
        ),
        repeating-linear-gradient(
            0deg,
            rgba(229, 184, 105, 0.05) 0px,
            rgba(229, 184, 105, 0.05) 2px,
            transparent 2px,
            transparent 55px
        ),
        radial-gradient(circle at 50% 20%, #3a191f 0%, #1d1118 60%, #0d090c 100%);
    transform: rotateX(58deg);
    transform-origin: top center;
    z-index: 1;
}

/* Dynamic Spotlights */
.spotlight {
    position: absolute;
    top: -40px;
    width: 240px;
    height: 420px;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.4s ease;
    z-index: 2;
    filter: blur(8px);
}
.spotlight.active {
    opacity: 1;
}
.spot-pros {
    left: 6%;
    background: conic-gradient(from 165deg at 50% 0%, transparent 0deg, rgba(255, 75, 92, 0.28) 20deg, transparent 40deg);
}
.spot-jury {
    left: calc(50% - 120px);
    background: conic-gradient(from 160deg at 50% 0%, transparent 0deg, rgba(229, 184, 105, 0.30) 20deg, transparent 40deg);
}
.spot-def {
    right: 6%;
    background: conic-gradient(from 155deg at 50% 0%, transparent 0deg, rgba(56, 182, 255, 0.28) 20deg, transparent 40deg);
}

/* ================= CHIBI STATIONS ================= */
.station {
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), filter 0.35s ease;
    z-index: 3;
}
.station.dimmed {
    filter: brightness(0.55) saturate(0.75);
}
.station.speaking {
    filter: brightness(1.12) drop-shadow(0 0 22px rgba(255, 255, 255, 0.22));
    z-index: 5;
}
.station.speaking .chibi-sprite {
    animation: chibiBounce 0.65s ease-in-out infinite alternate;
}

@keyframes chibiBounce {
    0%   { transform: translateY(0px) scale(1); }
    100% { transform: translateY(-9px) scale(1.04); }
}

/* Positions */
.station-jury {
    top: 62px;
    left: 50%;
    transform: translateX(-50%);
}
.station-pros {
    bottom: 155px;
    left: 7%;
}
.station-def {
    bottom: 155px;
    right: 7%;
}

/* Speech Callout Bubble ("OBJECTION!", "VERDICT!", etc.) */
.callout-badge {
    position: absolute;
    top: -28px;
    padding: 4px 12px;
    border-radius: 8px;
    font-family: 'Cinzel', serif;
    font-weight: 800;
    font-size: 12px;
    letter-spacing: 1.5px;
    color: #fff;
    opacity: 0;
    transform: scale(0.6) translateY(10px);
    transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 6px 18px rgba(0,0,0,0.65);
    white-space: nowrap;
    z-index: 8;
}
.station.speaking .callout-badge {
    opacity: 1;
    transform: scale(1) translateY(0);
}
.callout-pros { background: linear-gradient(135deg, #ff2a4b, #b01028); border: 2px solid #ffd1d8; }
.callout-def  { background: linear-gradient(135deg, #1d8cf8, #0b4f9c); border: 2px solid #cce7ff; }
.callout-jury { background: linear-gradient(135deg, #d89b2b, #875809); border: 2px solid #fff0c2; }

/* Chibi Wrapper */
.chibi-sprite {
    width: 145px;
    height: 155px;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    position: relative;
    z-index: 3;
}
.station-jury .chibi-sprite {
    width: 135px;
    height: 140px;
}

/* 3D Wooden Benches / Podiums */
.podium-3d {
    position: relative;
    margin-top: -18px;
    border-radius: 8px 8px 4px 4px;
    background: linear-gradient(180deg, #6e4826 0%, #3d2512 65%, #241509 100%);
    border-top: 4px solid #c99652;
    border-left: 2px solid #8a5c32;
    border-right: 2px solid #8a5c32;
    border-bottom: 3px solid #160c05;
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.85);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 4;
}
.podium-jury {
    width: 250px;
    height: 68px;
}
.podium-side {
    width: 195px;
    height: 64px;
}
.podium-pros {
    transform: perspective(400px) rotateY(14deg);
}
.podium-def {
    transform: perspective(400px) rotateY(-14deg);
}
.podium-plaque {
    padding: 3px 12px;
    border-radius: 4px;
    background: rgba(12, 10, 8, 0.82);
    border: 1px solid var(--gold);
    font-family: 'Cinzel', serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: var(--gold);
}
.podium-sub {
    font-size: 10px;
    color: #d6caba;
    margin-top: 2px;
    opacity: 0.85;
}
"""
