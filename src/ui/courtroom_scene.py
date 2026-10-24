import html
import re

def _get_chibi_prosecutor_svg() -> str:
    """Custom SVG Chibi Opposition Prosecutor (Crimson Suit, Spiky Hair, Dramatic Point)."""
    return """
    <svg viewBox="0 0 160 170" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <filter id="shadowP" x="-10%" y="-10%" width="120%" height="120%">
                <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000" flood-opacity="0.6"/>
            </filter>
        </defs>
        <g filter="url(#shadowP)">
            <path d="M35 110 L20 162 L140 162 L125 110 Z" fill="#6b0f1c"/>
            <rect x="44" y="102" width="72" height="58" rx="14" fill="#9e192d" stroke="#ff6b7b" stroke-width="2"/>
            <polygon points="80,104 68,136 80,145 92,136" fill="#f7f4ef"/>
            <polygon points="80,104 73,122 87,122" fill="#d9d2c5"/>
            <circle cx="60" cy="122" r="5.5" fill="#f5c869" stroke="#704e0c" stroke-width="1.5"/>
            <path d="M110 112 L148 92 L152 104 L114 126 Z" fill="#9e192d" stroke="#ff6b7b" stroke-width="1.5"/>
            <circle cx="149" cy="96" r="8" fill="#ffe0c8"/>
            <rect x="148" y="91" width="11" height="5" rx="2.5" fill="#ffe0c8"/>
            <path d="M46 112 L30 135 L42 142 L52 122 Z" fill="#821223"/>
            <rect x="42" y="34" width="76" height="68" rx="32" fill="#ffe0c8" stroke="#d4a88c" stroke-width="2"/>
            <ellipse cx="56" cy="78" rx="6" ry="3" fill="#ff8da1" opacity="0.55"/>
            <ellipse cx="104" cy="78" rx="6" ry="3" fill="#ff8da1" opacity="0.55"/>
            <ellipse cx="63" cy="68" rx="7.5" ry="9" fill="#1b1924"/>
            <ellipse cx="97" cy="68" rx="7.5" ry="9" fill="#1b1924"/>
            <circle cx="65" cy="64" r="3" fill="#fff"/>
            <circle cx="99" cy="64" r="3" fill="#fff"/>
            <circle cx="61" cy="72" r="1.5" fill="#ff4b5c"/>
            <circle cx="95" cy="72" r="1.5" fill="#ff4b5c"/>
            <path d="M52 54 L72 60" stroke="#2c1d24" stroke-width="4" stroke-linecap="round"/>
            <path d="M108 54 L88 60" stroke="#2c1d24" stroke-width="4" stroke-linecap="round"/>
            <path d="M72 84 Q80 92 89 83 Z" fill="#b8293d"/>
            <path d="M36 62 C32 28, 62 14, 82 18 C105 14, 128 28, 124 62 C118 42, 106 36, 98 44 C90 30, 72 30, 62 46 C52 36, 42 44, 36 62 Z" fill="#2c2938" stroke="#524d66" stroke-width="2"/>
            <polygon points="80,10 68,28 92,26" fill="#2c2938"/>
            <polygon points="112,20 96,32 122,40" fill="#2c2938"/>
            <polygon points="46,22 64,32 36,42" fill="#2c2938"/>
        </g>
    </svg>
    """


def _get_chibi_jury_svg() -> str:
    """Custom SVG Chibi Supreme Judge / Jury (Black & Gold Judicial Robes, Crown/Laurel, Gavel)."""
    return """
    <svg viewBox="0 0 160 170" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <filter id="shadowJ" x="-10%" y="-10%" width="120%" height="120%">
                <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000" flood-opacity="0.6"/>
            </filter>
        </defs>
        <g filter="url(#shadowJ)">
            <path d="M38 104 L28 162 L132 162 L122 104 Z" fill="#1e2230" stroke="#e5b869" stroke-width="2.5"/>
            <polygon points="68,104 60,162 72,162 76,104" fill="#e5b869"/>
            <polygon points="92,104 100,162 88,162 84,104" fill="#e5b869"/>
            <polygon points="80,106 66,118 80,126 94,118" fill="#ffffff"/>
            <rect x="124" y="84" width="6" height="42" rx="3" transform="rotate(-22 124 84)" fill="#8c5828" stroke="#cfa063" stroke-width="1.5"/>
            <rect x="108" y="74" width="28" height="14" rx="4" transform="rotate(-22 122 81)" fill="#5c3614" stroke="#e5b869" stroke-width="2"/>
            <circle cx="126" cy="112" r="7.5" fill="#ffe0c8"/>
            <rect x="44" y="36" width="72" height="66" rx="30" fill="#ffe0c8" stroke="#d4a88c" stroke-width="2"/>
            <circle cx="42" cy="64" r="11" fill="#e8e6f0"/>
            <circle cx="40" cy="80" r="10" fill="#dad7e6"/>
            <circle cx="118" cy="64" r="11" fill="#e8e6f0"/>
            <circle cx="120" cy="80" r="10" fill="#dad7e6"/>
            <path d="M40 54 C40 22, 120 22, 120 54 C105 38, 55 38, 40 54 Z" fill="#f2f0f7" stroke="#c7c3d4" stroke-width="2"/>
            <polygon points="62,32 70,16 80,26 90,16 98,32" fill="#f5c869" stroke="#8a5e0b" stroke-width="1.5"/>
            <ellipse cx="64" cy="68" rx="6.5" ry="8" fill="#1b1924"/>
            <ellipse cx="96" cy="68" rx="6.5" ry="8" fill="#1b1924"/>
            <circle cx="66" cy="65" r="2.5" fill="#fff"/>
            <circle cx="98" cy="65" r="2.5" fill="#fff"/>
            <path d="M64 84 Q80 78 96 84 Q88 92 80 86 Q72 92 64 84 Z" fill="#d8d4e3"/>
            <path d="M55 56 Q64 52 72 57" stroke="#9e9ab0" stroke-width="3.5" fill="none" stroke-linecap="round"/>
            <path d="M105 56 Q96 52 88 57" stroke="#9e9ab0" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        </g>
    </svg>
    """


