"""
Page 5 — Statistical Plots
Box, violin, stem plots.
"""
import streamlit as st
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, get_active_df, numeric_cols, categorical_cols, inject_custom_css)

st.set_page_config(page_title="Statistical Plots | DataViz", page_icon="📦", layout="wide")
inject_custom_css()

PAGE = "stat_plots"
PALETTE = ["#667eea", "#764ba2", "#f093fb", "#fda085", "#a18cd1"]


def render():
    section_header("📦", "Statistical Plots")
    st.markdown("Statistical plots help you understand **distributions, spread, and outliers**.")
    df = get_active_df("Tips")

    # ── Step 1: Box plot ──
    if step_check(1, "Box plot", PAGE):
        st.markdown("#### 📦 Box Plot (Box & Whisker)")
        lib = library_selector(f"{PAGE}_1")
        nc = numeric_cols(df)
        cc = categorical_cols(df)
        y_col = nc[0] if nc else df.columns[0]
        x_col = cc[0] if cc else None

        info_card("Box Plot Anatomy",
                  "Shows median (center line), Q1–Q3 (box), whiskers (1.5×IQR), and outliers (dots beyond whiskers).")

        if lib == "Matplotlib":
            show_code(f"""
fig, ax = plt.subplots(figsize=(8, 5))
if x_col:
    groups = [g["{y_col}"].values for _, g in df.groupby("{x_col}")]
    ax.boxplot(groups, labels=df["{x_col}"].unique())
else:
    ax.boxplot(df["{y_col}"])
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            if x_col:
                groups = [g[y_col].values for _, g in df.groupby(x_col)]
                bp = ax.boxplot(groups, labels=df[x_col].unique(), patch_artist=True)
                for patch, color in zip(bp["boxes"], PALETTE * 5):
                    patch.set_facecolor(color); patch.set_alpha(0.6)
                ax.set_xlabel(x_col)
            else:
                bp = ax.boxplot(df[y_col], patch_artist=True)
                bp["boxes"][0].set_facecolor(PALETTE[0])
            ax.set_ylabel(y_col)
            ax.set_title(f"Box Plot of {y_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code(f"""
sns.boxplot(data=df, x="{x_col}", y="{y_col}", palette=palette)
""")
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(data=df, x=x_col, y=y_col, palette=PALETTE, ax=ax)
            ax.set_title(f"Box Plot of {y_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            show_code(f"""
fig = px.box(df, x="{x_col}", y="{y_col}", color="{x_col}")
""")
            import plotly.express as px
            fig = px.box(df, x=x_col, y=y_col, color=x_col,
                         color_discrete_sequence=PALETTE,
                         title=f"Box Plot of {y_col}")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 2: Violin plot ──
    if step_check(2, "Violin plot", PAGE):
        st.markdown("#### 🎻 Violin Plot")
        lib = library_selector(f"{PAGE}_2")
        nc = numeric_cols(df); cc = categorical_cols(df)
        y_col = nc[0] if nc else df.columns[0]
        x_col = cc[0] if cc else None

        info_card("Violin Plot", "Combines a box plot with a KDE (kernel density) — wider sections show higher density.")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            if x_col:
                groups = [g[y_col].dropna().values for _, g in df.groupby(x_col)]
                vp = ax.violinplot(groups, showmeans=True, showmedians=True)
                ax.set_xticks(range(1, len(df[x_col].unique()) + 1))
                ax.set_xticklabels(df[x_col].unique())
                for i, body in enumerate(vp["bodies"]):
                    body.set_facecolor(PALETTE[i % len(PALETTE)]); body.set_alpha(0.6)
            else:
                ax.violinplot(df[y_col].dropna().values, showmeans=True)
            ax.set_ylabel(y_col)
            ax.set_title(f"Violin Plot of {y_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.violinplot(data=df, x=x_col, y=y_col, palette=PALETTE, ax=ax, inner="quart")
            ax.set_title(f"Violin Plot of {y_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.violin(df, x=x_col, y=y_col, color=x_col, box=True,
                            color_discrete_sequence=PALETTE,
                            title=f"Violin Plot of {y_col}")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 3: Stem plot ──
    if step_check(3, "Stem plot", PAGE):
        st.markdown("#### 🌿 Stem Plot")
        lib = library_selector(f"{PAGE}_3", default="Matplotlib", options=["Matplotlib", "Plotly"])

        np.random.seed(7)
        x = np.arange(1, 21)
        y = np.random.randint(1, 20, 20)

        info_card("Stem Plot", "Like a bar chart for discrete data, showing each value as a stem (line) with a marker head.")

        if lib == "Matplotlib":
            show_code("""
ax.stem(x, y, linefmt='-', markerfmt='o', basefmt='k-')
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 4))
            markerline, stemlines, baseline = ax.stem(x, y)
            plt.setp(stemlines, color="#667eea", linewidth=1.5)
            plt.setp(markerline, color="#764ba2", markersize=8)
            plt.setp(baseline, color="gray", linewidth=0.5)
            ax.set_title("Stem Plot", fontweight="bold")
            ax.set_xlabel("Index"); ax.set_ylabel("Value")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.graph_objects as go
            fig = go.Figure()
            for xi, yi in zip(x, y):
                fig.add_trace(go.Scatter(x=[xi, xi], y=[0, yi], mode="lines",
                                         line=dict(color="#667eea", width=2),
                                         showlegend=False))
            fig.add_trace(go.Scatter(x=x, y=y, mode="markers",
                                     marker=dict(color="#764ba2", size=10),
                                     name="Values"))
            fig.update_layout(title="Stem Plot", xaxis_title="Index", yaxis_title="Value")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 4: Whisker customization ──
    if step_check(4, "Customized box plot with notches", PAGE):
        st.markdown("#### 🎛️ Customized Box Plot")
        lib = library_selector(f"{PAGE}_4")
        nc = numeric_cols(df)
        y_col = nc[0] if nc else df.columns[0]

        if lib == "Matplotlib":
            show_code("""
ax.boxplot(data, notch=True, patch_artist=True, showfliers=True,
           flierprops=dict(marker='D', color='red'))
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 5))
            bp = ax.boxplot(df[y_col].dropna(), notch=True, patch_artist=True,
                            flierprops=dict(marker="D", color="#EF553B", markersize=5))
            bp["boxes"][0].set_facecolor(PALETTE[0]); bp["boxes"][0].set_alpha(0.6)
            ax.set_ylabel(y_col)
            ax.set_title(f"Notched Box Plot — {y_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.boxplot(data=df, y=y_col, color=PALETTE[0], notch=True,
                        flierprops=dict(marker="D", color="#EF553B"), ax=ax)
            ax.set_title(f"Notched Box Plot — {y_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.box(df, y=y_col, notched=True,
                         color_discrete_sequence=[PALETTE[0]],
                         title=f"Notched Box Plot — {y_col}")
            st.plotly_chart(fig, use_container_width=True)


render()
