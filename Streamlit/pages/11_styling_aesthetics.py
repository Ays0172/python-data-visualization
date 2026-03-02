"""
Page 11 — Styling & Aesthetics
Figure size, labels, axes, colors, grids, themes.
"""
import streamlit as st
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, inject_custom_css)

st.set_page_config(page_title="Styling & Aesthetics | DataViz", page_icon="🎨", layout="wide")
inject_custom_css()

PAGE = "styling"
PALETTE = ["#667eea", "#764ba2", "#f093fb", "#fda085", "#a18cd1"]


def render():
    section_header("🎨", "Styling & Aesthetics")
    st.markdown("Master **colors, fonts, themes, scales, and grids** to make publication-quality charts.")

    # ── Step 1: Figure size ──
    if step_check(1, "Figure size", PAGE):
        st.markdown("#### 📐 Figure Size")
        lib = library_selector(f"{PAGE}_1", default="Matplotlib", options=["Matplotlib", "Plotly"])

        w = st.slider("Width", 4, 16, 10, key=f"{PAGE}_w")
        h = st.slider("Height", 2, 10, 4, key=f"{PAGE}_h")

        show_code(f"""
fig, ax = plt.subplots(figsize=({w}, {h}))
# figsize is (width, height) in inches
""")

        np.random.seed(0)
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(w, h))
            ax.plot(x, y, color=PALETTE[0], linewidth=2)
            ax.set_title(f"Figure: {w}×{h} inches", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.line(x=x, y=y, title=f"Figure: {w*80}×{h*80} px")
            fig.update_layout(width=w*80, height=h*80)
            fig.update_traces(line_color=PALETTE[0])
            st.plotly_chart(fig)
        st.markdown("---")

    # ── Step 2: Labels, titles, fonts ──
    if step_check(2, "Labels, titles & fonts", PAGE):
        st.markdown("#### 🏷️ Labels, Titles & Fonts")
        lib = library_selector(f"{PAGE}_2", default="Matplotlib", options=["Matplotlib", "Plotly"])

        show_code("""
ax.set_title("Title", fontsize=16, fontweight='bold', fontfamily='serif')
ax.set_xlabel("X Label", fontsize=12, fontstyle='italic')
ax.set_ylabel("Y Label", fontsize=12)
ax.tick_params(axis='both', labelsize=10, rotation=45)
""")

        np.random.seed(1)
        x = np.arange(1, 8)
        y = np.random.randint(5, 25, 7)

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.bar(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], y,
                   color=PALETTE[0], edgecolor="white")
            ax.set_title("Weekly Performance", fontsize=16, fontweight="bold",
                         fontfamily="serif")
            ax.set_xlabel("Day of Week", fontsize=12, fontstyle="italic")
            ax.set_ylabel("Score", fontsize=12)
            ax.tick_params(axis="x", rotation=30)
            for i, v in enumerate(y):
                ax.text(i, v + 0.3, str(v), ha="center", fontsize=10, fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.bar(x=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], y=y,
                         color_discrete_sequence=[PALETTE[0]],
                         title="Weekly Performance", text=y,
                         labels={"x": "Day of Week", "y": "Score"})
            fig.update_layout(title_font=dict(size=20, family="serif"),
                              xaxis_title_font=dict(size=14))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 3: Axis scales ──
    if step_check(3, "Axis scales (log, symlog)", PAGE):
        st.markdown("#### 📏 Axis Scales")
        lib = library_selector(f"{PAGE}_3", default="Matplotlib", options=["Matplotlib", "Plotly"])

        scale = st.selectbox("Scale type", ["linear", "log", "symlog"], key=f"{PAGE}_scale")

        np.random.seed(2)
        x = np.linspace(1, 100, 100)
        y = np.exp(x / 20) + np.random.randn(100) * 5

        show_code(f"""
ax.set_yscale("{scale}")
""")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(9, 4))
            ax.plot(x, y, color=PALETTE[0], linewidth=1.5)
            ax.set_yscale(scale)
            ax.set_title(f"Y-Axis: {scale} scale", fontweight="bold")
            ax.set_xlabel("x"); ax.set_ylabel("y")
            ax.grid(alpha=0.3)
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.line(x=x, y=y, title=f"Y-Axis: {scale} scale")
            fig.update_traces(line_color=PALETTE[0])
            if scale == "log":
                fig.update_yaxes(type="log")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 4: Colors, line styles, markers ──
    if step_check(4, "Colors, palettes & colormaps", PAGE):
        st.markdown("#### 🌈 Color Palettes & Colormaps")

        import matplotlib.pyplot as plt

        info_card("Color Systems",
                  "Use named colors (\"red\"), hex (\"#667eea\"), RGB tuples, or colormaps "
                  "(\"viridis\", \"coolwarm\", \"Spectral\").")

        # Show popular palettes
        palettes = {
            "Viridis": plt.cm.viridis,
            "Plasma": plt.cm.plasma,
            "Inferno": plt.cm.inferno,
            "Coolwarm": plt.cm.coolwarm,
            "Spectral": plt.cm.Spectral,
        }

        fig, axes = plt.subplots(len(palettes), 1, figsize=(10, 3))
        for ax, (name, cmap) in zip(axes, palettes.items()):
            gradient = np.linspace(0, 1, 256).reshape(1, -1)
            ax.imshow(gradient, aspect="auto", cmap=cmap)
            ax.set_ylabel(name, fontsize=10, fontweight="bold", rotation=0, labelpad=60)
            ax.set_xticks([]); ax.set_yticks([])
        fig.suptitle("Popular Colormaps", fontweight="bold", fontsize=14)
        plt.tight_layout(); st.pyplot(fig)
        st.markdown("---")

    # ── Step 5: Grid ──
    if step_check(5, "Grid customization", PAGE):
        st.markdown("#### 📏 Grid Customization")
        lib = library_selector(f"{PAGE}_5", default="Matplotlib", options=["Matplotlib", "Plotly"])

        grid_on = st.checkbox("Show grid", True, key=f"{PAGE}_grid")
        grid_style = st.selectbox("Grid style", ["solid", "dashed", "dotted"], key=f"{PAGE}_gs")
        grid_alpha = st.slider("Grid opacity", 0.0, 1.0, 0.3, key=f"{PAGE}_ga")

        np.random.seed(3)
        x = np.linspace(0, 10, 50)
        y = np.sin(x) * np.exp(-x / 10) * 5

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(9, 4))
            ax.plot(x, y, color=PALETTE[0], linewidth=2)
            if grid_on:
                ax.grid(True, linestyle={"solid": "-", "dashed": "--", "dotted": ":"}[grid_style],
                        alpha=grid_alpha, color="#888")
            else:
                ax.grid(False)
            ax.set_title("Grid Customization", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.line(x=x, y=y, title="Grid Customization")
            fig.update_traces(line_color=PALETTE[0])
            fig.update_xaxes(showgrid=grid_on, griddash=grid_style,
                             gridcolor=f"rgba(136,136,136,{grid_alpha})")
            fig.update_yaxes(showgrid=grid_on, griddash=grid_style,
                             gridcolor=f"rgba(136,136,136,{grid_alpha})")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 6: Built-in styles ──
    if step_check(6, "Built-in styles & themes", PAGE):
        st.markdown("#### 🎭 Built-in Styles & Themes")

        import matplotlib.pyplot as plt
        styles = ["default", "seaborn-v0_8", "ggplot", "dark_background",
                  "bmh", "fivethirtyeight", "grayscale"]
        chosen = st.selectbox("Matplotlib style", styles, key=f"{PAGE}_style")

        show_code(f"""
plt.style.use("{chosen}")
""")

        with plt.style.context(chosen):
            np.random.seed(9)
            fig, ax = plt.subplots(figsize=(9, 4))
            for i in range(3):
                ax.plot(np.cumsum(np.random.randn(50)), label=f"Series {i+1}", linewidth=2)
            ax.legend()
            ax.set_title(f'Style: "{chosen}"', fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        st.markdown("---")

    # ── Step 7: Seaborn aesthetics ──
    if step_check(7, "Seaborn aesthetics (set_style, context, palette)", PAGE):
        st.markdown("#### 🌊 Seaborn Aesthetic Controls")
        import seaborn as sns, matplotlib.pyplot as plt

        c1, c2, c3 = st.columns(3)
        with c1:
            sns_style = st.selectbox("set_style", ["darkgrid", "whitegrid", "dark", "white", "ticks"],
                                     key=f"{PAGE}_sns_style")
        with c2:
            sns_context = st.selectbox("set_context", ["paper", "notebook", "talk", "poster"],
                                       key=f"{PAGE}_sns_ctx")
        with c3:
            sns_palette = st.selectbox("Palette", ["deep", "muted", "bright", "pastel", "dark", "colorblind"],
                                       key=f"{PAGE}_sns_pal")

        show_code(f"""
sns.set_style("{sns_style}")
sns.set_context("{sns_context}")
sns.set_palette("{sns_palette}")
""")

        sns.set_style(sns_style)
        sns.set_context(sns_context)
        np.random.seed(7)
        tips_df = sns.load_dataset("tips")
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.boxplot(data=tips_df, x="day", y="total_bill", palette=sns_palette, ax=ax)
        ax.set_title(f'Seaborn: style="{sns_style}", context="{sns_context}"', fontweight="bold")
        plt.tight_layout(); st.pyplot(fig)

        # Reset to defaults
        sns.set_style("darkgrid")
        sns.set_context("notebook")


render()
