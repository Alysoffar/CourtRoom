COURTROOM_DIALOGUE_CSS = r"""
/* ================= RPG VISUAL NOVEL DIALOGUE BOX ================= */
.vn-dialogue-wrap {
    position: absolute;
    left: 20px;
    right: 20px;
    bottom: 16px;
    min-height: 132px;
    max-height: 152px;
    background: linear-gradient(180deg, rgba(16, 19, 30, 0.94) 0%, rgba(8, 10, 16, 0.98) 100%);
    border: 2px solid var(--gold);
    border-radius: 14px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.9), inset 0 0 20px rgba(229, 184, 105, 0.08);
    padding: 22px 22px 14px 22px;
    z-index: 10;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.vn-speaker-tag {
    position: absolute;
    top: -15px;
    left: 22px;
    padding: 5px 18px;
    border-radius: 8px;
    font-family: 'Cinzel', serif;
    font-weight: 800;
    font-size: 13px;
    letter-spacing: 1.5px;
    color: #fff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    gap: 8px;
}
.tag-pros { background: linear-gradient(90deg, #d9253d, #8f1224); border: 1.5px solid #ff9aa8; }
.tag-def  { background: linear-gradient(90deg, #1b76d1, #0e4682); border: 1.5px solid #90cbff; }
.tag-jury { background: linear-gradient(90deg, #b8821e, #734d08); border: 1.5px solid #ffe09e; }
.tag-idle { background: linear-gradient(90deg, #3a4054, #222634); border: 1.5px solid #8c93ab; }

.vn-round-pill {
    position: absolute;
    top: -13px;
    right: 22px;
    padding: 4px 12px;
    border-radius: 999px;
    background: #161925;
    border: 1px solid var(--gold);
    color: var(--gold);
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
}

.vn-text-body {
    font-size: 15px;
    line-height: 1.55;
    color: #f7f4ed;
    overflow-y: auto;
    max-height: 86px;
    padding-right: 8px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
}

.vn-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 6px;
    font-size: 11.5px;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
}
.vn-cursor {
    display: inline-block;
    color: var(--gold);
    animation: blinkCursor 0.9s infinite;
}
@keyframes blinkCursor {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
}

/* Sidebar & Card Polish */
.control-card {
    background: var(--panel-bg) !important;
    border: 1px solid var(--panel-border) !important;
    border-radius: 16px !important;
    padding: 14px !important;
}
.section-title h3 {
    color: var(--gold) !important;
    font-family: 'Cinzel', serif !important;
    letter-spacing: 1.5px !important;
    font-weight: 700 !important;
}
"""
