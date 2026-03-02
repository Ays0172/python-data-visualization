@echo off
copy /Y "pages\01_getting_started.py" "sections\01_getting_started.py"
copy /Y "pages\02_line_charts.py" "sections\02_line_charts.py"
copy /Y "pages\03_bar_charts.py" "sections\03_bar_charts.py"
copy /Y "pages\04_scatter_plots.py" "sections\04_scatter_plots.py"
copy /Y "pages\05_statistical_plots.py" "sections\05_statistical_plots.py"
copy /Y "pages\06_area_and_fill.py" "sections\06_area_and_fill.py"
copy /Y "pages\07_pie_and_donut.py" "sections\07_pie_and_donut.py"
copy /Y "pages\08_categorical_plots.py" "sections\08_categorical_plots.py"
copy /Y "pages\09_joint_pair_plots.py" "sections\09_joint_pair_plots.py"
copy /Y "pages\10_subplots_layouts.py" "sections\10_subplots_layouts.py"
copy /Y "pages\11_styling_aesthetics.py" "sections\11_styling_aesthetics.py"
copy /Y "pages\12_3d_plots.py" "sections\12_3d_plots.py"
copy /Y "pages\13_advanced.py" "sections\13_advanced.py"
echo Copied all 13 files
rmdir /S /Q "pages"
echo Deleted pages directory
echo DONE
