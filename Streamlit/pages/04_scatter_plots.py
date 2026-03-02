"""
Page 4 — Scatter Plots
Basic, color/size encoding, bubble, regression.
"""
import streamlit as st
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, get_active_df, numeric_cols, categorical_cols,
                   pick_xy, inject_custom_css)

st.set_page_config(page_title="Scatter Plots | DataViz", page_icon="⚡", layout="wide")
inject_custom_css()

PAGE = "scatter_plots"


def render():
    section_header("⚡", "Scatter Plots")
    st.markdown("Scatter plots reveal **relationships between two numeric variables**.")

    df = get_active_df("Tips")

    # ── Step 1: Basic scatter ──
    if step_check(1, "Basic scatter plot", PAGE):
        st.markdown("#### ⚡ Basic Scatter Plot")
        lib = library_selector(f"{PAGE}_1")

        nc = numeric_cols(df)
        if st.session_state.get("use_custom_data"):
            x_col, y_col = pick_xy(df, f"{PAGE}_1")
        else:
            x_col = nc[0] if len(nc) > 0 else df.columns[0]
            y_col = nc[1] if len(nc) > 1 else df.columns[1]

        if lib == "Matplotlib":
            show_code(f"""
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df["{x_col}"], df["{y_col}"], alpha=0.6, color="#667eea", edgecolors="white")
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(df[x_col], df[y_col], alpha=0.6, color="#667eea",
                       edgecolors="white", s=60)
            ax.set_xlabel(x_col); ax.set_ylabel(y_col)
            ax.set_title(f"{y_col} vs {x_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code(f"""
sns.scatterplot(data=df, x="{x_col}", y="{y_col}", alpha=0.6, color="#667eea")
""")
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.scatterplot(data=df, x=x_col, y=y_col, alpha=0.6,
                            color="#667eea", edgecolor="white", ax=ax)
            ax.set_title(f"{y_col} vs {x_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            show_code(f"""
fig = px.scatter(df, x="{x_col}", y="{y_col}", opacity=0.6)
""")
            import plotly.express as px
            fig = px.scatter(df, x=x_col, y=y_col, opacity=0.6,
                             color_discrete_sequence=["#667eea"],
                             title=f"{y_col} vs {x_col}")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 2: Color & size encoding ──
    if step_check(2, "Color & size encoding", PAGE):
        st.markdown("#### 🎨 Color & Size Encoding")
        lib = library_selector(f"{PAGE}_2")

        nc = numeric_cols(df)
        cc = categorical_cols(df)

        if st.session_state.get("use_custom_data"):
            x_col, y_col = pick_xy(df, f"{PAGE}_2")
            color_col = st.selectbox("Color by", cc + nc, key=f"{PAGE}_2_c")
            size_col = st.selectbox("Size by", nc, key=f"{PAGE}_2_s") if nc else None
        else:
            x_col = nc[0] if nc else df.columns[0]
            y_col = nc[1] if len(nc) > 1 else df.columns[1]
            color_col = cc[0] if cc else None
            size_col = nc[2] if len(nc) > 2 else None

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            scatter = ax.scatter(df[x_col], df[y_col],
                                 c=pd.factorize(df[color_col])[0] if color_col else "#667eea",
                                 s=df[size_col]*5 if size_col else 60,
                                 alpha=0.6, cmap="viridis", edgecolors="white")
            if color_col:
                plt.colorbar(scatter, ax=ax, label=color_col)
            ax.set_xlabel(x_col); ax.set_ylabel(y_col)
            ax.set_title("Color & Size Encoded Scatter", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.scatterplot(data=df, x=x_col, y=y_col,
                            hue=color_col, size=size_col,
                            palette="viridis", alpha=0.6, ax=ax)
            ax.set_title("Color & Size Encoded Scatter", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.scatter(df, x=x_col, y=y_col,
                             color=color_col, size=size_col,
                             opacity=0.7, title="Color & Size Encoded Scatter")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 3: Bubble chart ──
    if step_check(3, "Bubble chart", PAGE):
        st.markdown("#### 🫧 Bubble Chart")
        lib = library_selector(f"{PAGE}_3")

        np.random.seed(42)
        bdf = pd.DataFrame({
            "GDP (T$)": [21.4, 14.7, 5.1, 2.9, 2.7, 2.0, 1.8, 1.6, 1.5, 1.3],
            "Life Expectancy": [78.5, 76.9, 84.6, 83.0, 81.1, 82.6, 80.4, 73.2, 81.2, 77.3],
            "Population (M)": [331, 1402, 126, 67, 67, 83, 60, 1380, 38, 212],
            "Country": ["USA", "China", "Japan", "France", "UK",
                        "Germany", "Italy", "India", "Canada", "Brazil"],
        })

        show_code("""
# Bubble chart: x=GDP, y=Life Expectancy, size=Population
fig = px.scatter(bdf, x="GDP (T$)", y="Life Expectancy",
                 size="Population (M)", color="Country",
                 hover_name="Country", size_max=60)
""")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(9, 5))
            scatter = ax.scatter(bdf["GDP (T$)"], bdf["Life Expectancy"],
                                 s=bdf["Population (M)"] / 3, alpha=0.6,
                                 c=range(len(bdf)), cmap="Spectral", edgecolors="white")
            for _, row in bdf.iterrows():
                ax.annotate(row["Country"], (row["GDP (T$)"], row["Life Expectancy"]),
                            fontsize=8, ha="center")
            ax.set_xlabel("GDP (T$)"); ax.set_ylabel("Life Expectancy")
            ax.set_title("Bubble Chart — World Economies", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(9, 5))
            sns.scatterplot(data=bdf, x="GDP (T$)", y="Life Expectancy",
                            size="Population (M)", hue="Country",
                            sizes=(50, 600), alpha=0.6, ax=ax)
            ax.set_title("Bubble Chart — World Economies", fontweight="bold")
            ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=7)
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.scatter(bdf, x="GDP (T$)", y="Life Expectancy",
                             size="Population (M)", color="Country",
                             hover_name="Country", size_max=60,
                             title="Bubble Chart — World Economies")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 4: Regression ──
    if step_check(4, "Scatter with regression line", PAGE):
        st.markdown("#### 📐 Scatter with Regression Line")
        lib = library_selector(f"{PAGE}_4")

        nc = numeric_cols(df)
        x_col = nc[0] if nc else df.columns[0]
        y_col = nc[1] if len(nc) > 1 else df.columns[1]

        if lib == "Matplotlib":
            show_code(f"""
z = np.polyfit(df["{x_col}"], df["{y_col}"], 1)
p = np.poly1d(z)
ax.plot(df["{x_col}"], p(df["{x_col}"]), "r--", linewidth=2, label="Trend")
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(df[x_col], df[y_col], alpha=0.5, color="#667eea", edgecolors="white")
            z = np.polyfit(df[x_col].astype(float), df[y_col].astype(float), 1)
            p = np.poly1d(z)
            xs = np.linspace(df[x_col].min(), df[x_col].max(), 100)
            ax.plot(xs, p(xs), "--", color="#EF553B", linewidth=2, label="Trend")
            ax.legend(); ax.set_xlabel(x_col); ax.set_ylabel(y_col)
            ax.set_title(f"Regression: {y_col} vs {x_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            show_code(f"""
sns.regplot(data=df, x="{x_col}", y="{y_col}", scatter_kws={{"alpha": 0.5}})
""")
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.regplot(data=df, x=x_col, y=y_col, ax=ax,
                        scatter_kws={"alpha": 0.5, "color": "#667eea"},
                        line_kws={"color": "#EF553B"})
            ax.set_title(f"Regression: {y_col} vs {x_col}", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            show_code(f"""
fig = px.scatter(df, x="{x_col}", y="{y_col}", trendline="ols")
""")
            import plotly.express as px
            fig = px.scatter(df, x=x_col, y=y_col, trendline="ols",
                             opacity=0.6, color_discrete_sequence=["#667eea"],
                             title=f"Regression: {y_col} vs {x_col}")
            st.plotly_chart(fig, use_container_width=True)


render()
