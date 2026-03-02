"""
Page 2 — Line Charts
Basic, multi-line, styled, time-series line plots.
"""
import streamlit as st
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, get_active_df, pick_xy, numeric_cols, inject_custom_css)

st.set_page_config(page_title="Line Charts | DataViz", page_icon="📈", layout="wide")
inject_custom_css()

PAGE = "line_charts"


def render():
    section_header("📈", "Line Charts")
    st.markdown("Line charts are ideal for showing **trends over time** or continuous data.")

    df = get_active_df("Stocks (AAPL)")

    # ── Step 1: Basic line ──
    if step_check(1, "Basic line plot", PAGE):
        st.markdown("#### 📏 Basic Line Plot")
        lib = library_selector(f"{PAGE}_1")

        if st.session_state.get("use_custom_data", False) and "_uploaded_file" in st.session_state:
            x_col, y_col = pick_xy(df, f"{PAGE}_1")
        else:
            x_col, y_col = "Date", "Close"
            if x_col not in df.columns:
                x_col, y_col = df.columns[0], numeric_cols(df)[0] if numeric_cols(df) else df.columns[1]

        show_code(f"""
# Basic line plot
x = df["{x_col}"]
y = df["{y_col}"]
""")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df[x_col], df[y_col], color="#667eea", linewidth=2)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"{y_col} over {x_col}", fontweight="bold")
            ax.tick_params(axis="x", rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        elif lib == "Seaborn":
            import matplotlib.pyplot as plt
            import seaborn as sns
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=df, x=x_col, y=y_col, color="#667eea", ax=ax)
            ax.set_title(f"{y_col} over {x_col}", fontweight="bold")
            ax.tick_params(axis="x", rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
            fig.update_traces(line_color="#667eea")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

    # ── Step 2: Multi-line ──
    if step_check(2, "Multi-line plot", PAGE):
        st.markdown("#### 🔀 Multi-Line Plot")
        lib = library_selector(f"{PAGE}_2")

        # Generate sample multi-line data
        np.random.seed(0)
        x = np.linspace(0, 10, 100)
        lines = {"x": x, "sin(x)": np.sin(x), "cos(x)": np.cos(x), "sin(2x)/2": np.sin(2*x)/2}
        mdf = pd.DataFrame(lines)

        show_code("""
import numpy as np
x = np.linspace(0, 10, 100)
# Plot sin(x), cos(x), sin(2x)/2 on the same axes
""")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 4))
            for col in ["sin(x)", "cos(x)", "sin(2x)/2"]:
                ax.plot(mdf["x"], mdf[col], label=col, linewidth=2)
            ax.legend()
            ax.set_title("Multiple Trig Functions", fontweight="bold")
            ax.set_xlabel("x"); ax.set_ylabel("y")
            plt.tight_layout()
            st.pyplot(fig)
        elif lib == "Seaborn":
            import matplotlib.pyplot as plt
            import seaborn as sns
            melted = mdf.melt("x", var_name="Function", value_name="y")
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=melted, x="x", y="y", hue="Function", ax=ax)
            ax.set_title("Multiple Trig Functions", fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            import plotly.express as px
            melted = mdf.melt("x", var_name="Function", value_name="y")
            fig = px.line(melted, x="x", y="y", color="Function",
                          title="Multiple Trig Functions")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

    # ── Step 3: Styled lines ──
    if step_check(3, "Line styles, markers & colors", PAGE):
        st.markdown("#### 🎨 Line Styles, Markers & Colors")
        lib = library_selector(f"{PAGE}_3")

        np.random.seed(1)
        x = np.arange(1, 11)
        y1 = np.random.randint(2, 10, 10)
        y2 = np.random.randint(2, 10, 10)
        y3 = np.random.randint(2, 10, 10)

        if lib == "Matplotlib":
            show_code("""
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y1, 'o-',  color="#667eea", linewidth=2, label="Solid + circles")
ax.plot(x, y2, 's--', color="#764ba2", linewidth=2, label="Dashed + squares")
ax.plot(x, y3, '^:',  color="#f093fb", linewidth=2, label="Dotted + triangles")
ax.legend()
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(x, y1, "o-", color="#667eea", linewidth=2, label="Solid + circles")
            ax.plot(x, y2, "s--", color="#764ba2", linewidth=2, label="Dashed + squares")
            ax.plot(x, y3, "^:", color="#f093fb", linewidth=2, label="Dotted + triangles")
            ax.legend()
            ax.set_title("Line Styles & Markers", fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig)
        elif lib == "Seaborn":
            show_code("""
# Seaborn uses style parameter for line styles
sns.lineplot(data=df_melted, x="x", y="y", hue="Series",
             style="Series", markers=True, dashes=True)
""")
            import matplotlib.pyplot as plt
            import seaborn as sns
            sdf = pd.DataFrame({"x": np.tile(x, 3),
                                "y": np.concatenate([y1, y2, y3]),
                                "Series": ["A"]*10 + ["B"]*10 + ["C"]*10})
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=sdf, x="x", y="y", hue="Series", style="Series",
                         markers=True, dashes=True, ax=ax,
                         palette=["#667eea", "#764ba2", "#f093fb"])
            ax.set_title("Line Styles & Markers", fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            show_code("""
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers',
                         line=dict(dash='solid'),  name='Solid'))
fig.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers',
                         line=dict(dash='dash'),   name='Dashed'))
fig.add_trace(go.Scatter(x=x, y=y3, mode='lines+markers',
                         line=dict(dash='dot'),    name='Dotted'))
""")
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y1, mode="lines+markers",
                                     line=dict(dash="solid", color="#667eea"), name="Solid"))
            fig.add_trace(go.Scatter(x=x, y=y2, mode="lines+markers",
                                     line=dict(dash="dash", color="#764ba2"), name="Dashed"))
            fig.add_trace(go.Scatter(x=x, y=y3, mode="lines+markers",
                                     line=dict(dash="dot", color="#f093fb"), name="Dotted"))
            fig.update_layout(title="Line Styles & Markers")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

    # ── Step 4: Time series ──
    if step_check(4, "Time-series line chart", PAGE):
        st.markdown("#### 🕐 Time-Series Line Chart")
        lib = library_selector(f"{PAGE}_4")

        stock = get_active_df("Stocks (AAPL)")
        if "Date" in stock.columns and "Close" in stock.columns:
            ts_x, ts_y = "Date", "Close"
        else:
            nc = numeric_cols(stock)
            ts_x = stock.columns[0]
            ts_y = nc[0] if nc else stock.columns[1]

        info_card("Time-Series", "Stock data is a classic example. The x-axis shows dates and the y-axis shows closing prices.")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(stock[ts_x], stock[ts_y], color="#667eea", linewidth=1.5)
            ax.fill_between(range(len(stock)), stock[ts_y], alpha=0.15, color="#667eea")
            ax.set_title(f"{ts_y} over Time", fontweight="bold")
            ax.set_xlabel(ts_x); ax.set_ylabel(ts_y)
            ax.tick_params(axis="x", rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        elif lib == "Seaborn":
            import matplotlib.pyplot as plt
            import seaborn as sns
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=stock, x=ts_x, y=ts_y, color="#667eea", ax=ax)
            ax.set_title(f"{ts_y} over Time", fontweight="bold")
            ax.tick_params(axis="x", rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.line(stock, x=ts_x, y=ts_y, title=f"{ts_y} over Time")
            fig.update_traces(line_color="#667eea",
                              fill="tozeroy", fillcolor="rgba(102,126,234,0.1)")
            st.plotly_chart(fig, use_container_width=True)


render()
