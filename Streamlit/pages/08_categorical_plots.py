"""
Page 8 — Categorical Plots
Count, strip, swarm, point (Seaborn-centric with alternatives).
"""
import streamlit as st
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, get_active_df, numeric_cols, categorical_cols, inject_custom_css)

st.set_page_config(page_title="Categorical Plots | DataViz", page_icon="📋", layout="wide")
inject_custom_css()

PAGE = "cat_plots"
PALETTE = ["#667eea", "#764ba2", "#f093fb", "#fda085", "#a18cd1"]


def render():
    section_header("📋", "Categorical Plots")
    st.markdown("Categorical plots are designed for **categorical (grouping) variables** — "
                "they're a Seaborn specialty.")

    df = get_active_df("Tips")
    nc = numeric_cols(df)
    cc = categorical_cols(df)
    y_col = nc[0] if nc else df.columns[0]
    x_col = cc[0] if cc else df.columns[0]
    hue_col = cc[1] if len(cc) > 1 else None

    # ── Step 1: Count plot ──
    if step_check(1, "Count plot", PAGE):
        st.markdown("#### 🔢 Count Plot")
        lib = library_selector(f"{PAGE}_1")

        info_card("Count Plot", "Shows the count of observations in each category — like a histogram for categorical data.")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            counts = df[x_col].value_counts()
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(counts.index.astype(str), counts.values, color=PALETTE[:len(counts)])
            ax.set_title(f"Count of {x_col}", fontweight="bold")
            ax.set_xlabel(x_col); ax.set_ylabel("Count")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code(f"""
sns.countplot(data=df, x="{x_col}", hue="{hue_col}", palette=palette)
""")
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.countplot(data=df, x=x_col, hue=hue_col, palette=PALETTE, ax=ax)
            ax.set_title(f"Count of {x_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.histogram(df, x=x_col, color=hue_col, barmode="group",
                               color_discrete_sequence=PALETTE,
                               title=f"Count of {x_col}")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 2: Strip plot ──
    if step_check(2, "Strip plot", PAGE):
        st.markdown("#### 📍 Strip Plot")
        lib = library_selector(f"{PAGE}_2")

        info_card("Strip Plot", "Shows every individual observation as a jittered dot. Great for small-to-medium datasets.")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            cats = df[x_col].unique()
            for i, cat in enumerate(cats):
                subset = df[df[x_col] == cat][y_col]
                jitter = np.random.uniform(-0.2, 0.2, len(subset))
                ax.scatter(np.full(len(subset), i) + jitter, subset,
                           alpha=0.5, color=PALETTE[i % len(PALETTE)], s=30)
            ax.set_xticks(range(len(cats))); ax.set_xticklabels(cats)
            ax.set_xlabel(x_col); ax.set_ylabel(y_col)
            ax.set_title(f"Strip Plot — {y_col} by {x_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code(f"""
sns.stripplot(data=df, x="{x_col}", y="{y_col}", hue="{hue_col}",
              jitter=True, palette=palette, alpha=0.6)
""")
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.stripplot(data=df, x=x_col, y=y_col, hue=hue_col,
                          jitter=True, palette=PALETTE, alpha=0.6, ax=ax)
            ax.set_title(f"Strip Plot — {y_col} by {x_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.strip(df, x=x_col, y=y_col, color=hue_col,
                           color_discrete_sequence=PALETTE,
                           title=f"Strip Plot — {y_col} by {x_col}")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 3: Swarm plot ──
    if step_check(3, "Swarm plot", PAGE):
        st.markdown("#### 🐝 Swarm Plot")
        lib = library_selector(f"{PAGE}_3", default="Seaborn", options=["Seaborn", "Plotly"])

        info_card("Swarm Plot", "Like strip plot, but points are adjusted so they don't overlap — revealing density.")

        if lib == "Seaborn":
            show_code(f"""
sns.swarmplot(data=df, x="{x_col}", y="{y_col}", hue="{hue_col}", palette=palette)
""")
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            sample = df.sample(min(100, len(df)), random_state=42)
            sns.swarmplot(data=sample, x=x_col, y=y_col, hue=hue_col,
                          palette=PALETTE, ax=ax, size=5)
            ax.set_title(f"Swarm Plot — {y_col} by {x_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.strip(df, x=x_col, y=y_col, color=hue_col,
                           color_discrete_sequence=PALETTE,
                           title=f"Swarm-style Plot — {y_col} by {x_col}")
            st.plotly_chart(fig, use_container_width=True)
            st.caption("_Plotly uses jittered strip plot as swarm approximation._")
        st.markdown("---")

    # ── Step 4: Point plot ──
    if step_check(4, "Point plot (with error bars)", PAGE):
        st.markdown("#### 📌 Point Plot")
        lib = library_selector(f"{PAGE}_4")

        info_card("Point Plot", "Shows point estimates (mean) and confidence intervals. Great for comparing group means.")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            grouped = df.groupby(x_col)[y_col].agg(["mean", "std"]).reset_index()
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.errorbar(grouped[x_col], grouped["mean"], yerr=grouped["std"],
                        fmt="o-", color=PALETTE[0], capsize=5, capthick=2,
                        markersize=8, linewidth=2)
            ax.set_xlabel(x_col); ax.set_ylabel(f"Mean {y_col}")
            ax.set_title(f"Point Plot — Mean {y_col} by {x_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code(f"""
sns.pointplot(data=df, x="{x_col}", y="{y_col}", hue="{hue_col}",
              palette=palette, dodge=True, capsize=0.1)
""")
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.pointplot(data=df, x=x_col, y=y_col, hue=hue_col,
                          palette=PALETTE, dodge=0.3, capsize=0.1,
                          err_kws={"linewidth": 1.5}, ax=ax)
            ax.set_title(f"Point Plot — Mean {y_col} by {x_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            grouped = df.groupby([x_col] + ([hue_col] if hue_col else []))[y_col]\
                        .agg(["mean", "std"]).reset_index()
            fig = px.scatter(grouped, x=x_col, y="mean", color=hue_col,
                             error_y="std", color_discrete_sequence=PALETTE,
                             title=f"Point Plot — Mean {y_col} by {x_col}")
            fig.update_traces(mode="markers+lines")
            st.plotly_chart(fig, use_container_width=True)


render()
