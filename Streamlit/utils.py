"""
Utility functions for the Data Visualization Learning App.
Provides dataset loading, UI helpers, and styling.
"""

import streamlit as st
import pandas as pd
import numpy as np
import io

# ---------------------------------------------------------------------------
# Dataset helpers
# ---------------------------------------------------------------------------

def get_sample_datasets():
    """Return a dict of available sample datasets."""
    return {
        "Tips": _load_tips,
        "Iris": _load_iris,
        "Penguins": _load_penguins,
        "Stocks (AAPL)": _load_stocks,
        "Diamonds (sample)": _load_diamonds,
    }


def _load_tips():
    import seaborn as sns
    return sns.load_dataset("tips")


def _load_iris():
    import seaborn as sns
    return sns.load_dataset("iris")


def _load_penguins():
    import seaborn as sns
    df = sns.load_dataset("penguins").dropna()
    return df


def _load_stocks():
    """Generate realistic AAPL-style stock data."""
    np.random.seed(42)
    dates = pd.bdate_range("2023-01-02", periods=252)
    price = 150 + np.cumsum(np.random.randn(252) * 1.5)
    volume = np.random.randint(50_000_000, 120_000_000, 252)
    df = pd.DataFrame({
        "Date": dates,
        "Open": price + np.random.randn(252) * 0.5,
        "High": price + abs(np.random.randn(252)) * 2,
        "Low": price - abs(np.random.randn(252)) * 2,
        "Close": price,
        "Volume": volume,
    })
    return df


def _load_diamonds():
    import seaborn as sns
    df = sns.load_dataset("diamonds").sample(500, random_state=42)
    return df


def load_dataset(name: str) -> pd.DataFrame:
    """Load a sample dataset by name."""
    datasets = get_sample_datasets()
    if name in datasets:
        return datasets[name]()
    return _load_tips()


@st.cache_data
def load_cached_dataset(name: str) -> pd.DataFrame:
    return load_dataset(name)


def get_user_data() -> pd.DataFrame | None:
    """Handle CSV upload and return a DataFrame (or None)."""
    uploaded = st.session_state.get("_uploaded_file")
    if uploaded is not None:
        try:
            return pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    return None


def get_active_df(default_name: str = "Tips") -> pd.DataFrame:
    """Return the active dataset — uploaded or sample."""
    if st.session_state.get("use_custom_data", False):
        df = get_user_data()
        if df is not None:
            return df
        st.info("⬆️ Upload a CSV in the sidebar, or switch back to sample data.")
        return load_cached_dataset(default_name)
    return load_cached_dataset(
        st.session_state.get("selected_dataset", default_name)
    )


# ---------------------------------------------------------------------------
# Column helpers for user-uploaded data
# ---------------------------------------------------------------------------

def numeric_cols(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include="number").columns.tolist()


def categorical_cols(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


def pick_xy(df: pd.DataFrame, prefix: str = ""):
    """Let user pick x and y columns for their custom dataset."""
    num = numeric_cols(df)
    cat = categorical_cols(df)
    all_cols = df.columns.tolist()

    c1, c2 = st.columns(2)
    with c1:
        x = st.selectbox(f"X-axis column", all_cols, key=f"{prefix}_x")
    with c2:
        y_default = num[0] if num else all_cols[0]
        y = st.selectbox(f"Y-axis column", all_cols,
                         index=all_cols.index(y_default) if y_default in all_cols else 0,
                         key=f"{prefix}_y")
    return x, y


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

def show_code(code: str, language: str = "python"):
    """Display code in a styled expander."""
    with st.expander("📝 View Code", expanded=False):
        st.code(code.strip(), language=language)


def step_check(step_num: int, label: str, page_key: str) -> bool:
    """
    Render a step checkbox. Returns True if the step should be shown.
    Steps are sequential — step N only shows if step N-1 is checked.
    """
    key = f"{page_key}_step_{step_num}"
    if step_num == 1:
        return st.checkbox(f"**Step {step_num}:** {label}", key=key, value=True)

    prev_key = f"{page_key}_step_{step_num - 1}"
    if st.session_state.get(prev_key, False):
        return st.checkbox(f"**Step {step_num}:** {label}", key=key)
    return False


def library_selector(key: str = "lib", default: str = "Plotly",
                     options: list[str] | None = None) -> str:
    """Render library chooser radio buttons."""
    opts = options or ["Matplotlib", "Seaborn", "Plotly"]
    idx = opts.index(default) if default in opts else 0
    return st.radio("🎨 Visualization Library", opts,
                    index=idx, key=f"lib_{key}", horizontal=True)


def section_header(icon: str, title: str):
    """Render a styled section header."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    ">
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">
            {icon} {title}
        </h2>
    </div>
    """, unsafe_allow_html=True)