def _get_chibi_defense_svg() -> str:
    """Custom SVG Chibi Government Defense Attorney (Cobalt Blue Suit, Red Tie, Case File)."""
    return """
    <svg viewBox="0 0 160 170" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <filter id="shadowD" x="-10%" y="-10%" width="120%" height="120%">
                <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000" flood-opacity="0.6"/>
            </filter>
        </defs>
        <g filter="url(#shadowD)">
            <rect x="44" y="102" width="72" height="58" rx="14" fill="#16569c" stroke="#5cb8ff" stroke-width="2"/>
            <polygon points="80,102 68,128 80,148 92,128" fill="#ffffff"/>
            <polygon points="80,106 75,134 80,144 85,134" fill="#e02f44"/>
            <circle cx="98" cy="120" r="5" fill="#f5c869" stroke="#785208" stroke-width="1.5"/>
            <rect x="20" y="96" width="32" height="40" rx="4" transform="rotate(-12 20 96)" fill="#e8cfa2" stroke="#8c6732" stroke-width="2"/>
            <line x1="26" y1="106" x2="44" y2="103" stroke="#6e5023" stroke-width="2"/>
            <line x1="28" y1="114" x2="46" y2="111" stroke="#6e5023" stroke-width="2"/>
            <circle cx="38" cy="122" r="7.5" fill="#ffe0c8"/>
            <rect x="42" y="34" width="76" height="68" rx="32" fill="#ffe0c8" stroke="#d4a88c" stroke-width="2"/>
            <ellipse cx="56" cy="78" rx="6" ry="3" fill="#ff8da1" opacity="0.5"/>
            <ellipse cx="104" cy="78" rx="6" ry="3" fill="#ff8da1" opacity="0.5"/>
            <ellipse cx="63" cy="68" rx="7" ry="8.5" fill="#152438"/>
            <ellipse cx="97" cy="68" rx="7" ry="8.5" fill="#152438"/>
            <circle cx="65" cy="65" r="2.8" fill="#fff"/>
            <circle cx="99" cy="65" r="2.8" fill="#fff"/>
            <rect x="51" y="60" width="24" height="16" rx="4" fill="none" stroke="#e5b869" stroke-width="2"/>
            <rect x="85" y="60" width="24" height="16" rx="4" fill="none" stroke="#e5b869" stroke-width="2"/>
            <line x1="75" y1="66" x2="85" y2="66" stroke="#e5b869" stroke-width="2"/>
            <path d="M54 54 L72 56" stroke="#182030" stroke-width="3.5" stroke-linecap="round"/>
            <path d="M106 54 L88 56" stroke="#182030" stroke-width="3.5" stroke-linecap="round"/>
            <path d="M73 85 Q80 90 87 85" stroke="#a64b4b" stroke-width="3" fill="none" stroke-linecap="round"/>
            <path d="M38 60 C34 25, 68 14, 92 18 C115 20, 128 36, 122 60 C114 42, 100 36, 86 42 C72 32, 54 38, 38 60 Z" fill="#182030" stroke="#364663" stroke-width="2"/>
            <polygon points="34,30 58,28 42,48" fill="#182030"/>
            <polygon points="26,44 50,38 40,56" fill="#182030"/>
            <polygon points="84,12 70,26 98,24" fill="#182030"/>
        </g>
    </svg>
    """


