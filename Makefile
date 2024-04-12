# Makefile

# Main target
# all: reports/shopper_intention_analysis_report.html
all:data/online_shoppers_intention.csv \
	data/cleaned/cleaned_features.csv data/cleaned/cleaned_targets.csv \
	data/model-test-train/x_train.csv data/model-test-train/x_test.csv data/model-test-train/y_train.csv data/model-test-train/y_test.csv \
	data/preprocessed/preprocessed_train_data.csv data/preprocessed/preprocessed_test_data.csv \
	eda_figures \
	results/model_comparison_results.csv results/random_forest_confusion_matrix.png\
	reports/shopper_intention_analysis_report.html

# read data
DATASET_ID = 468
data/online_shoppers_intention.csv: src/read_data.py
	python src/read_data.py $(DATASET_ID) data/raw/raw_features.csv data/raw/raw_targets.csv


# clean data
data/cleaned/cleaned_features.csv data/cleaned/cleaned_targets.csv: src/cleaning.py data/raw/raw_features.csv data/raw/raw_targets.csv
	python src/cleaning.py data/raw/raw_features.csv data/raw/raw_targets.csv data/cleaned/cleaned_features.csv data/cleaned/cleaned_targets.csv

# data_split
data/model-test-train/x_train.csv data/model-test-train/x_test.csv data/model-test-train/y_train.csv data/model-test-train/y_test.csv: data/cleaned/cleaned_features.csv data/cleaned/cleaned_targets.csv
	python src/data_split.py data/cleaned/cleaned_features.csv data/cleaned/cleaned_targets.csv data/model-test-train/x_train.csv data/model-test-train/x_test.csv data/model-test-train/y_train.csv data/model-test-train/y_test.csv

# pre-process data
data/preprocessed/preprocessed_train_data.csv data/preprocessed/preprocessed_test_data.csv: data/model-test-train/x_train.csv data/model-test-train/x_test.csv data/model-test-train/y_train.csv data/model-test-train/y_test.csv
	python src/preprocessing.py data/model-test-train/x_train.csv data/model-test-train/x_test.csv data/model-test-train/y_train.csv data/model-test-train/y_test.csv data/preprocessed/preprocessed_train_data.csv data/preprocessed/preprocessed_test_data.csv
    
# EDA figures
.PHONY: eda_figures

eda_figures:img/eda_revenue_class_distribution.png \
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
img/eda_correlation_matrix.png: data/cleaned/cleaned_features.csv data/cleaned/cleaned_targets.csv
	python src/eda_figures.py data/cleaned/cleaned_features.csv data/cleaned/cleaned_targets.csv img/eda_

# analysis
results/model_comparison_results.csv results/random_forest_confusion_matrix.png: data/preprocessed/preprocessed_train_data.csv data/preprocessed/preprocessed_test_data.csv
	python src/analysis.py data/preprocessed/preprocessed_train_data.csv data/preprocessed/preprocessed_test_data.csv results

# write the report
reports/shopper_intention_analysis_report.html : results reports/shopper_intention_analysis_report.qmd 
	quarto render reports/shopper_intention_analysis_report.qmd --to html

.PHONY: clean-figs clean-all
clean-figs:
	rm -f img/eda_*.png

clean-all: clean-figs
	rm -f data/checkpoints/*.csv data/cleaned/*.csv data/model-test-train/*.csv data/preprocessed/*.csv data/raw/*.csv data/test-data/*.csv results/*.csv results/*.png reports/*.html