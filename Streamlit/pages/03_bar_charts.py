"""
Page 3 — Bar Charts
Basic, grouped, stacked, horizontal, histograms.
"""
import streamlit as st
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, get_active_df, numeric_cols, categorical_cols, inject_custom_css)

st.set_page_config(page_title="Bar Charts | DataViz", page_icon="📊", layout="wide")
inject_custom_css()

PAGE = "bar_charts"

PALETTE = ["#667eea", "#764ba2", "#f093fb", "#fda085", "#a18cd1", "#fbc2eb"]


def render():
    section_header("📊", "Bar Charts")
    st.markdown("Bar charts compare **categorical data** using rectangular bars.")

    df = get_active_df("Tips")

    # ── Step 1: Basic bar ──
    if step_check(1, "Basic bar chart", PAGE):
        st.markdown("#### 📊 Basic Bar Chart")
        lib = library_selector(f"{PAGE}_1")

        categories = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        values = [12, 19, 8, 15, 22]

        if lib == "Matplotlib":
            show_code("""
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(categories, values, color="#667eea", edgecolor="white", linewidth=0.8)
ax.set_title("Weekly Sales")
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(categories, values, color="#667eea", edgecolor="white", linewidth=0.8)
            ax.set_title("Weekly Sales", fontweight="bold")
            ax.set_ylabel("Units")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code("""
sns.barplot(x=categories, y=values, palette="viridis")
""")
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=categories, y=values, palette=PALETTE[:5], ax=ax)
            ax.set_title("Weekly Sales", fontweight="bold"); ax.set_ylabel("Units")
            plt.tight_layout(); st.pyplot(fig)
        else:
            show_code("""
fig = px.bar(x=categories, y=values, color=categories, title="Weekly Sales")
""")
            import plotly.express as px
            fig = px.bar(x=categories, y=values, color=categories,
                         color_discrete_sequence=PALETTE, title="Weekly Sales",
                         labels={"x": "Day", "y": "Units"})
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 2: Grouped bar ──
    if step_check(2, "Grouped bar chart", PAGE):
        st.markdown("#### 📊 Grouped Bar Chart")
        lib = library_selector(f"{PAGE}_2")

        gdf = pd.DataFrame({
            "Quarter": ["Q1", "Q2", "Q3", "Q4"],
            "Product A": [20, 35, 30, 40],
            "Product B": [25, 32, 34, 20],
            "Product C": [15, 25, 28, 35],
        })

        if lib == "Matplotlib":
            show_code("""
x = np.arange(len(quarters))
width = 0.25
ax.bar(x - width, prodA, width, label='Product A')
ax.bar(x,         prodB, width, label='Product B')
ax.bar(x + width, prodC, width, label='Product C')
""")
            import matplotlib.pyplot as plt
            x = np.arange(4)
            w = 0.25
            fig, ax = plt.subplots(figsize=(9, 4))
            ax.bar(x - w, gdf["Product A"], w, label="Product A", color=PALETTE[0])
            ax.bar(x, gdf["Product B"], w, label="Product B", color=PALETTE[1])
            ax.bar(x + w, gdf["Product C"], w, label="Product C", color=PALETTE[2])
            ax.set_xticks(x); ax.set_xticklabels(gdf["Quarter"])
            ax.legend(); ax.set_title("Quarterly Sales by Product", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code("""
melted = gdf.melt("Quarter", var_name="Product", value_name="Sales")
sns.barplot(data=melted, x="Quarter", y="Sales", hue="Product")
""")
            import seaborn as sns, matplotlib.pyplot as plt
            melted = gdf.melt("Quarter", var_name="Product", value_name="Sales")
            fig, ax = plt.subplots(figsize=(9, 4))
            sns.barplot(data=melted, x="Quarter", y="Sales", hue="Product",
                        palette=PALETTE[:3], ax=ax)
            ax.set_title("Quarterly Sales by Product", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            show_code("""
melted = gdf.melt("Quarter", var_name="Product", value_name="Sales")
fig = px.bar(melted, x="Quarter", y="Sales", color="Product", barmode="group")
""")
            import plotly.express as px
            melted = gdf.melt("Quarter", var_name="Product", value_name="Sales")
            fig = px.bar(melted, x="Quarter", y="Sales", color="Product",
                         barmode="group", color_discrete_sequence=PALETTE,
                         title="Quarterly Sales by Product")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 3: Stacked bar ──
    if step_check(3, "Stacked bar chart", PAGE):
        st.markdown("#### 📊 Stacked Bar Chart")
        lib = library_selector(f"{PAGE}_3")

        sdf = pd.DataFrame({
            "Region": ["North", "South", "East", "West"],
            "Online": [30, 45, 25, 40],
            "In-Store": [50, 35, 45, 30],
            "Wholesale": [20, 20, 30, 30],
        })

        if lib == "Matplotlib":
            show_code("""
ax.bar(regions, online, label='Online', color='#667eea')
ax.bar(regions, instore, bottom=online, label='In-Store', color='#764ba2')
ax.bar(regions, wholesale, bottom=online+instore, label='Wholesale', color='#f093fb')
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(sdf["Region"], sdf["Online"], label="Online", color=PALETTE[0])
            ax.bar(sdf["Region"], sdf["In-Store"], bottom=sdf["Online"],
                   label="In-Store", color=PALETTE[1])
            ax.bar(sdf["Region"], sdf["Wholesale"],
                   bottom=sdf["Online"]+sdf["In-Store"],
                   label="Wholesale", color=PALETTE[2])
            ax.legend(); ax.set_title("Sales by Channel", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code("""
melted = sdf.melt("Region", var_name="Channel", value_name="Sales")
# Seaborn doesn't have a direct stacked bar — use Matplotlib stacking
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(sdf["Region"], sdf["Online"], label="Online", color=PALETTE[0])
            ax.bar(sdf["Region"], sdf["In-Store"], bottom=sdf["Online"],
                   label="In-Store", color=PALETTE[1])
            ax.bar(sdf["Region"], sdf["Wholesale"],
                   bottom=sdf["Online"]+sdf["In-Store"],
                   label="Wholesale", color=PALETTE[2])
            ax.legend(); ax.set_title("Sales by Channel (Stacked)", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            show_code("""
fig = px.bar(melted, x="Region", y="Sales", color="Channel", barmode="stack")
""")
            import plotly.express as px
            melted = sdf.melt("Region", var_name="Channel", value_name="Sales")
            fig = px.bar(melted, x="Region", y="Sales", color="Channel",
                         color_discrete_sequence=PALETTE, title="Sales by Channel (Stacked)")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 4: Horizontal bars ──
    if step_check(4, "Horizontal bar chart", PAGE):
        st.markdown("#### ↔️ Horizontal Bar Chart")
        lib = library_selector(f"{PAGE}_4")

        langs = ["Python", "JavaScript", "Java", "C++", "Go", "Rust"]
        popularity = [92, 85, 72, 65, 55, 48]

        if lib == "Matplotlib":
            show_code("""
ax.barh(langs, popularity, color=palette)
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(langs, popularity, color=PALETTE)
            ax.set_xlabel("Popularity Index"); ax.set_title("Language Popularity", fontweight="bold")
            ax.invert_yaxis()
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=popularity, y=langs, palette=PALETTE, ax=ax, orient="h")
            ax.set_xlabel("Popularity Index"); ax.set_title("Language Popularity", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.bar(x=popularity, y=langs, orientation="h", color=langs,
                         color_discrete_sequence=PALETTE, title="Language Popularity",
                         labels={"x": "Popularity Index", "y": "Language"})
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 5: Histogram vs Bar ──
    if step_check(5, "Histograms vs bar charts", PAGE):
        st.markdown("#### 📊 Histograms vs Bar Charts")

        info_card(
            "Key Difference",
            "<b>Bar charts</b> compare categorical data. <b>Histograms</b> show the "
            "distribution of continuous data by grouping values into bins."
        )

        lib = library_selector(f"{PAGE}_5")
        nc = numeric_cols(df)
        hist_col = nc[0] if nc else df.columns[0]

        if lib == "Matplotlib":
            show_code(f"""
ax.hist(df["{hist_col}"], bins=20, color="#667eea", edgecolor="white", alpha=0.8)
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.hist(df[hist_col], bins=20, color="#667eea", edgecolor="white", alpha=0.8)
            ax.set_title(f"Distribution of {hist_col}", fontweight="bold")
            ax.set_xlabel(hist_col); ax.set_ylabel("Frequency")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code(f"""
sns.histplot(df["{hist_col}"], bins=20, kde=True, color="#667eea")
""")
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(df[hist_col], bins=20, kde=True, color="#667eea", ax=ax)
            ax.set_title(f"Distribution of {hist_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            show_code(f"""
fig = px.histogram(df, x="{hist_col}", nbins=20, title="Distribution of {hist_col}")
""")
            import plotly.express as px
            fig = px.histogram(df, x=hist_col, nbins=20,
                               color_discrete_sequence=["#667eea"],
                               title=f"Distribution of {hist_col}")
            st.plotly_chart(fig, use_container_width=True)


render()
