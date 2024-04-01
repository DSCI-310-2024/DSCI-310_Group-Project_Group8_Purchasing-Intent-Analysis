all: data/cleaned_features.csv \
	data/cleaned_targets.csv \
	data/x_train.csv \
	data/x_test.csv \
	data/y_train.csv \
	data/y_test.csv \
	data/preprocessed_train_data.csv \
	data/preprocessed_test_data.csv \
	results/model_comparison_results.csv \
	results/feature_importances.csv \
	results/random_forest_metrics.csv \
	results/random_forest_confusion_matrix.png \
	img/figure_browser_distribution.png \
	img/figure_correlation_matrix.png \
	img/figure_month_distribution.png \
	img/figure_region_distribution.png \
	img/figure_revenue_class_distribution.png \
	img/figure_traffic_type_distribution.png \
	img/figure_visitor_type_distribution.png \
	img/figure_weekend_distribution.png \
	reports/shopper_intention_analysis_report.html \
	reports/shopper_intention_analysis_report.pdf

# Read raw data
data/raw_features.csv data/raw_targets.csv:
	python src/read_data.py 468 data/raw_features.csv data/raw_targets.csv

# Clean data
data/cleaned_features.csv data/cleaned_targets.csv: data/raw_features.csv data/raw_targets.csv
	python src/cleaning.py data/raw_features.csv data/raw_targets.csv data/cleaned_features.csv data/cleaned_targets.csv

# Split data
data/x_train.csv data/x_test.csv data/y_train.csv data/y_test.csv: data/cleaned_features.csv data/cleaned_targets.csv
	python src/data_split.py data/cleaned_features.csv data/cleaned_targets.csv data/x_train.csv data/x_test.csv data/y_train.csv data/y_test.csv

# Preprocess data
data/preprocessed_train_data.csv data/preprocessed_test_data.csv: data/x_train.csv data/x_test.csv data/y_train.csv data/y_test.csv
	python src/preprocessing.py data/x_train.csv data/x_test.csv data/y_train.csv data/y_test.csv data/preprocessed_train_data.csv data/preprocessed_test_data.csv

# Perform analysis
results/model_comparison_results.csv results/feature_importances.csv results/random_forest_metrics.csv results/random_forest_confusion_matrix.png: data/preprocessed_train_data.csv data/preprocessed_test_data.csv
	python src/analysis.py data/preprocessed_train_data.csv data/preprocessed_test_data.csv results

# Generate EDA figures
img/figure_browser_distribution.png img/figure_correlation_matrix.png img/figure_month_distribution.png img/figure_region_distribution.png img/figure_revenue_class_distribution.png img/figure_traffic_type_distribution.png img/figure_visitor_type_distribution.png img/figure_weekend_distribution.png:
	mkdir -p img
	python src/eda_figures.py data/cleaned_features.csv data/cleaned_targets.csv figure

# Render Quarto reports
reports/shopper_intention_analysis_report.html reports/shopper_intention_analysis_report.pdf: src/analysis.py
	quarto render reports/shopper_intention_analysis_report.qmd --to html
	quarto render reports/shopper_intention_analysis_report.qmd --to pdf

clean-all:
	rm -f data/*.csv
	rm -f results/*.csv
	rm -f results/*.png
	rm -f img/*.png
	rm -f reports/*.html
	rm -f reports/*.pdf



# # Makefile

# # This driver script completes the analysis and creates figures 
# # online shopper intent data using machine learning algorithms

# # example usage:
# # make all

# # get analysis outputs
# all: figs \
# 	results/model_comparison_results.csv results/random_forest_confusion_matrix.png \
# 	results/figure/correlation_matrix.png \
# 	reports/shopper_intention_analysis_report.html \
# 	reports/shopper_intention_analysis_report.pdf


# dats: results/output.dat \


# results/model_comparison_results.csv results/random_forest_confusion_matrix.png: src/analysis.py data/preprocessed_train_data.csv data/preprocessed_test_data.csv
# 	python src/analysis.py \
# 		--preprocessed_train_data=data/preprocessed_train_data.csv \
# 		--preprocessed_test_data=data/preprocessed_test_data.csv \
# 		--output_path=results

# # get plot figures
# figs : img/eda_revenue_class_distribution.png \
#        img/eda_month_distribution.png \
#        img/eda_browser_distribution.png \
#        img/eda_region_distribution.png \
#        img/eda_traffic_type_distribution.png \
#        img/eda_visitor_type_distribution.png \
#        img/eda_weekend_distribution.png \
#        img/eda_correlation_matrix.png

# img/eda_revenue_class_distribution.png \
# img/eda_month_distribution.png \
# img/eda_browser_distribution.png \
# img/eda_region_distribution.png \
# img/eda_traffic_type_distribution.png \
# img/eda_visitor_type_distribution.png \
# img/eda_weekend_distribution.png \
# img/eda_correlation_matrix.png \
# results/figure/correlation_matrix.png : src/eda_figures.py data/cleaned_online_shoppers_intention.csv
# 	# python src/eda_figures.py \
# 	# 	--cleaned_data_file=data/cleaned_online_shoppers_intention.csv \
# 	# 	--figure_prefix=results/figure
# 	python src/eda_figures.py \
# 		data/cleaned_online_shoppers_intention.csv \
# 		results/figure





# # write the report
# reports/shopper_intention_analysis_report.html : results reports/shopper_intention_analysis_report.qmd 
# 	quarto render reports/shopper_intention_analysis_report.qmd --to html

# reports/shopper_intention_analysis_report.pdf: results reports/shopper_intention_analysis_report.qmd
# 	quarto render reports/shopper_intention_analysis_report.qmd --to pdf


# #### 
# clean-dats :
# 	rm -f results/output.dat \ 


# ####
# clean-figs:
# 	rm -f img/*.png
# 	rm -f results/figure/*.png
# 	# rm -f results/figure/output.png \ 

# ####
# clean-all : clean-dats \
# 	clean-figs
# 	rm -f report/count_report.html
# 	rm -rf report/count_report_files