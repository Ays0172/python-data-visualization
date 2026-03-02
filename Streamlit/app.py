"""
📊 Interactive Data Visualization Learning App
Home page — landing page with interactive cards navigating to topic pages.
"""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from utils import inject_custom_css, get_sample_datasets

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="📊 Data Visualization Masterclass",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()

# ──────────────────────────────────────────────
# Sidebar — dataset controls
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("##### 📁 Dataset")
    use_custom = st.toggle("Upload my own CSV", key="use_custom_data")

    if use_custom:
        st.file_uploader(
            "Upload CSV", type=["csv"], key="_uploaded_file",
            help="Upload any CSV — columns are auto-detected.",
        )
    else:
        ds_names = list(get_sample_datasets().keys())
        st.selectbox("Sample dataset", ds_names, key="selected_dataset")

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding: 0.3rem 0 0.5rem 0;">
        <span style="font-size: 2rem;">📊</span>
        <h2 style="margin: 0.2rem 0 0 0; font-size: 1rem; letter-spacing: 0.5px; color: #ffffff;">
            DataViz Masterclass
        </h2>
        <p style="color: rgba(255,255,255,0.6); font-size: 0.72rem; margin-top: 0.2rem;">
            Matplotlib · Seaborn · Plotly
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Built with ❤️ using Streamlit")
    st.caption("© 2026 Ayush Sood")

# ──────────────────────────────────────────────
# Hero Section (compact)
# ──────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 0.8rem 1rem 0.5rem 1rem;">
    <span style="font-size: 2.5rem;">📊</span>
    <h1 style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem; font-weight: 800;
        margin: 0.2rem 0 0.2rem 0; line-height: 1.2;
    ">Data Visualization Masterclass</h1>
    <p style="font-size: 0.95rem; opacity: 0.85; max-width: 600px; margin: 0 auto 0.4rem auto;">
        An interactive guide to <b>Matplotlib</b>, <b>Seaborn</b> &amp; <b>Plotly</b> — step by step.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Feature badges (compact) ──
f1, f2, f3 = st.columns(3)
_features = [
    ("🎯", "Step-by-Step",    "Click through concepts at your pace."),
    ("🔄", "Library Switcher", "Same chart in Matplotlib, Seaborn, or Plotly."),
    ("📂", "Your Data",       "Sample datasets or upload your own CSV."),
]
for col, (icon, title, desc) in zip([f1, f2, f3], _features):
    col.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(102,126,234,0.10), rgba(118,75,162,0.06));
        border: 1px solid rgba(102,126,234,0.18);
        border-radius: 10px; padding: 0.8rem 0.7rem; text-align: center;
    ">
        <div style="font-size: 1.5rem; margin-bottom: 0.2rem;">{icon}</div>
        <h3 style="margin:0 0 0.15rem 0; font-size:0.92rem;">{title}</h3>
        <p style="opacity:0.8; font-size:0.78rem; margin:0; line-height:1.3;">{desc}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("#### 📚 Topics")

# ── Topic cards (compact) ──
TOPICS = [
    ("🚀", "Getting Started",       "Imports, first chart, library comparison"),
    ("📈", "Line Charts",           "Basic, multi-line, styled, time-series"),
    ("📊", "Bar Charts",            "Grouped, stacked, horizontal, histograms"),
    ("⚡", "Scatter Plots",         "Color/size encoding, bubble, regression"),
    ("📦", "Statistical Plots",     "Box, violin, stem, whisker plots"),
    ("🌊", "Area & Fill",           "Area charts, stack plots, fill between"),
    ("🥧", "Pie & Donut",           "Pie, donut, exploded slices, shadows"),
    ("📋", "Categorical Plots",     "Count, strip, swarm, point plots"),
    ("🔗", "Joint & Pair Plots",    "Joint, pair plots, heatmaps"),
    ("🔲", "Subplots & Layouts",    "Grid layouts, shared axes, mixed types"),
    ("🎨", "Styling & Aesthetics",  "Colors, themes, fonts, scales, grids"),
    ("🧊", "3D Plots",              "3D scatter, surface, interactive"),
    ("⚙️", "Advanced Topics",       "Live data, datetime, export, explorer"),
]

for row_start in range(0, len(TOPICS), 4):
    cols = st.columns(4)
    for i, col in enumerate(cols):
        idx = row_start + i
        if idx >= len(TOPICS):
            break
        icon, label, desc = TOPICS[idx]
        with col:
            st.markdown(f"""
            <div style="
                background: rgba(102,126,234,0.04);
                border: 1px solid rgba(102,126,234,0.12);
                border-radius: 8px; padding: 0.5rem 0.6rem;
                margin-bottom: 0.3rem;
            ">
                <p style="margin:0 0 0.1rem 0; font-size:0.85rem;">
                    <b>{icon} {idx+1}. {label}</b>
                </p>
                <p style="opacity:0.75; font-size:0.72rem; margin:0; line-height:1.25;">
                    {desc}
                </p>
            </div>
            """, unsafe_allow_html=True)

st.info("👈 **Select a topic from the sidebar** to begin!")
