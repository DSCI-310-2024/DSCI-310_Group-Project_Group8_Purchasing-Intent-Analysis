# Makefile

# This driver script completes the analysis and creates figures 
# online shopper intent data using machine learning algorithms

# example usage:
# make all

# get analysis outputs
all: report/shopper_intent_report.html


dats: results/output.dat \


results/model_comparison_results.csv results/random_forest_confusion_matrix.png: scripts/analysis.py data/processed_train_data.csv data/processed_test_data.csv
	python scripts/analysis.py \
		--processed_train_data=data/processed_train_data.csv \
		--processed_test_data=data/processed_test_data.csv \
		--output_path=results

# get plot figures
figs : results/figure/revenue_class_distribution.png \
       results/figure/month_distribution.png \
       results/figure/browser_distribution.png \
       results/figure/region_distribution.png \
       results/figure/traffic_type_distribution.png \
       results/figure/visitor_type_distribution.png \
       results/figure/weekend_distribution.png \
       results/figure/correlation_matrix.png

results/figure/revenue_class_distribution.png \
results/figure/month_distribution.png \
results/figure/browser_distribution.png \
results/figure/region_distribution.png \
results/figure/traffic_type_distribution.png \
results/figure/visitor_type_distribution.png \
results/figure/weekend_distribution.png \
results/figure/correlation_matrix.png : scripts/eda_figures.py data/cleaned_data.csv
	python scripts/eda_figures.py \
		--cleaned_data_file=data/cleaned_data.csv \
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