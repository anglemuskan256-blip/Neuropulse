"""
NeuroPulse - AI Mental Health Monitoring System
Streamlit Version
"""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime

# ── Path setup ────────────────────────────────────────────────────────────────
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "app"))

# ── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="NeuroPulse — Mental Health Monitor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

/* ── Dark background ── */
.stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.15) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero-sub {
    color: #a5b4fc;
    font-size: 1.1rem;
    margin-top: 0.5rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 50px;
    padding: 0.3rem 1rem;
    color: #a5b4fc;
    font-size: 0.85rem;
    margin-top: 1rem;
}

/* ── Section cards ── */
.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
}
.card-title {
    color: #e2e8f0;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Result big badge ── */
.result-badge {
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.result-emoji { font-size: 3.5rem; }
.result-level { font-size: 2rem; font-weight: 800; margin: 0.5rem 0; }
.result-desc  { font-size: 1rem; opacity: 0.85; }

/* ── Metric pills ── */
.metric-pill {
    background: rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}
.metric-pill .val { font-size: 1.8rem; font-weight: 700; color: #a5b4fc; }
.metric-pill .lbl { font-size: 0.78rem; color: #94a3b8; margin-top: 0.3rem; }

/* ── Recommendation cards ── */
.rec-card {
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    border-left: 4px solid;
}
.rec-card.natural  { background: rgba(16,185,129,0.1); border-color: #10b981; }
.rec-card.otc      { background: rgba(245,158,11,0.1);  border-color: #f59e0b; }
.rec-card.pro      { background: rgba(99,102,241,0.1);  border-color: #6366f1; }
.rec-card h4 { color: #e2e8f0; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem; }
.rec-card li { color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0.3rem; }

/* ── MLI gauge text ── */
.mli-number {
    font-size: 4rem;
    font-weight: 800;
    text-align: center;
    line-height: 1;
}
.mli-label { text-align: center; font-size: 1rem; color: #94a3b8; margin-top: 0.5rem; }

/* ── Warning box ── */
.warning-box {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #fca5a5;
}
.info-box {
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #a5b4fc;
}
.success-box {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #6ee7b7;
}

/* ── Streamlit widget labels ── */
label, .stSlider label { color: #cbd5e1 !important; font-size: 0.9rem !important; }
.stSlider > div > div > div { background: rgba(99,102,241,0.3) !important; }

/* ── Submit button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(99,102,241,0.4) !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #475569;
    font-size: 0.8rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)


# ── Import prediction engine (Flask-free standalone module) ───────────────────
@st.cache_resource(show_spinner=False)
def load_engine():
    """Load the pure-Python prediction engine (no Flask dependency)."""
    try:
        from prediction_engine import predict_stress
        return predict_stress, True
    except Exception as e:
        st.error(f"Engine load error: {e}")
        return None, False

predict_stress_fn, engine_loaded = load_engine()


# ── Helper: run prediction ────────────────────────────────────────────────────
def run_prediction(inputs: dict):
    if predict_stress_fn is None:
        st.error("Prediction engine failed to load. Check your installation.")
        return None
    return predict_stress_fn(inputs)


# ── Helper: MLI color ─────────────────────────────────────────────────────────
def mli_color(score):
    if score <= 30:   return "#10b981"
    elif score <= 70: return "#f59e0b"
    else:             return "#ef4444"

def stress_color(level):
    colors = {"Low": "#10b981", "Moderate-Low": "#84cc16",
              "Moderate-High": "#f59e0b", "High": "#ef4444"}
    return colors.get(level, "#6366f1")

def stress_emoji(level):
    emojis = {"Low": "😌", "Moderate-Low": "🙂", "Moderate-High": "😐", "High": "😰"}
    return emojis.get(level, "🧠")


# ═══════════════════════════════════════════════════════════════════════════════
#  HERO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
    <p class="hero-title">🧠 NeuroPulse</p>
    <p class="hero-sub">AI-Powered Mental Health Monitoring System</p>
    <span class="hero-badge">✦ Voting Ensemble Model &nbsp;·&nbsp; 90.28% Accuracy &nbsp;·&nbsp; IoT-Enabled</span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  INPUT FORM
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title">❤️ Physiological Metrics</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    heart_rate   = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75, step=1)
    bp_systolic  = st.number_input("BP Systolic (mmHg)", min_value=80, max_value=200, value=120, step=1)

with col2:
    hrv          = st.number_input("HRV (ms)", min_value=0, max_value=200, value=50, step=1)
    bp_diastolic = st.number_input("BP Diastolic (mmHg)", min_value=40, max_value=120, value=80, step=1)

with col3:
    respiration  = st.number_input("Respiration Rate (breaths/min)", min_value=8, max_value=40, value=16, step=1)
    skin_temp    = st.number_input("Skin Temperature (°C)", min_value=32.0, max_value=40.0, value=36.5, step=0.1)

st.markdown('</div>', unsafe_allow_html=True)

# ── Psychological sliders ──────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">🧠 Psychological Assessment (1 = Calm, 5 = Stressed)</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    cognitive_state = st.slider(
        "🧩 Are you feeling mentally tired?",
        min_value=1, max_value=5, value=3,
        help="1 = Not at all  →  5 = Extremely"
    )
    concentration = st.slider(
        "🎯 How well can you concentrate right now?",
        min_value=1, max_value=5, value=3,
        help="1 = Very poor  →  5 = Excellent"
    )
    overloaded = st.slider(
        "🌀 Are you feeling mentally overloaded?",
        min_value=1, max_value=5, value=3,
        help="1 = No  →  5 = Yes, very much"
    )

with col_b:
    emotional_state = st.slider(
        "💭 How would you describe your emotional state?",
        min_value=1, max_value=5, value=3,
        help="1 = Very calm  →  5 = Very anxious"
    )
    mental_tired = st.slider(
        "😴 How mentally tired do you feel?",
        min_value=1, max_value=5, value=3,
        help="1 = Not tired  →  5 = Extremely tired"
    )

# Derive composite cognitive & emotional scores (average of related sliders)
cognitive_score  = round((cognitive_state + concentration + overloaded) / 3)
emotional_score  = round((emotional_state + mental_tired) / 2)

st.markdown('</div>', unsafe_allow_html=True)

# ── Submit ─────────────────────────────────────────────────────────────────────
analyze = st.button("🔍  Analyze My Stress Level", use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
if analyze:
    input_data = {
        "Heart_Rate":     float(heart_rate),
        "HRV":            float(hrv),
        "Respiration":    float(respiration),
        "Skin_Temp":      float(skin_temp),
        "BP_Systolic":    float(bp_systolic),
        "BP_Diastolic":   float(bp_diastolic),
        "Cognitive_State": int(cognitive_score),
        "Emotional_State": int(emotional_score),
    }

    with st.spinner("🔬 Analyzing your biometric data..."):
        result = run_prediction(input_data)

    if result and "error" not in result:
        sl    = result.get("stress_level", "Unknown")
        cond  = result.get("condition", sl)
        mli   = result.get("mental_load_index", 0)
        emoji = stress_emoji(sl)
        color = stress_color(sl)
        mc    = mli_color(mli)

        st.divider()

        # ── 1. CONDITION ──────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="result-badge" style="background:linear-gradient(135deg,{color}22,{color}11);
             border:2px solid {color}55;">
            <div class="result-emoji">{emoji}</div>
            <div class="result-level" style="color:{color};">{sl}</div>
            <div class="result-desc" style="color:#cbd5e1;">Condition: <strong>{cond}</strong></div>
        </div>
        """, unsafe_allow_html=True)

        # ── 2. INPUT SUMMARY ──────────────────────────────────────────────────
        st.markdown('<div class="card"><div class="card-title">📊 1️⃣ Input Summary</div>', unsafe_allow_html=True)
        mc1, mc2, mc3, mc4, mc5, mc6 = st.columns(6)
        pills = [
            (mc1, heart_rate,    "Heart Rate", "bpm"),
            (mc2, hrv,           "HRV",        "ms"),
            (mc3, respiration,   "Respiration","br/min"),
            (mc4, skin_temp,     "Skin Temp",  "°C"),
            (mc5, bp_systolic,   "BP Sys",     "mmHg"),
            (mc6, bp_diastolic,  "BP Dia",     "mmHg"),
        ]
        for col, val, label, unit in pills:
            with col:
                st.markdown(f"""
                <div class="metric-pill">
                    <div class="val">{val}</div>
                    <div class="lbl">{label}<br><span style="color:#6366f1">{unit}</span></div>
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── 3. MENTAL LOAD INDEX ──────────────────────────────────────────────
        st.markdown('<div class="card"><div class="card-title">⚡ 2️⃣ Mental Load Index (0–100)</div>', unsafe_allow_html=True)
        mli_col1, mli_col2 = st.columns([1, 2])
        with mli_col1:
            st.markdown(f"""
            <div class="mli-number" style="color:{mc};">{mli}</div>
            <div class="mli-label">/ 100</div>
            """, unsafe_allow_html=True)
        with mli_col2:
            st.progress(mli / 100)
            if mli <= 30:
                st.markdown('<div class="success-box">✅ <strong>Low Load</strong> — Your mental load is well within healthy range.</div>', unsafe_allow_html=True)
            elif mli <= 70:
                st.markdown('<div class="info-box">⚠️ <strong>Moderate Load</strong> — Some stress indicators detected. Consider taking breaks.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">🚨 <strong>High Load</strong> — Significant mental stress. Action recommended.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── 4. ADVISORY ───────────────────────────────────────────────────────
        rec = result.get("recommendation", {})
        if rec:
            st.markdown('<div class="card"><div class="card-title">💡 3️⃣ Advisory</div>', unsafe_allow_html=True)
            st.markdown(f"**{rec.get('title', '')}**")
            st.markdown(f"_{rec.get('primary', '')}_")
            actions = rec.get("actions", [])
            if actions:
                for action in actions:
                    st.markdown(f"- {action}")
            st.markdown('</div>', unsafe_allow_html=True)

        # ── 5. EARLY WARNING ──────────────────────────────────────────────────
        st.markdown('<div class="card"><div class="card-title">🔔 4️⃣ Early Warning</div>', unsafe_allow_html=True)
        if mli >= 71 or sl == "High":
            st.markdown('<div class="warning-box">🚨 <strong>Burnout Risk Detected</strong> — Your current metrics suggest elevated risk. Consider seeking professional support if this persists.</div>', unsafe_allow_html=True)
        elif mli >= 50:
            st.markdown('<div class="info-box">⚠️ <strong>Monitor Closely</strong> — Stress levels are rising. Implement stress management strategies now to prevent escalation.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">✅ <strong>No Immediate Warning</strong> — Keep maintaining your current healthy habits.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── 6. PERSONALIZED RECOMMENDATIONS ──────────────────────────────────
        full_recs = result.get("recommendations", {})
        if full_recs:
            st.markdown('<div class="card"><div class="card-title">🌿 5️⃣ Personalized Recommendations</div>', unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)

            with r1:
                natural = full_recs.get("natural_interventions", [])
                items   = "\n".join(f"<li>{i}</li>" for i in natural[:5]) if natural else "<li>No data</li>"
                st.markdown(f"""<div class="rec-card natural">
                    <h4>🌿 Natural Interventions</h4>
                    <ul style="padding-left:1.2rem">{items}</ul>
                    <p style="color:#94a3b8;font-size:0.8rem;margin-top:0.5rem">Non-pharmacological options to reduce cognitive load.</p>
                </div>""", unsafe_allow_html=True)

            with r2:
                otc   = full_recs.get("otc_options", [])
                items = "\n".join(f"<li>{i}</li>" for i in otc[:5]) if otc else "<li>No data</li>"
                st.markdown(f"""<div class="rec-card otc">
                    <h4>💊 OTC Options</h4>
                    <ul style="padding-left:1.2rem">{items}</ul>
                    <p style="color:#94a3b8;font-size:0.8rem;margin-top:0.5rem">Short-term over-the-counter supports where appropriate.</p>
                </div>""", unsafe_allow_html=True)

            with r3:
                pro   = full_recs.get("professional_services", [])
                items = "\n".join(f"<li>{i}</li>" for i in pro[:5]) if pro else "<li>No data</li>"
                st.markdown(f"""<div class="rec-card pro">
                    <h4>🧠 Professional Referral</h4>
                    <ul style="padding-left:1.2rem">{items}</ul>
                    <p style="color:#94a3b8;font-size:0.8rem;margin-top:0.5rem">When clinical assessment or specialist care is recommended.</p>
                </div>""", unsafe_allow_html=True)

            st.markdown("""<p style="color:#64748b;font-size:0.8rem;text-align:center;margin-top:1rem">
                ⚕️ This system does not replace professional medical diagnosis.
            </p>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Session history ───────────────────────────────────────────────────
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "stress_level": sl,
            "mli": mli,
            "condition": cond,
        })

    else:
        st.error(f"❌ Prediction failed: {result.get('error', 'Unknown error') if result else 'Engine not loaded'}")

# ── Trend chart (history) ─────────────────────────────────────────────────────
if "history" in st.session_state and len(st.session_state.history) > 1:
    st.markdown('<div class="card"><div class="card-title">📈 6️⃣ Stress Trend (This Session)</div>', unsafe_allow_html=True)
    import pandas as pd
    df = pd.DataFrame(st.session_state.history)
    st.line_chart(df.set_index("time")["mli"], use_container_width=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    col_dl, col_cl = st.columns(2)
    with col_dl:
        csv = df.to_csv(index=False)
        st.download_button("⬇ Download History (CSV)", csv, "neuropulse_history.csv", "text/csv")
    with col_cl:
        if st.button("🗑 Clear History"):
            st.session_state.history = []
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🧠 &nbsp; NeuroPulse — AI Mental Health Monitoring &nbsp;·&nbsp;
    ⚕️ &nbsp; For educational purposes only &nbsp;·&nbsp;
    📊 &nbsp; 90.28% Model Accuracy
</div>
""", unsafe_allow_html=True)
