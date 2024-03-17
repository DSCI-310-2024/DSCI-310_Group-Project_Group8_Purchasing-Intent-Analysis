# Makefile

# This driver script completes the analysis and creates figures 
# online shopper intent data using machine learning algorithms

# example usage:
# make all

# get analysis outputs
all: report/shopper_intent_report.html


dats: results/output.dat \


results/model_comparison_results.csv results/random_forest_confusion_matrix.png: scripts/analysis.py data/processed_train.csv data/processed_test.csv
	python scripts/analysis.py \
		--processed_train_data=data/processed_train.csv \
		--processed_test_data=data/processed_test.csv \
		--output_path=results

# get plot figures
figs : img/eda_revenue_class_distribution.png \
       img/eda_month_distribution.png \
       img/eda_browser_distribution.png \
       img/eda_region_distribution.png \
       img/eda_traffic_type_distribution.png \
       img/eda_visitor_type_distribution.png \
       img/eda_weekend_distribution.png \
       img/eda_correlation_matrix.png

img/eda_revenue_class_distribution.png \
img/eda_month_distribution.png \
img/eda_browser_distribution.png \
img/eda_region_distribution.png \
img/eda_traffic_type_distribution.png \
img/eda_visitor_type_distribution.png \
img/eda_weekend_distribution.png \
results/figure/correlation_matrix.png : scripts/eda_figures.py data/cleaned_online_shoppers_intention.csv
	python scripts/eda_figures.py \
		--cleaned_data_file=data/cleaned_online_shoppers_intention.csv \
		--figure_prefix=results/figure



### From here I think we'll need the quarto file
# write the report
report/report.html : report/report.qmd figs
	quarto render report/quarto_filename.qmd


#### 
clean-dats :
	rm -f results/output.dat \ 


####
clean-figs :
	rm -f results/figure/output.png \ 

####
clean-all : clean-dats \
	clean-figs
	rm -f report/count_report.html
	rm -rf report/count_report_files