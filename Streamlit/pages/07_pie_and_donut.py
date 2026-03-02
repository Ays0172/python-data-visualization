"""
Page 7 — Pie & Donut Charts
Pie, exploded, donut, labels, legends, shadows.
"""
import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector, info_card, inject_custom_css)

st.set_page_config(page_title="Pie & Donut | DataViz", page_icon="🥧", layout="wide")
inject_custom_css()

PAGE = "pie_donut"
PALETTE = ["#667eea", "#764ba2", "#f093fb", "#fda085", "#a18cd1", "#fbc2eb"]


def render():
    section_header("🥧", "Pie & Donut Charts")
    st.markdown("Pie charts show **proportions** of a whole. Use them sparingly — "
                "humans find angles harder to compare than lengths.")

    # ── Step 1: Basic pie ──
    if step_check(1, "Basic pie chart", PAGE):
        st.markdown("#### 🥧 Basic Pie Chart")
        lib = library_selector(f"{PAGE}_1")

        labels = ["Python", "JavaScript", "Java", "C++", "Other"]
        sizes = [35, 25, 18, 12, 10]

        if lib == "Matplotlib":
            show_code("""
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=palette, startangle=90)
ax.set_title("Language Popularity")
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=PALETTE,
                   startangle=90, textprops={"fontsize": 10})
            ax.set_title("Language Popularity", fontweight="bold", fontsize=14)
            st.pyplot(fig)
        elif lib == "Seaborn":
            st.info("Seaborn doesn't provide pie charts — using Matplotlib instead.")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=PALETTE,
                   startangle=90)
            ax.set_title("Language Popularity", fontweight="bold")
            st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.pie(names=labels, values=sizes, title="Language Popularity",
                         color_discrete_sequence=PALETTE)
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 2: Exploded + shadows ──
    if step_check(2, "Exploded slices & shadows", PAGE):
        st.markdown("#### 💥 Exploded Slices & Shadows")
        lib = library_selector(f"{PAGE}_2")

        labels = ["Rent", "Food", "Transport", "Entertainment", "Savings"]
        sizes = [35, 20, 15, 10, 20]
        explode = (0.08, 0, 0, 0.15, 0)

        if lib == "Matplotlib":
            show_code("""
explode = (0.08, 0, 0, 0.15, 0)  # pull out slices
ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
       shadow=True, colors=palette)
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%",
                   shadow=True, colors=PALETTE, startangle=140,
                   wedgeprops={"edgecolor": "white", "linewidth": 1.5})
            ax.set_title("Monthly Budget", fontweight="bold", fontsize=14)
            st.pyplot(fig)
        elif lib == "Seaborn":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%",
                   shadow=True, colors=PALETTE, startangle=140,
                   wedgeprops={"edgecolor": "white", "linewidth": 1.5})
            ax.set_title("Monthly Budget", fontweight="bold")
            st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.pie(names=labels, values=sizes, title="Monthly Budget",
                         color_discrete_sequence=PALETTE)
            fig.update_traces(pull=[0.08, 0, 0, 0.15, 0], textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 3: Donut chart ──
    if step_check(3, "Donut chart", PAGE):
        st.markdown("#### 🍩 Donut Chart")
        lib = library_selector(f"{PAGE}_3")

        labels = ["Chrome", "Safari", "Firefox", "Edge", "Other"]
        sizes = [64, 19, 4, 4, 9]

        if lib == "Matplotlib":
            show_code("""
# Create a donut by adding a white circle in the center
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                    colors=palette, pctdistance=0.8)
centre = plt.Circle((0, 0), 0.55, fc='white')
ax.add_artist(centre)
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 6))
            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, autopct="%1.1f%%",
                colors=PALETTE, pctdistance=0.8, startangle=90,
                wedgeprops={"edgecolor": "white", "linewidth": 2})
            centre = plt.Circle((0, 0), 0.55, fc="white")
            ax.add_artist(centre)
            ax.set_title("Browser Market Share", fontweight="bold", fontsize=14)
            st.pyplot(fig)
        elif lib == "Seaborn":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(sizes, labels=labels, autopct="%1.1f%%",
                   colors=PALETTE, pctdistance=0.8, startangle=90,
                   wedgeprops={"edgecolor": "white", "linewidth": 2})
            centre = plt.Circle((0, 0), 0.55, fc="white")
            ax.add_artist(centre)
            ax.set_title("Browser Market Share", fontweight="bold")
            st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.pie(names=labels, values=sizes, title="Browser Market Share",
                         color_discrete_sequence=PALETTE, hole=0.45)
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 4: Labels, legends, rotation ──
    if step_check(4, "Labels, legends & rotation", PAGE):
        st.markdown("#### 🏷️ Labels, Legends & Rotation")
        lib = library_selector(f"{PAGE}_4")

        labels = ["A", "B", "C", "D", "E"]
        sizes = [15, 30, 25, 10, 20]

        col1, col2 = st.columns(2)
        start_angle = col1.slider("Start Angle", 0, 360, 90, key=f"{PAGE}_4_angle")
        show_pct = col2.checkbox("Show Percentages", True, key=f"{PAGE}_4_pct")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 6))
            wedges, texts = ax.pie(sizes, labels=labels if not show_pct else None,
                                    colors=PALETTE, startangle=start_angle,
                                    wedgeprops={"edgecolor": "white"})[:2]
            if show_pct:
                ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=PALETTE,
                       startangle=start_angle, wedgeprops={"edgecolor": "white"})
            ax.legend(labels, title="Categories", loc="center left",
                      bbox_to_anchor=(1, 0.5))
            ax.set_title("Custom Pie Chart", fontweight="bold", fontsize=14)
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(sizes, labels=labels, autopct="%1.1f%%" if show_pct else None,
                   colors=PALETTE, startangle=start_angle,
                   wedgeprops={"edgecolor": "white"})
            ax.legend(labels, title="Categories", loc="center left",
                      bbox_to_anchor=(1, 0.5))
            ax.set_title("Custom Pie Chart", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.pie(names=labels, values=sizes, title="Custom Pie Chart",
                         color_discrete_sequence=PALETTE)
            fig.update_traces(
                rotation=start_angle,
                textinfo="percent+label" if show_pct else "label"
            )
            st.plotly_chart(fig, use_container_width=True)


render()
