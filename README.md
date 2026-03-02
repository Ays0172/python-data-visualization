# 📊 Python Data Visualization Masterclass & Interactive App

This repository serves two primary purposes:
1. It contains a comprehensive collection of **Jupyter Notebooks** detailing step-by-step implementations from a certification course on Data Visualization in Python.
2. It features a full **Interactive Streamlit Web Application** designed to teach and demonstrate these charting techniques dynamically alongside Python code snippets.

---

## 🚀 1. The Interactive Streamlit App

The `Streamlit/` directory houses an immersive dashboard built to make learning data visualization engaging and intuitive. It allows you to explore, compare, and understand various charting techniques using **Matplotlib**, **Seaborn**, and **Plotly**.

### 🌟 Key Features:
- **Guided Learning Paths**: Click through concepts step-by-step from beginner to advanced.
- **Library Switcher**: See the exact same data visualized across Matplotlib, Seaborn, and Plotly with a single click.
- **Live Code Display**: View the actual Python code generating the visualizations in real-time.
- **Custom Data Support**: Upload your own CSV datasets or choose from built-in sample data (e.g., Tips, Iris, Titanic, Gapminder) to see how charts adapt to different data shapes.

### 🏃‍♂️ Running the Web App locally:
```bash
# Navigate to the Streamlit directory
cd python-data-visualization/Streamlit

# Install required packages
pip install -r requirements.txt

# Launch the Application
streamlit run app.py
```

---

## 📚 2. Comprehensive Jupyter Notebooks (Course Modules)

The core repository is structured into specific folders for the three major plotting libraries. These notebooks cover every step of the data visualization journey, from rendering basic lines to constructing complex 3D surfaces.

### 📉 Matplotlib Mastery (`Matplotlib/`)
The foundational library for Python plotting. The notebooks cover detailed, granular customization:
- **Fundamentals**: Figure sizes (`1figsize.ipynb`), axis scaling (`3axis_scales.ipynb`), and grid setup (`21Setting_up_no_of_rows_columns.ipynb`).
- **Aesthetics**: Label and title styling (`2Label_Styling.ipynb`), custom colors, linestyles, and markers (`4colors_linestyle_marker_linewidth.ipynb`), applying built-in plotting styles (`6plotting_style.ipynb`), and adding grids (`5Addying_grid.ipynb`).
- **Basic Charts**: Connecting data points (`19Connecting_data_points_by_line.ipynb`), scatter plots (`17scatterplot.ipynb`), and stem plots (`15stemplot.ipynb`).
- **Distributions**: Histograms vs. Bar Charts (`10Histograms_v_barCharts.ipynb`) and advanced histogram techniques (`11AdvancedHistograms.ipynb`).
- **Categorical & Composition**: Stacked bar charts (`12Stacked_bar_charts.ipynb`), basic stack/area plots (`14Basic_stack_plot.ipynb`), Box and Whisker plots (`13Box_Whisker_Plots.ipynb`), and pie charts including rotating, legends, and shadows (`9Title_legends_rotating piecharts.ipynb`, `8shadow_edgecolor.ipynb`).
- **Advanced Techniques**: Filling areas between lines (`7filling.ipynb`), handling Python datetime modules (`18python_date_time_module.ipynb`), and processing live, updating data streams (`20live_data.ipynb`).

### 🌊 Seaborn Statistical Plots (`Seaborn/`)
Seaborn builds on Matplotlib to provide beautiful, complex statistical plots with minimal code:
- **Core Aesthetics**: Deep dives into plot aesthetics (`6Plot Aesthetics.ipynb`) and manipulating data mappings with hue, style, and size (`1hue_style_size.ipynb`).
- **Multivariate Analysis**: Combining multiple chart types with subplots (`2subplots.ipynb`), joint plots, and pair plots (`5jointplot_pairplot.ipynb`).
- **Relationships & Categories**: Line plots with statistical estimations (`3linoplts.ipynb`) and advanced categorical plots (strip, swarm, violin, box) (`4catplots.ipynb`).

### 🪄 Plotly Interactive Visualizations (`Plotly/`)
Plotly brings web-based interactivity, hover tools, and 3D capabilities to Python:
- **Getting Started**: Installation and basic setup (`1installation.ipynb`, `first_figure.html`).
- **Interactive 2D**: Exploring various interactive chart types (bar, scatter, pie, etc.) (`2different_charts.ipynb`).
- **3D Visualizations**: Constructing dynamic 3D scatter plots and surface plots (`3_3DPlots.ipynb`).

---

## 🎯 Project Goal

To provide an end-to-end framework for mastering the art of creating **clear, insightful, and professional visualizations** for data analysis and storytelling. Whether you prefer reading through heavily annotated Jupyter notebooks or interacting with a dynamic web application, this repository is designed to elevate your Python DataViz skills.
