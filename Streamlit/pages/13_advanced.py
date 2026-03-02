"""
Page 13 — Advanced Topics
Date/time axes, live data simulation, custom dataset explorer, export.
"""
import streamlit as st
import numpy as np
import pandas as pd
import datetime
import io
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, get_active_df, numeric_cols, categorical_cols, inject_custom_css)

st.set_page_config(page_title="Advanced Topics | DataViz", page_icon="⚙️", layout="wide")
inject_custom_css()

PAGE = "advanced"
PALETTE = ["#667eea", "#764ba2", "#f093fb", "#fda085", "#a18cd1"]


def render():
    section_header("⚙️", "Advanced Topics")
    st.markdown("Date axes, live data, dataset exploration, and chart export.")

    # ── Step 1: Date/time axes ──
    if step_check(1, "Date & time axis formatting", PAGE):
        st.markdown("#### 📅 Date & Time Axis Formatting")
        lib = library_selector(f"{PAGE}_1")

        dates = pd.date_range("2024-01-01", periods=90, freq="D")
        np.random.seed(99)
        values = np.cumsum(np.random.randn(90)) + 100

        show_code("""
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
fig.autofmt_xdate()
""")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(dates, values, color=PALETTE[0], linewidth=2)
            ax.fill_between(dates, values, alpha=0.12, color=PALETTE[0])
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
            fig.autofmt_xdate()
            ax.set_title("Date-Formatted X-Axis", fontweight="bold")
            ax.set_ylabel("Value")
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            import seaborn as sns, matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(x=dates, y=values, color=PALETTE[0], ax=ax)
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
            fig.autofmt_xdate()
            ax.set_title("Date-Formatted X-Axis", fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.express as px
            fig = px.line(x=dates, y=values, title="Date-Formatted X-Axis",
                          labels={"x": "Date", "y": "Value"})
            fig.update_traces(line_color=PALETTE[0], fill="tozeroy",
                              fillcolor="rgba(102,126,234,0.1)")
            fig.update_xaxes(dtick="M1", tickformat="%b %Y")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 2: Live data simulation ──
    if step_check(2, "Live data simulation", PAGE):
        st.markdown("#### 📡 Live Data Simulation")

        info_card("Simulated Live Feed",
                  "Click the button to simulate a real-time stock ticker. "
                  "Each click generates a new batch of random-walk data.")

        lib = library_selector(f"{PAGE}_2")

        if st.button("🔄 Generate New Data", key=f"{PAGE}_live_btn"):
            st.session_state[f"{PAGE}_live_seed"] = np.random.randint(0, 10000)

        seed = st.session_state.get(f"{PAGE}_live_seed", 42)
        np.random.seed(seed)

        n_points = st.slider("Number of ticks", 50, 500, 200, key=f"{PAGE}_live_n")
        price = 100 + np.cumsum(np.random.randn(n_points) * 0.5)
        timestamps = pd.date_range("2024-01-01 09:30", periods=n_points, freq="1min")

        show_code(f"""
# Simulated live data (seed={seed})
price = 100 + np.cumsum(np.random.randn({n_points}) * 0.5)
""")

        if lib == "Matplotlib":
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 4))
            color_up = "#00cc96"; color_dn = "#EF553B"
            ax.plot(timestamps, price, color=PALETTE[0], linewidth=1.5)
            ax.fill_between(timestamps, price, price[0],
                            where=price >= price[0], color=color_up, alpha=0.15)
            ax.fill_between(timestamps, price, price[0],
                            where=price < price[0], color=color_dn, alpha=0.15)
            ax.axhline(price[0], color="gray", linestyle="--", linewidth=0.8)
            ax.set_title(f"Live Ticker (seed={seed})", fontweight="bold")
            ax.tick_params(axis="x", rotation=30)
            plt.tight_layout(); st.pyplot(fig)
        elif lib == "Seaborn":
            import seaborn as sns, matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(x=timestamps, y=price, color=PALETTE[0], ax=ax)
            ax.axhline(price[0], color="gray", linestyle="--", linewidth=0.8)
            ax.set_title(f"Live Ticker (seed={seed})", fontweight="bold")
            ax.tick_params(axis="x", rotation=30)
            plt.tight_layout(); st.pyplot(fig)
        else:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=timestamps, y=price, mode="lines",
                                      line=dict(color=PALETTE[0], width=1.5),
                                      fill="tozeroy",
                                      fillcolor="rgba(102,126,234,0.08)"))
            fig.add_hline(y=price[0], line_dash="dash", line_color="gray")
            fig.update_layout(title=f"Live Ticker (seed={seed})",
                              xaxis_title="Time", yaxis_title="Price")
            st.plotly_chart(fig, use_container_width=True)

        # Key stats
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Current", f"${price[-1]:.2f}",
                  f"{price[-1] - price[0]:+.2f}")
        c2.metric("High", f"${price.max():.2f}")
        c3.metric("Low", f"${price.min():.2f}")
        c4.metric("Volatility", f"{price.std():.2f}")
        st.markdown("---")

    # ── Step 3: Custom dataset explorer ──
    if step_check(3, "Custom dataset explorer", PAGE):
        st.markdown("#### 🔍 Dataset Explorer")

        df = get_active_df("Tips")

        info_card("Explore Any Dataset",
                  "View summary statistics, column distributions, and auto-generated charts for any loaded dataset.")

        # Summary
        st.markdown("##### 📋 Dataset Overview")
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", f"{len(df):,}")
        c2.metric("Columns", len(df.columns))
        c3.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

        with st.expander("📊 Data Preview", expanded=True):
            st.dataframe(df.head(20), use_container_width=True)

        with st.expander("📈 Summary Statistics"):
            st.dataframe(df.describe(), use_container_width=True)

        # Auto-chart
        st.markdown("##### 🤖 Auto-Generated Charts")
        nc = numeric_cols(df)
        cc = categorical_cols(df)

        if nc:
            lib = library_selector(f"{PAGE}_3")
            chart_col = st.selectbox("Column to visualize", nc, key=f"{PAGE}_3_col")

            tab1, tab2 = st.tabs(["Distribution", "Box Plot"])
            with tab1:
                if lib == "Matplotlib":
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.hist(df[chart_col].dropna(), bins=30, color=PALETTE[0],
                            edgecolor="white", alpha=0.8)
                    ax.set_title(f"Distribution of {chart_col}", fontweight="bold")
                    ax.set_xlabel(chart_col); ax.set_ylabel("Frequency")
                    plt.tight_layout(); st.pyplot(fig)
                elif lib == "Seaborn":
                    import seaborn as sns, matplotlib.pyplot as plt
                    fig, ax = plt.subplots(figsize=(8, 4))
                    sns.histplot(df[chart_col].dropna(), bins=30, kde=True,
                                color=PALETTE[0], ax=ax)
                    ax.set_title(f"Distribution of {chart_col}", fontweight="bold")
                    plt.tight_layout(); st.pyplot(fig)
                else:
                    import plotly.express as px
                    fig = px.histogram(df, x=chart_col, nbins=30,
                                       color_discrete_sequence=[PALETTE[0]],
                                       title=f"Distribution of {chart_col}",
                                       marginal="box")
                    st.plotly_chart(fig, use_container_width=True)
            with tab2:
                if cc:
                    grp = st.selectbox("Group by", cc, key=f"{PAGE}_3_grp")
                else:
                    grp = None
                if lib == "Matplotlib":
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots(figsize=(8, 4))
                    if grp:
                        groups = [g[chart_col].dropna().values for _, g in df.groupby(grp)]
                        bp = ax.boxplot(groups, labels=df[grp].unique(), patch_artist=True)
                        for patch, c in zip(bp["boxes"], PALETTE * 5):
                            patch.set_facecolor(c); patch.set_alpha(0.6)
                    else:
                        ax.boxplot(df[chart_col].dropna(), patch_artist=True)
                    ax.set_title(f"Box Plot of {chart_col}", fontweight="bold")
                    plt.tight_layout(); st.pyplot(fig)
                elif lib == "Seaborn":
                    import seaborn as sns, matplotlib.pyplot as plt
                    fig, ax = plt.subplots(figsize=(8, 4))
                    sns.boxplot(data=df, x=grp, y=chart_col, palette=PALETTE, ax=ax)
                    ax.set_title(f"Box Plot of {chart_col}", fontweight="bold")
                    plt.tight_layout(); st.pyplot(fig)
                else:
                    import plotly.express as px
                    fig = px.box(df, x=grp, y=chart_col, color=grp,
                                 color_discrete_sequence=PALETTE,
                                 title=f"Box Plot of {chart_col}")
                    st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # ── Step 4: Exporting charts ──
    if step_check(4, "Exporting charts", PAGE):
        st.markdown("#### 💾 Exporting Charts")

        info_card("Export Options",
                  "<b>Matplotlib</b>: fig.savefig('chart.png', dpi=300, bbox_inches='tight')<br/>"
                  "<b>Plotly</b>: fig.write_html('chart.html') or fig.write_image('chart.png')")

        show_code("""
# Matplotlib export
fig.savefig("my_chart.png", dpi=300, bbox_inches="tight",
            facecolor="white", edgecolor="none")
fig.savefig("my_chart.svg")   # Vector format
fig.savefig("my_chart.pdf")   # PDF format

# Plotly export
fig.write_html("my_chart.html")             # Interactive HTML
fig.write_image("my_chart.png", scale=2)    # Requires kaleido
fig.write_json("my_chart.json")             # JSON for later use
""")

        # Demo: generate a chart and let user download it
        st.markdown("##### Try it — download a sample chart:")

        import matplotlib.pyplot as plt
        np.random.seed(7)
        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.arange(1, 11)
        y = np.random.randint(5, 30, 10)
        ax.bar(x, y, color=PALETTE[:10], edgecolor="white")
        ax.set_title("Sample Chart for Export", fontweight="bold")
        ax.set_xlabel("Category"); ax.set_ylabel("Value")
        plt.tight_layout()

        # Convert to PNG bytes for download
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                    facecolor="white", edgecolor="none")
        buf.seek(0)

        st.pyplot(fig)
        st.download_button(
            label="⬇️ Download as PNG",
            data=buf,
            file_name="chart_export.png",
            mime="image/png",
        )


render()
