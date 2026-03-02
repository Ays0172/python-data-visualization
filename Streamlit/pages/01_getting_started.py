"""
Page 1 — Getting Started
First chart, imports, library comparison.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (section_header, show_code, step_check, library_selector,
                   info_card, inject_custom_css)

st.set_page_config(page_title="Getting Started | DataViz", page_icon="🚀", layout="wide")
inject_custom_css()

PAGE = "getting_started"


def render():
    section_header("🚀", "Getting Started")

    st.markdown("""
    Welcome to the **first step** of your data visualization journey!
    Here you'll learn how to import the three major Python plotting libraries
    and create your very first chart.
    """)

    # ── Step 1: Imports ──
    if step_check(1, "Import the libraries", PAGE):
        st.markdown("#### 📦 Importing Libraries")
        info_card(
            "Three Libraries, One Goal",
            "Matplotlib is the foundation, Seaborn adds statistical elegance, "
            "and Plotly brings interactivity. All three work beautifully with Pandas DataFrames."
        )
        show_code("""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
import numpy as np
""")
        st.success("✅ Libraries are ready to use!")
        st.markdown("---")

    # ── Step 2: First chart ──
    if step_check(2, "Create your first chart", PAGE):
        st.markdown("#### 📊 Your First Bar Chart")

        lib = library_selector(f"{PAGE}_2")

        data = {"Category": ["A", "B", "C", "D"],
                "Value": [4, 7, 1, 8]}

        if lib == "Matplotlib":
            show_code("""
import matplotlib.pyplot as plt

categories = ["A", "B", "C", "D"]
values = [4, 7, 1, 8]

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(categories, values, color=["#667eea", "#764ba2", "#f093fb", "#fda085"])
ax.set_title("My First Bar Chart", fontsize=14, fontweight="bold")
ax.set_ylabel("Value")
plt.tight_layout()
plt.show()
""")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(data["Category"], data["Value"],
                   color=["#667eea", "#764ba2", "#f093fb", "#fda085"])
            ax.set_title("My First Bar Chart", fontsize=14, fontweight="bold")
            ax.set_ylabel("Value")
            plt.tight_layout()
            st.pyplot(fig)

        elif lib == "Seaborn":
            show_code("""
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({"Category": ["A","B","C","D"], "Value": [4,7,1,8]})
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=df, x="Category", y="Value",
            palette=["#667eea","#764ba2","#f093fb","#fda085"], ax=ax)
ax.set_title("My First Bar Chart", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
""")
            import seaborn as sns
            import pandas as pd
            import matplotlib.pyplot as plt
            df = pd.DataFrame(data)
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(data=df, x="Category", y="Value",
                        palette=["#667eea", "#764ba2", "#f093fb", "#fda085"], ax=ax)
            ax.set_title("My First Bar Chart", fontsize=14, fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig)

        else:  # Plotly
            show_code("""
import plotly.express as px
import pandas as pd

df = pd.DataFrame({"Category": ["A","B","C","D"], "Value": [4,7,1,8]})
fig = px.bar(df, x="Category", y="Value",
             color="Category",
             color_discrete_sequence=["#667eea","#764ba2","#f093fb","#fda085"],
             title="My First Bar Chart")
fig.show()
""")
            import plotly.express as px
            import pandas as pd
            df = pd.DataFrame(data)
            fig = px.bar(df, x="Category", y="Value",
                         color="Category",
                         color_discrete_sequence=["#667eea", "#764ba2",
                                                   "#f093fb", "#fda085"],
                         title="My First Bar Chart")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

    # ── Step 3: Library comparison ──
    if step_check(3, "Compare the three libraries", PAGE):
        st.markdown("#### 🔍 Library Comparison")
        import pandas as pd
        comparison = pd.DataFrame({
            "Feature": ["Interactivity", "Ease of Use", "Statistical Focus",
                        "3D Support", "Web Export", "Customization"],
            "Matplotlib": ["⭐", "⭐⭐⭐", "⭐⭐", "⭐⭐", "⭐", "⭐⭐⭐⭐⭐"],
            "Seaborn": ["⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐", "⭐", "⭐⭐⭐"],
            "Plotly": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐"],
        })
        st.dataframe(comparison, use_container_width=True, hide_index=True)

        info_card(
            "💡 Pro Tip",
            "Use <b>Matplotlib</b> when you need pixel-perfect control, "
            "<b>Seaborn</b> for quick statistical plots, and "
            "<b>Plotly</b> for interactive dashboards."
        )


render()
