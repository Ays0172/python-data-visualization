"""
Page 6 — Area & Fill Charts
Area charts, stack plots, fill between.
"""
import streamlit as st
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, inject_custom_css)

st.set_page_config(page_title="Area & Fill | DataViz", page_icon="🌊", layout="wide")
inject_custom_css()

PAGE = "area_fill"
PALETTE = ["#667eea", "#764ba2", "#f093fb", "#fda085", "#a18cd1"]


def render():
    section_header("🌊", "Area & Fill Charts")
    st.markdown("Area charts emphasize the **magnitude** of values over time by filling below the line.")

    # ── Step 1: Basic area ──
    if step_check(1, "Basic area chart", PAGE):
        st.markdown("#### 🌊 Basic Area Chart")
        lib = library_selector(f"{PAGE}_1")

        np.random.seed(3)
        x = np.arange(1, 31)
        y = np.cumsum(np.random.randn(30)) + 50

        if lib == "Matplotlib":
            show_code("""
ax.fill_between(x, y, alpha=0.3, color="#667eea")
ax.plot(x, y, color="#667eea", linewidth=2)
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.fill_between(x, y, alpha=0.25, color=PALETTE[0])
            ax.plot(x, y, color=PALETTE[0], linewidth=2)
            ax.set_title("Monthly Revenue", fontweight="bold")
            ax.set_xlabel("Day"); ax.set_ylabel("Revenue ($K)")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.fill_between(x, y, alpha=0.25, color=PALETTE[0])
            sns.lineplot(x=x, y=y, color=PALETTE[0], ax=ax)
            ax.set_title("Monthly Revenue", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.area(x=x, y=y, title="Monthly Revenue",
                          labels={"x": "Day", "y": "Revenue ($K)"})
            fig.update_traces(line_color=PALETTE[0], fillcolor="rgba(102,126,234,0.2)")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 2: Stacked area ──
    if step_check(2, "Stacked area (stack plot)", PAGE):
        st.markdown("#### 📚 Stacked Area Chart")
        lib = library_selector(f"{PAGE}_2")

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        web = [10, 12, 15, 14, 18, 20, 22, 25, 23, 21, 19, 24]
        mobile = [5, 7, 8, 10, 12, 14, 15, 16, 18, 20, 22, 25]
        desktop = [8, 8, 7, 7, 6, 5, 5, 4, 4, 3, 3, 2]

        if lib == "Matplotlib":
            show_code("""
ax.stackplot(months, web, mobile, desktop,
             labels=['Web', 'Mobile', 'Desktop'],
             colors=palette, alpha=0.8)
ax.legend(loc='upper left')
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.stackplot(months, web, mobile, desktop,
                         labels=["Web", "Mobile", "Desktop"],
                         colors=PALETTE[:3], alpha=0.8)
            ax.legend(loc="upper left")
            ax.set_title("Traffic Sources — Stacked Area", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.stackplot(months, web, mobile, desktop,
                         labels=["Web", "Mobile", "Desktop"],
                         colors=PALETTE[:3], alpha=0.8)
            ax.legend(loc="upper left")
            ax.set_title("Traffic Sources — Stacked Area", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
            st.caption("_Seaborn uses Matplotlib's `stackplot` under the hood._")
        else:
            import plotly.graph_objects as go
            fig = go.Figure()
            for name, vals, color in zip(["Web", "Mobile", "Desktop"],
                                          [web, mobile, desktop], PALETTE[:3]):
                fig.add_trace(go.Scatter(x=months, y=vals, name=name,
                                         stackgroup="one",
                                         line=dict(color=color)))
            fig.update_layout(title="Traffic Sources — Stacked Area")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 3: Fill between ──
    if step_check(3, "Fill between two lines", PAGE):
        st.markdown("#### ↕️ Fill Between Two Lines")
        lib = library_selector(f"{PAGE}_3")

        np.random.seed(5)
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x) * 3 + 10
        y2 = np.sin(x) * 3 + 10 + np.random.uniform(1, 3, 100)

        if lib == "Matplotlib":
            show_code("""
ax.fill_between(x, y1, y2, alpha=0.3, color="#667eea", label="Confidence Band")
ax.plot(x, y1, color="#667eea", linewidth=2, label="Lower")
ax.plot(x, y2, color="#764ba2", linewidth=2, label="Upper")
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.fill_between(x, y1, y2, alpha=0.25, color=PALETTE[0])
            ax.plot(x, y1, color=PALETTE[0], linewidth=2, label="Lower Bound")
            ax.plot(x, y2, color=PALETTE[1], linewidth=2, label="Upper Bound")
            ax.legend(); ax.set_title("Confidence Band", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.fill_between(x, y1, y2, alpha=0.25, color=PALETTE[0])
            ax.plot(x, y1, color=PALETTE[0], linewidth=2, label="Lower")
            ax.plot(x, y2, color=PALETTE[1], linewidth=2, label="Upper")
            ax.legend(); ax.set_title("Confidence Band", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=np.concatenate([x, x[::-1]]),
                                     y=np.concatenate([y2, y1[::-1]]),
                                     fill="toself", fillcolor="rgba(102,126,234,0.15)",
                                     line=dict(color="rgba(255,255,255,0)"),
                                     name="Band"))
            fig.add_trace(go.Scatter(x=x, y=y1, line=dict(color=PALETTE[0]), name="Lower"))
            fig.add_trace(go.Scatter(x=x, y=y2, line=dict(color=PALETTE[1]), name="Upper"))
            fig.update_layout(title="Confidence Band")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 4: Gradient fill ──
    if step_check(4, "Area with gradient effect", PAGE):
        st.markdown("#### 🌈 Gradient-Style Area")
        lib = library_selector(f"{PAGE}_4", default="Plotly", options=["Matplotlib", "Plotly"])

        np.random.seed(8)
        x = np.arange(50)
        y = np.cumsum(np.random.randn(50)) + 30

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            from matplotlib.collections import PolyCollection
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(x, y, color=PALETTE[0], linewidth=2)
            # Simulate gradient by layered filled regions
            for i in range(10):
                ax.fill_between(x, y - (y.max()-y.min())*i/10, y,
                                alpha=0.03, color=PALETTE[0])
            ax.fill_between(x, 0, y, alpha=0.08, color=PALETTE[0])
            ax.set_title("Gradient Fill Effect", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.graph_objects as go
            fig = go.Figure(go.Scatter(x=x, y=y, fill="tozeroy",
                                        line=dict(color=PALETTE[0], width=2),
                                        fillgradient=dict(
                                            type="vertical",
                                            colorscale=[(0, "rgba(102,126,234,0)"),
                                                        (1, "rgba(102,126,234,0.4)")]),
                                        ))
            fig.update_layout(title="Gradient Fill Effect")
            st.plotly_chart(fig, use_container_width=True)


render()
