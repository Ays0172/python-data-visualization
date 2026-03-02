"""
Page 10 — Subplots & Layouts
Grid layouts, shared axes, mixed chart types.
"""
import streamlit as st
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, get_active_df, numeric_cols, inject_custom_css)

st.set_page_config(page_title="Subplots & Layouts | DataViz", page_icon="🔲", layout="wide")
inject_custom_css()

PAGE = "subplots"
PALETTE = ["#667eea", "#764ba2", "#f093fb", "#fda085", "#a18cd1", "#fbc2eb"]


def render():
    section_header("🔲", "Subplots & Layouts")
    st.markdown("Arrange **multiple charts in a grid** to compare side by side.")

    df = get_active_df("Tips")
    nc = numeric_cols(df)

    # ── Step 1: Basic subplots ──
    if step_check(1, "Creating subplots (rows × cols)", PAGE):
        st.markdown("#### 🔲 Basic Subplot Grid")
        lib = library_selector(f"{PAGE}_1")

        rows = st.slider("Rows", 1, 3, 2, key=f"{PAGE}_rows")
        cols = st.slider("Cols", 1, 3, 2, key=f"{PAGE}_cols")

        if lib in ("Matplotlib", "Seaborn"):
            show_code(f"""
fig, axes = plt.subplots({rows}, {cols}, figsize=(12, 8))
for i, ax in enumerate(axes.flat):
    ax.plot(np.random.randn(50), color=palette[i % len(palette)])
    ax.set_title(f"Subplot {{i+1}}")
plt.tight_layout()
""")
            import matplotlib.pyplot as plt
            fig, axes = plt.subplots(rows, cols, figsize=(12, 3 * rows))
            axes_flat = np.array(axes).flatten()
            for i, ax in enumerate(axes_flat):
                np.random.seed(i)
                ax.plot(np.cumsum(np.random.randn(50)), color=PALETTE[i % len(PALETTE)], linewidth=2)
                ax.set_title(f"Subplot {i+1}", fontsize=10, fontweight="bold")
                ax.grid(alpha=0.3)
            plt.suptitle(f"{rows}×{cols} Subplot Grid", fontweight="bold", fontsize=14)
            plt.tight_layout(); st.pyplot(fig)
        else:
            show_code(f"""
from plotly.subplots import make_subplots
fig = make_subplots(rows={rows}, cols={cols})
""")
            from plotly.subplots import make_subplots
            import plotly.graph_objects as go
            fig = make_subplots(rows=rows, cols=cols,
                                subplot_titles=[f"Subplot {i+1}" for i in range(rows*cols)])
            idx = 0
            for r in range(1, rows+1):
                for c in range(1, cols+1):
                    np.random.seed(idx)
                    fig.add_trace(go.Scatter(
                        y=np.cumsum(np.random.randn(50)), mode="lines",
                        line=dict(color=PALETTE[idx % len(PALETTE)]),
                        name=f"Series {idx+1}"), row=r, col=c)
                    idx += 1
            fig.update_layout(title_text=f"{rows}×{cols} Subplot Grid", height=300*rows,
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 2: Shared axes ──
    if step_check(2, "Shared axes", PAGE):
        st.markdown("#### 🔗 Shared Axes")
        lib = library_selector(f"{PAGE}_2")

        np.random.seed(10)
        x = np.linspace(0, 2 * np.pi, 100)

        if lib in ("Matplotlib", "Seaborn"):
            show_code("""
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12, 4))
ax1.plot(x, np.sin(x))   # Same y-range
ax2.plot(x, np.cos(x))   # for comparison
""")
            import matplotlib.pyplot as plt
            fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12, 4))
            ax1.plot(x, np.sin(x), color=PALETTE[0], linewidth=2)
            ax1.set_title("sin(x)", fontweight="bold"); ax1.set_xlabel("x")
            ax1.fill_between(x, np.sin(x), alpha=0.15, color=PALETTE[0])
            ax2.plot(x, np.cos(x), color=PALETTE[1], linewidth=2)
            ax2.set_title("cos(x)", fontweight="bold"); ax2.set_xlabel("x")
            ax2.fill_between(x, np.cos(x), alpha=0.15, color=PALETTE[1])
            fig.suptitle("Shared Y-Axis", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            from plotly.subplots import make_subplots
            import plotly.graph_objects as go
            fig = make_subplots(rows=1, cols=2, shared_yaxes=True,
                                subplot_titles=["sin(x)", "cos(x)"])
            fig.add_trace(go.Scatter(x=x, y=np.sin(x), line=dict(color=PALETTE[0]),
                                     fill="tozeroy", name="sin"), row=1, col=1)
            fig.add_trace(go.Scatter(x=x, y=np.cos(x), line=dict(color=PALETTE[1]),
                                     fill="tozeroy", name="cos"), row=1, col=2)
            fig.update_layout(title_text="Shared Y-Axis")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 3: Mixed chart types ──
    if step_check(3, "Mixed chart types in subplots", PAGE):
        st.markdown("#### 🎲 Mixed Chart Types")
        lib = library_selector(f"{PAGE}_3")

        np.random.seed(42)
        bar_data = [15, 25, 20, 30, 18]
        line_data = np.cumsum(np.random.randn(30)) + 50
        pie_data = [35, 25, 20, 20]
        hist_data = np.random.randn(200)

        if lib in ("Matplotlib", "Seaborn"):
            show_code("""
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0,0].bar(...)    # Bar chart
axes[0,1].plot(...)   # Line chart
axes[1,0].pie(...)    # Pie chart
axes[1,1].hist(...)   # Histogram
""")
            import matplotlib.pyplot as plt
            fig, axes = plt.subplots(2, 2, figsize=(12, 9))

            axes[0, 0].bar(["A", "B", "C", "D", "E"], bar_data, color=PALETTE[:5])
            axes[0, 0].set_title("Bar Chart", fontweight="bold")

            axes[0, 1].plot(line_data, color=PALETTE[0], linewidth=2)
            axes[0, 1].fill_between(range(30), line_data, alpha=0.15, color=PALETTE[0])
            axes[0, 1].set_title("Line Chart", fontweight="bold")

            axes[1, 0].pie(pie_data, labels=["W", "X", "Y", "Z"], autopct="%1.0f%%",
                           colors=PALETTE[:4])
            axes[1, 0].set_title("Pie Chart", fontweight="bold")

            axes[1, 1].hist(hist_data, bins=25, color=PALETTE[1], edgecolor="white")
            axes[1, 1].set_title("Histogram", fontweight="bold")

            fig.suptitle("Mixed Chart Types", fontweight="bold", fontsize=14)
            plt.tight_layout(); st.pyplot(fig)
        else:
            from plotly.subplots import make_subplots
            import plotly.graph_objects as go
            fig = make_subplots(rows=2, cols=2,
                                specs=[[{"type": "bar"}, {"type": "scatter"}],
                                       [{"type": "pie"}, {"type": "histogram"}]],
                                subplot_titles=["Bar", "Line", "Pie", "Histogram"])
            fig.add_trace(go.Bar(x=["A","B","C","D","E"], y=bar_data,
                                  marker_color=PALETTE[:5]), row=1, col=1)
            fig.add_trace(go.Scatter(y=line_data, mode="lines",
                                      line=dict(color=PALETTE[0]),
                                      fill="tozeroy"), row=1, col=2)
            fig.add_trace(go.Pie(labels=["W","X","Y","Z"], values=pie_data,
                                  marker=dict(colors=PALETTE[:4])), row=2, col=1)
            fig.add_trace(go.Histogram(x=hist_data, marker_color=PALETTE[1]),
                          row=2, col=2)
            fig.update_layout(title_text="Mixed Chart Types", height=700, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 4: Plotly make_subplots ──
    if step_check(4, "Advanced: secondary y-axis", PAGE):
        st.markdown("#### 📐 Secondary Y-Axis")
        lib = library_selector(f"{PAGE}_4")

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        revenue = [120, 150, 130, 170, 160, 190]
        margin = [25, 30, 22, 35, 28, 32]

        if lib in ("Matplotlib", "Seaborn"):
            show_code("""
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()    # create second y-axis
ax1.bar(months, revenue, color="#667eea")
ax2.plot(months, margin, 'o-', color="#EF553B")
""")
            import matplotlib.pyplot as plt
            fig, ax1 = plt.subplots(figsize=(9, 5))
            ax2 = ax1.twinx()
            ax1.bar(months, revenue, color=PALETTE[0], alpha=0.7, label="Revenue ($K)")
            ax2.plot(months, margin, "o-", color="#EF553B", linewidth=2,
                     markersize=8, label="Margin (%)")
            ax1.set_ylabel("Revenue ($K)", color=PALETTE[0])
            ax2.set_ylabel("Margin (%)", color="#EF553B")
            ax1.set_title("Revenue & Margin", fontweight="bold")
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
            plt.tight_layout(); st.pyplot(fig)
        else:
            from plotly.subplots import make_subplots
            import plotly.graph_objects as go
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=months, y=revenue, name="Revenue ($K)",
                                  marker_color=PALETTE[0], opacity=0.7),
                          secondary_y=False)
            fig.add_trace(go.Scatter(x=months, y=margin, name="Margin (%)",
                                      mode="lines+markers",
                                      line=dict(color="#EF553B", width=2)),
                          secondary_y=True)
            fig.update_yaxes(title_text="Revenue ($K)", secondary_y=False)
            fig.update_yaxes(title_text="Margin (%)", secondary_y=True)
            fig.update_layout(title_text="Revenue & Margin")
            st.plotly_chart(fig, use_container_width=True)


render()
