# Makefile

# This driver script completes the analysis and creates figures 
# online shopper intent data using machine learning algorithms

# example usage:
# make all

# get analysis outputs
all: figs \
	reports/shopper_intention_analysis_report.html \
	reports/shopper_intention_analysis_report.pdf


dats: results/output.dat \


results/model_comparison_results.csv results/random_forest_confusion_matrix.png: src/analysis.py data/processed_train.csv data/processed_test.csv
	python src/analysis.py \
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
img/eda_correlation_matrix.png \
results/figure/correlation_matrix.png : src/eda_figures.py data/cleaned_online_shoppers_intention.csv
	# python src/eda_figures.py \
	# 	--cleaned_data_file=data/cleaned_online_shoppers_intention.csv \
	# 	--figure_prefix=results/figure
	python src/eda_figures.py \
		data/cleaned_online_shoppers_intention.csv \
		results/figure




### From here I think we'll need the quarto file
# write the report
reports/shopper_intention_analysis_report.html : results reports/shopper_intention_analysis_report.qmd 
	quarto render reports/shopper_intention_analysis_report.qmd --to html

reports/shopper_intention_analysis_report.pdf: results reports/shopper_intention_analysis_report.qmd
	quarto render reports/shopper_intention_analysis_report.qmd --to pdf


#### 
clean-dats :
	rm -f results/output.dat \ 


####
clean-figs:
	rm -f img/*.png
	rm -f results/figure/*.png
	# rm -f results/figure/output.png \ 

####
clean-all : clean-dats \
	clean-figs
	rm -f report/count_report.html
	rm -rf report/count_report_files