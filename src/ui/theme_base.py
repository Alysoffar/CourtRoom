COURTROOM_BASE_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Plus+Jakarta+Sans:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap');

:root {
    --bg-dark: #090a0f;
    --panel-bg: #12151f;
    --panel-border: #2a2f42;
    --gold: #e5b869;
    --gold-glow: rgba(229, 184, 105, 0.35);
    --ink: #f4f1ea;
    --muted: #9aa0b5;
}

.gradio-container {
    max-width: 1520px !important;
    background: radial-gradient(circle at 50% 0%, #1a162b 0%, #090a0f 75%) !important;
    color: var(--ink) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Header Banner */
.tribunal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 28px;
    margin-bottom: 14px;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(44, 34, 24, 0.85) 0%, rgba(18, 21, 31, 0.95) 60%);
    border: 1px solid rgba(229, 184, 105, 0.35);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6);
}
.tribunal-header h1 {
    font-family: 'Cinzel', serif;
    font-size: 28px;
    font-weight: 800;
    color: var(--gold);
    margin: 0;
    letter-spacing: 2px;
    text-shadow: 0 2px 12px rgba(229, 184, 105, 0.4);
}
.tribunal-header p {
    margin: 4px 0 0;
    color: var(--muted);
    font-size: 13.5px;
}
.header-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(229, 184, 105, 0.12);
    border: 1px solid var(--gold);
    color: var(--gold);
}

"""