def _clean_markdown_for_vn_box(raw_text: str) -> str:
    """Formats markdown into clean HTML for the RPG dialogue box without cutting off text."""
    if not raw_text:
        return ""
    cleaned = html.escape(raw_text)
    cleaned = re.sub(r"#{1,6}\s*", "", cleaned)
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", cleaned)
    cleaned = cleaned.replace("\n", "<br>")
    return cleaned


def render_3d_courtroom(
    active_role: str = "IDLE",
    speaker_title: str = "CHAMBER CLERK",
    dialogue_text: str = "Chambers are set. Select a jurisdiction and indictment on the left, then click <b>CONVENE COURT</b> to begin the tribunal.",
    round_label: str = "PRE-TRIAL",
    country: str = "Egypt",
    pros_model: str = "Prosecutor AI",
    def_model: str = "Defense AI",
    jury_model: str = "Supreme Jury AI",
) -> str:
    """Renders the 2.5D/3D courtroom stage, Chibi avatars, spotlights, and RPG dialogue box."""
    is_pros = active_role == "PROSECUTION"
    is_def = active_role == "DEFENSE"
    is_jury = active_role == "JURY"
    is_idle = active_role == "IDLE"

    pros_state = "speaking" if is_pros else ("dimmed" if not is_idle else "")
    def_state = "speaking" if is_def else ("dimmed" if not is_idle else "")
    jury_state = "speaking" if is_jury else ("dimmed" if not is_idle else "")

    if is_pros:
        tag_class = "tag-pros"
        speaker_icon = "🔴"
    elif is_def:
        tag_class = "tag-def"
        speaker_icon = "🔵"
    elif is_jury:
        tag_class = "tag-jury"
        speaker_icon = "⚖️"
    else:
        tag_class = "tag-idle"
        speaker_icon = "🏛️"

    safe_country = html.escape(country or "Sovereign State")
    safe_pros_model = html.escape((pros_model or "Prosecutor").split("/")[-1][:20])
    safe_def_model = html.escape((def_model or "Defense").split("/")[-1][:20])
    safe_jury_model = html.escape((jury_model or "Supreme Jury").split("/")[-1][:22])

    formatted_dialogue = (
        dialogue_text
        if is_idle
        else _clean_markdown_for_vn_box(dialogue_text)
    )

    return f"""
    <div class="court-viewport">
        <div class="court-wall">
            <div class="wall-crest">
                <div class="wall-crest-circle">⚖️</div>
                <div class="wall-crest-title">TRIBUNAL OF {safe_country.upper()}</div>
            </div>
        </div>

        <div class="court-floor"></div>

        <div class="spotlight spot-pros {'active' if is_pros else ''}"></div>
        <div class="spotlight spot-jury {'active' if is_jury else ''}"></div>
        <div class="spotlight spot-def {'active' if is_def else ''}"></div>

        <!-- SUPREME JURY STATION -->
        <div class="station station-jury {jury_state}">
            <div class="callout-badge callout-jury">⚖️ FINAL VERDICT!</div>
            <div class="chibi-sprite">
                {_get_chibi_jury_svg()}
            </div>
            <div class="podium-3d podium-jury">
                <div class="podium-plaque">⚖ SUPREME JURY</div>
                <div class="podium-sub">{safe_jury_model}</div>
            </div>
        </div>

        <!-- PROSECUTION STATION -->
        <div class="station station-pros {pros_state}">
            <div class="callout-badge callout-pros">💥 OBJECTION!</div>
            <div class="chibi-sprite">
                {_get_chibi_prosecutor_svg()}
            </div>
            <div class="podium-3d podium-side podium-pros">
                <div class="podium-plaque" style="border-color:#ff6b7b;color:#ff8da1;">🔴 PROSECUTION</div>
                <div class="podium-sub">{safe_pros_model}</div>
            </div>
        </div>

        <!-- DEFENSE STATION -->
        <div class="station station-def {def_state}">
            <div class="callout-badge callout-def">🛡️ HOLD IT!</div>
            <div class="chibi-sprite">
                {_get_chibi_defense_svg()}
            </div>
            <div class="podium-3d podium-side podium-def">
                <div class="podium-plaque" style="border-color:#5cb8ff;color:#90cbff;">🔵 DEFENSE</div>
                <div class="podium-sub">{safe_def_model}</div>
            </div>
        </div>

        <!-- VISUAL NOVEL DIALOGUE BOX -->
        <div class="vn-dialogue-wrap">
            <div class="vn-speaker-tag {tag_class}">
                <span>{speaker_icon}</span>
                <span>{html.escape(speaker_title)}</span>
            </div>
            <div class="vn-round-pill">{html.escape(round_label)}</div>
            <div class="vn-text-body">
                {formatted_dialogue} <span class="vn-cursor">▼</span>
            </div>
            <div class="vn-footer">
                <span>JURISDICTION: {safe_country.upper()}</span>
                <span>LIVE COURTROOM FEED</span>
            </div>
        </div>
    </div>
    """