def info_card(title: str, content: str):
    """Render an info card."""
    st.markdown(f"""
    <div style="
        background: rgba(102, 126, 234, 0.08);
        border-left: 4px solid #667eea;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0 1rem 0;
    ">
        <strong>{title}</strong><br/>
        <span style="opacity: 0.85;">{content}</span>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------

def inject_custom_css():
    """Inject premium enterprise styling."""
    st.markdown("""
    <style>
    /* ========== Global ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Tighter vertical rhythm */
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    .stMarkdown { margin-bottom: 0; }

    /* ========== Sidebar ========== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding-top: 0.5rem;
    }
    /* All sidebar text white */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h5 { color: #ffffff !important; }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stToggle label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p { color: #f0f0f0 !important; }
    /* Nav links & "View N more" / "View less" */
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] a span,
    section[data-testid="stSidebar"] button[kind="link"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] span,
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] button,
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li span,
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] summary,
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] details > summary,
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] details > summary span {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    section[data-testid="stSidebar"] .stCaption { color: rgba(255,255,255,0.7) !important; }
    section[data-testid="stSidebar"] hr {
        border: none; height: 1px;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.2), transparent);
        margin: 0.6rem 0;
    }

    /* ========== Step checkboxes ========== */
    .stCheckbox > label {
        background: rgba(102, 126, 234, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 8px;
        padding: 0.5rem 0.9rem;
        transition: all 0.25s ease;
    }
    .stCheckbox > label:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.12);
        transform: translateX(2px);
    }

    /* ========== Radio buttons (library selector) ========== */
    .stRadio > div { gap: 0.25rem; }
    .stRadio > div > label {
        background: rgba(102, 126, 234, 0.06);
        border: 1px solid rgba(102, 126, 234, 0.15);
        border-radius: 20px;
        padding: 0.3rem 0.9rem;
        transition: all 0.2s ease;
        font-size: 0.9rem;
    }
    .stRadio > div > label:hover { border-color: #667eea; }

    /* ========== Buttons ========== */
    .stButton > button {
        border: 1px solid rgba(102, 126, 234, 0.25);
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.25s ease;
    }
    .stButton > button:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    /* ========== Tabs ========== */
    .stTabs [data-baseweb="tab-list"] { gap: 0.4rem; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.4rem 1rem;
        font-weight: 500;
    }

    /* ========== Expanders ========== */
    .streamlit-expanderHeader {
        font-weight: 600;
        border-radius: 8px;
    }

    /* ========== Metrics ========== */
    [data-testid="stMetric"] {
        background: rgba(102, 126, 234, 0.04);
        border: 1px solid rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        padding: 0.6rem;
    }
    [data-testid="stMetricLabel"] { font-weight: 600; }

    /* ========== Code blocks ========== */
    .stCodeBlock { border-radius: 10px; }

    /* ========== Dividers ========== */
    hr {
        border: none; height: 1px;
        background: linear-gradient(to right, transparent, #667eea40, transparent);
        margin: 1rem 0;
    }

    /* ========== Dataframes ========== */
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

