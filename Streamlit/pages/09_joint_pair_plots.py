"""
Page 9 — Joint & Pair Plots
Hue/style/size, joint plot, pair plot, heatmap.
"""
import streamlit as st
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, get_active_df, numeric_cols, categorical_cols, inject_custom_css)

st.set_page_config(page_title="Joint & Pair Plots | DataViz", page_icon="🔗", layout="wide")
inject_custom_css()

PAGE = "joint_pair"
PALETTE = ["#667eea", "#764ba2", "#f093fb", "#fda085", "#a18cd1"]


def render():
    section_header("🔗", "Joint & Pair Plots")
    st.markdown("Explore **multi-variable relationships** with joint plots, pair plots, and heatmaps.")

    df = get_active_df("Iris")
    nc = numeric_cols(df)
    cc = categorical_cols(df)

    # ── Step 1: Hue, style, size ──
    if step_check(1, "Hue, style & size parameters", PAGE):
        st.markdown("#### 🎨 Hue, Style & Size")
        lib = library_selector(f"{PAGE}_1")

        info_card("These parameters encode additional variables:",
                  "<b>hue</b> → color, <b>style</b> → marker shape / line dash, "
                  "<b>size</b> → marker size. Seaborn excels at this.")

        x_col = nc[0] if nc else df.columns[0]
        y_col = nc[1] if len(nc) > 1 else df.columns[1]
        hue_col = cc[0] if cc else None
        size_col = nc[2] if len(nc) > 2 else None

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            if hue_col:
                for cat in df[hue_col].unique():
                    sub = df[df[hue_col] == cat]
                    ax.scatter(sub[x_col], sub[y_col], label=cat, alpha=0.7,
                               s=sub[size_col]*10 if size_col else 40)
                ax.legend(title=hue_col)
            else:
                ax.scatter(df[x_col], df[y_col], alpha=0.7)
            ax.set_xlabel(x_col); ax.set_ylabel(y_col)
            ax.set_title(f"Scatter with Hue & Size", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code(f"""
sns.scatterplot(data=df, x="{x_col}", y="{y_col}",
                hue="{hue_col}", style="{hue_col}",
                size="{size_col}", palette="viridis")
""")
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue_col,
                            style=hue_col, size=size_col,
                            palette=PALETTE, ax=ax, alpha=0.7)
            ax.set_title("Scatter with Hue, Style & Size", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.scatter(df, x=x_col, y=y_col, color=hue_col,
                             symbol=hue_col, size=size_col,
                             color_discrete_sequence=PALETTE,
                             title="Scatter with Hue, Symbol & Size")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 2: Joint plot ──
    if step_check(2, "Joint plot", PAGE):
        st.markdown("#### 🔗 Joint Plot")
        lib = library_selector(f"{PAGE}_2", default="Seaborn", options=["Seaborn", "Plotly"])

        x_col = nc[0] if nc else df.columns[0]
        y_col = nc[1] if len(nc) > 1 else df.columns[1]
        hue_col = cc[0] if cc else None

        info_card("Joint Plot", "Combines a scatter (or other bi-variate) plot with marginal distributions (histograms / KDEs).")

        if lib == "Seaborn":
            show_code(f"""
g = sns.jointplot(data=df, x="{x_col}", y="{y_col}",
                  hue="{hue_col}", kind="scatter", palette=palette)
""")
            import seaborn as sns, matplotlib.pyplot as plt
            g = sns.jointplot(data=df, x=x_col, y=y_col, hue=hue_col,
                              kind="scatter", palette=PALETTE, height=6)
            g.figure.suptitle(f"Joint Plot — {x_col} vs {y_col}", y=1.02, fontweight="bold")
            st.pyplot(g.figure)
        else:
            import plotly.express as px
            fig = px.scatter(df, x=x_col, y=y_col, color=hue_col,
                             marginal_x="histogram", marginal_y="histogram",
                             color_discrete_sequence=PALETTE,
                             title=f"Joint Plot — {x_col} vs {y_col}")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 3: Pair plot ──
    if step_check(3, "Pair plot", PAGE):
        st.markdown("#### 🔲 Pair Plot")
        lib = library_selector(f"{PAGE}_3", default="Seaborn", options=["Seaborn", "Plotly"])

        hue_col = cc[0] if cc else None
        use_cols = nc[:4]  # limit to 4 numeric columns for performance

        info_card("Pair Plot", "Creates a grid of scatter plots for every combination of numeric variables.")

        if lib == "Seaborn":
            show_code(f"""
g = sns.pairplot(df[{use_cols} + ["{hue_col}"]], hue="{hue_col}", palette=palette)
""")
            import seaborn as sns, matplotlib.pyplot as plt
            subset = df[use_cols + ([hue_col] if hue_col else [])].dropna()
            g = sns.pairplot(subset, hue=hue_col, palette=PALETTE,
                             plot_kws={"alpha": 0.6, "s": 30})
            g.figure.suptitle("Pair Plot", y=1.02, fontweight="bold")
            st.pyplot(g.figure)
        else:
            import plotly.express as px
            fig = px.scatter_matrix(df, dimensions=use_cols, color=hue_col,
                                    color_discrete_sequence=PALETTE,
                                    title="Pair Plot (Scatter Matrix)")
            fig.update_traces(diagonal_visible=True, marker=dict(size=3, opacity=0.5))
            fig.update_layout(height=700)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 4: Heatmap / correlation ──
    if step_check(4, "Heatmap / correlation matrix", PAGE):
        st.markdown("#### 🗺️ Heatmap — Correlation Matrix")
        lib = library_selector(f"{PAGE}_4")

        corr = df[nc].corr()

        if lib == "Matplotlib":
            show_code("""
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(im)
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 6))
            im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1, aspect="auto")
            ax.set_xticks(range(len(corr))); ax.set_xticklabels(corr.columns, rotation=45)
            ax.set_yticks(range(len(corr))); ax.set_yticklabels(corr.columns)
            for i in range(len(corr)):
                for j in range(len(corr)):
                    ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=9)
            plt.colorbar(im, ax=ax)
            ax.set_title("Correlation Matrix", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code("""
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
""")
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1,
                        fmt=".2f", linewidths=0.5, ax=ax)
            ax.set_title("Correlation Matrix", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                            zmin=-1, zmax=1, title="Correlation Matrix")
            st.plotly_chart(fig, use_container_width=True)


render()
