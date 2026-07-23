import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Voice Console", page_icon="🎙️", layout="centered")

# ---- Config ----
def get_secret(key, default=""):
    try:
        return st.secrets.get(key, default)
    except Exception:
        # No secrets.toml file present at all — use default.
        return default

public_key = get_secret("VAPI_PUBLIC_KEY", "")
assistant_id = get_secret("VAPI_ASSISTANT_ID", "")

# ---- Sidebar: console modules ----
with st.sidebar:
    st.markdown('<div class="module-label">Module 01 — Appearance</div>', unsafe_allow_html=True)
    theme = st.selectbox("Theme", ["dark", "light"], index=0)
    accent_color = st.color_picker("Accent color", "#E8A33D")
    st.markdown('<hr class="hairline"/>', unsafe_allow_html=True)

    st.markdown('<div class="module-label">Module 02 — Behavior</div>', unsafe_allow_html=True)
    show_transcript = st.checkbox("Show live transcript", value=True)
    st.markdown('<hr class="hairline"/>', unsafe_allow_html=True)

    st.markdown('<div class="module-label">Module 03 — Placement</div>', unsafe_allow_html=True)
    size = st.selectbox("Widget size", ["tiny", "compact", "full"], index=2)
    position = st.selectbox(
        "Position (only matters if size ≠ full)",
        ["bottom-right", "bottom-left", "top-right", "top-left"],
        index=0,
    )

status_ready = bool(public_key and assistant_id)
status_text = "READY" if status_ready else "KEY MISSING"
status_dot = "var(--accent)" if status_ready else "#8A5A5A"

# ---- Global styling ----
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap');

    :root {{
        --accent: {accent_color};
        --bg: #10141A;
        --panel: #1B2129;
        --text: #ECE8E1;
        --muted: #6B7684;
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        background-color: var(--bg);
        color: var(--text);
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stSidebar"] {{
        background-color: var(--panel);
        border-right: 1px solid rgba(255,255,255,0.06);
    }}

    .module-label {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--muted);
        margin: 0.4rem 0 0.6rem 0;
    }}

    .hairline {{
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 1.1rem 0;
    }}

    [data-testid="stSidebar"] label {{
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: var(--text) !important;
    }}

    /* ---- Nameplate header ---- */
    .nameplate {{
        margin-top: 0.5rem;
        margin-bottom: 1.6rem;
    }}
    .eyebrow {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--muted);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }}
    .status-dot {{
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: {status_dot};
        box-shadow: 0 0 8px {status_dot};
        display: inline-block;
    }}
    .headline {{
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 2.6rem;
        line-height: 1.05;
        color: var(--text);
        margin: 0;
        letter-spacing: -0.01em;
    }}
    .subhead {{
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: var(--muted);
        margin-top: 0.6rem;
        max-width: 34ch;
    }}

    /* ---- Waveform hero ---- */
    .waveform {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        height: 88px;
        margin: 2rem 0 1.8rem 0;
        padding: 0 1rem;
        border-top: 1px solid rgba(255,255,255,0.07);
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }}
    .waveform .bar {{
        width: 4px;
        border-radius: 3px;
        background: var(--accent);
        opacity: 0.85;
        animation: breathe 1.8s ease-in-out infinite;
    }}
    @keyframes breathe {{
        0%, 100% {{ height: 10px; opacity: 0.45; }}
        50% {{ height: var(--peak, 46px); opacity: 0.95; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
        .waveform .bar {{ animation: none; height: 24px; }}
    }}

    .console-note {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        color: var(--muted);
        text-align: center;
        letter-spacing: 0.04em;
        margin-top: -0.6rem;
    }}

    #vapi-parent-container {{
        display: flex;
        justify-content: center;
        padding-top: 1.2rem;
    }}

    footer {{visibility: hidden;}}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Nameplate header ----
st.markdown(
    f"""
    <div class="nameplate">
        <div class="eyebrow"><span class="status-dot"></span>STATUS · {status_text}</div>
        <div class="headline">Voice Console</div>
        <div class="subhead">A direct line to your assistant — no dial tone, just talk.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---- Waveform hero (idle "breathing" bars, heights staggered for a live feel) ----
peaks = [22, 40, 30, 52, 26, 44, 20, 36, 48, 24, 32, 42, 18]
bars_html = "".join(
    f'<div class="bar" style="--peak:{p}px; animation-delay:{i * 0.09:.2f}s;"></div>'
    for i, p in enumerate(peaks)
)
st.markdown(f'<div class="waveform">{bars_html}</div>', unsafe_allow_html=True)
st.markdown('<div class="console-note">IDLE — MIC OPEN ON START</div>', unsafe_allow_html=True)

if not public_key or not assistant_id:
    st.error(
        "Missing **PUBLIC_KEY** or **ASSISTANT_ID**. "
        "Add them to your `.streamlit/secrets.toml` file, e.g.\n\n"
        "```toml\n"
        "PUBLIC_KEY = \"your-public-key\"\n"
        "ASSISTANT_ID = \"your-assistant-id\"\n"
        "```"
    )
    st.stop()

# ---- Sandbox Breakout Embed Script ----
# This script injects the Vapi widget directly into the main browser window (parent),
# ensuring that standard browser microphone permissions work perfectly.
sandbox_breakout_html = f"""
<script>
    const parentDoc = window.parent.document;

    // Check if the script is already loaded in the parent to prevent duplicates
    if (!parentDoc.getElementById("vapi-script")) {{
        const script = parentDoc.createElement("script");
        script.id = "vapi-script";
        script.src = "https://unpkg.com/@vapi-ai/client-sdk-react/dist/embed/widget.umd.js";
        script.async = true;
        script.defer = true;
        parentDoc.head.appendChild(script);
    }}

    // Check if the widget elements already exist, otherwise create them
    let container = parentDoc.getElementById("vapi-parent-container");
    if (!container) {{
        container = parentDoc.createElement("div");
        container.id = "vapi-parent-container";

        // Find Streamlit's main block container to append our widget cleanly
        const mainContent = parentDoc.querySelector(".main .block-container");
        if (mainContent) {{
            mainContent.appendChild(container);
        }} else {{
            parentDoc.body.appendChild(container);
        }}
    }}

    // Update or inject the widget configurations dynamically
    container.innerHTML = `
      <vapi-widget
        public-key="{public_key}"
        assistant-id="{assistant_id}"
        mode="chat"
        theme="{theme}"
        accent-color="{accent_color}"
        cta-button-color="{accent_color}"
        cta-button-text-color="#ffffff"
        border-radius="large"
        size="{size}"
        position="{position}"
        title="Voice Assistant"
        start-button-text="Start Call"
        end-button-text="End Call"
        voice-show-transcript="{str(show_transcript).lower()}"
      ></vapi-widget>
    `;
</script>
"""

# Call the component with 0 height so it executes seamlessly in the background
components.html(sandbox_breakout_html, height=0)

st.markdown('<div class="console-note" style="margin-top:1.6rem;">WIDGET ARMED — USE PANEL ABOVE TO TALK</div>', unsafe_allow_html=True)

st.markdown('<hr class="hairline"/>', unsafe_allow_html=True)
