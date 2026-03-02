"""
Page 12 — 3D Plots
3D scatter, surface, line (Plotly-centric with Matplotlib fallback).
"""
import streamlit as st
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, inject_custom_css)

st.set_page_config(page_title="3D Plots | DataViz", page_icon="🧊", layout="wide")
inject_custom_css()

PAGE = "3d_plots"
PALETTE = ["#667eea", "#764ba2", "#f093fb", "#fda085"]


def render():
    section_header("🧊", "3D Plots")
    st.markdown("3D plots add a **depth dimension** — ideal for exploring three-variable relationships.")

    # ── Step 1: 3D Scatter ──
    if step_check(1, "3D scatter plot", PAGE):
        st.markdown("#### ⚡ 3D Scatter Plot")
        lib = library_selector(f"{PAGE}_1", options=["Plotly", "Matplotlib"])

        np.random.seed(42)
        n = 200
        df3 = pd.DataFrame({
            "x": np.random.randn(n),
            "y": np.random.randn(n),
            "z": np.random.randn(n),
            "group": np.random.choice(["A", "B", "C"], n),
        })

        if lib == "Plotly":
            show_code("""
import plotly.express as px
fig = px.scatter_3d(df, x="x", y="y", z="z", color="group",
                    opacity=0.7, title="3D Scatter Plot")
fig.show()
""")
            import plotly.express as px
            fig = px.scatter_3d(df3, x="x", y="y", z="z", color="group",
                                opacity=0.7, color_discrete_sequence=PALETTE,
                                title="3D Scatter Plot")
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        else:
            show_code("""
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c=colors, alpha=0.6)
""")
            import matplotlib.pyplot as plt
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection="3d")
            colors = {"A": PALETTE[0], "B": PALETTE[1], "C": PALETTE[2]}
            for grp in df3["group"].unique():
                sub = df3[df3["group"] == grp]
                ax.scatter(sub["x"], sub["y"], sub["z"], label=grp,
                           color=colors[grp], alpha=0.6, s=30)
            ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
            ax.set_title("3D Scatter Plot", fontweight="bold")
            ax.legend()
            plt.tight_layout(); st.pyplot(fig)

        info_card("💡 Tip", "Plotly 3D plots are interactive — drag to rotate, scroll to zoom!")
        st.markdown("---")

    # ── Step 2: 3D Surface ──
    if step_check(2, "3D surface plot", PAGE):
        st.markdown("#### 🏔️ 3D Surface Plot")
        lib = library_selector(f"{PAGE}_2", options=["Plotly", "Matplotlib"])

        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X**2 + Y**2))

        if lib == "Plotly":
            show_code("""
import plotly.graph_objects as go
fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
fig.update_layout(title='3D Surface', scene=dict(
    xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
""")
            import plotly.graph_objects as go
            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Viridis")])
            fig.update_layout(title="3D Surface — sin(√(x²+y²))", height=600,
                              scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            show_code("""
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
""")
            import matplotlib.pyplot as plt
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111, projection="3d")
            ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.85, edgecolor="none")
            ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
            ax.set_title("3D Surface — sin(√(x²+y²))", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        st.markdown("---")

    # ── Step 3: 3D Line ──
    if step_check(3, "3D line plot", PAGE):
        st.markdown("#### 〰️ 3D Line Plot")
        lib = library_selector(f"{PAGE}_3", options=["Plotly", "Matplotlib"])

        t = np.linspace(0, 10 * np.pi, 500)
        x = np.sin(t)
        y = np.cos(t)
        z = t

        if lib == "Plotly":
            show_code("""
import plotly.graph_objects as go
fig = go.Figure(data=[go.Scatter3d(
    x=np.sin(t), y=np.cos(t), z=t,
    mode='lines', line=dict(color=t, colorscale='Viridis', width=4)
)])
""")
            import plotly.graph_objects as go
            fig = go.Figure(data=[go.Scatter3d(
                x=x, y=y, z=z, mode="lines",
                line=dict(color=z, colorscale="Viridis", width=4)
            )])
            fig.update_layout(title="3D Helix", height=600,
                              scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            import matplotlib.pyplot as plt
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection="3d")
            ax.plot(x, y, z, color=PALETTE[0], linewidth=1.5)
            ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
            ax.set_title("3D Helix", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        st.markdown("---")

    # ── Step 4: Interactive rotation ──
    if step_check(4, "Interactive 3D with controls", PAGE):
        st.markdown("#### 🎮 Interactive 3D with Controls")

        st.markdown("Use the sliders to control the 3D surface function:")
        c1, c2 = st.columns(2)
        freq = c1.slider("Frequency", 0.5, 5.0, 1.0, 0.5, key=f"{PAGE}_freq")
        amp = c2.slider("Amplitude", 0.5, 3.0, 1.0, 0.5, key=f"{PAGE}_amp")

        x = np.linspace(-5, 5, 60)
        y = np.linspace(-5, 5, 60)
        X, Y = np.meshgrid(x, y)
        Z = amp * np.sin(freq * np.sqrt(X**2 + Y**2))

        import plotly.graph_objects as go
        fig = go.Figure(data=[go.Surface(
            z=Z, x=X, y=Y, colorscale="Plasma",
            contours=dict(z=dict(show=True, usecolormap=True,
                                  highlightcolor="limegreen", project_z=True))
        )])
        fig.update_layout(
            title=f"Interactive Surface — amp={amp}, freq={freq}",
            height=600,
            scene=dict(
                xaxis_title="X", yaxis_title="Y", zaxis_title="Z",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.0))
            )
        )
        st.plotly_chart(fig, use_container_width=True)

        show_code(f"""
Z = {amp} * np.sin({freq} * np.sqrt(X**2 + Y**2))
fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Plasma')])
""")


render()
