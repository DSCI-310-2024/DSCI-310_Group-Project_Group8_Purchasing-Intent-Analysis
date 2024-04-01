cd src
python read_data.py 468 ../data/raw_features.csv ../data/raw_targets.csv
python data_split.py ../data/raw_features.csv ../data/raw_targets.csv ../data/x_train.csv ../data/x_test.csv ../data/y_train.csv ../data/y_test.csv
python cleaning.py ../data/x_train.csv ../data/y_train.csv ../data/cleaned_train_data.csv
python eda_figures.py ../data/cleaned_train_data.csv ../img/figure
python read_data.py 468 ../data/raw_features.csv ../data/raw_targets.csv
python cleaning.py ../data/raw_features.csv ../data/raw_targets.csv ../data/cleaned_features.csv ../data/cleaned_targets.csv
python cleaning.py ../data/raw_features.csv ../data/raw_targets.csv ../data/cleaned_features.csv ../data/cleaned_targets.csv
python cleaning.py ../data/raw_features.csv ../data/raw_targets.csv ../data/cleaned_features.csv ../data/cleaned_targets.csv
python read_data.py 468 ../data/raw_features.csv ../data/raw_targets.csv
python cleaning.py ../data/raw_features.csv ../data/raw_targets.csv ../data/cleaned_features.csv ../data/cleaned_targets.csv
python data_split.py ../data/cleaned_features.csv ../data/cleaned_targets.csv ../data/x_train.csv ../data/x_test.csv ../data/y_train.csv ../data/y_test.csv
python eda.py ../data/cleaned_features.csv ../data/cleaned_targets.csv ../img/figure
python eda_figures.py ../data/cleaned_features.csv ../data/cleaned_targets.csv ../img/figure
python preprocessing.py ../data/x_train.csv ../data/x_test.csv ../data/y_train.csv ../data/y_test.csv ../data/preprocessed_train_data.csv ../data/preprocessed_test_data.csv
python analysis.py ../data/preprocessed_train_data.csv and ../data/preprocessed_test_data.csv ../results
python analysis.py ../data/preprocessed_train_data.csv ../data/preprocessed_test_data.csv ../results
python analysis.py ../data/preprocessed_train_data.csv ../data/preprocessed_test_data.csv ../results
python analysis.py ../data/preprocessed_train_data.csv ../data/preprocessed_test_data.csv ../results
exit
exit
cd tests 
pytest
pytest
pytest
pytest
pytest
pytest
pytest
exit
cd reports
open shopper_intention_analysis_report.html
exit
make clean-all
make all
make clean-all
make all
make clean-all
make all
make clean-all
make all
make clean-all
make all
make clean-all
make all
make clean-all
make all
make clean-all
make all
make clean-all
make clean-all
make clean-all
make all
make clean-all
make clean
make all
cd src
python eda_figures.py ../data/cleaned_features.csv ../data/cleaned_targets.csv ../img/figure
cd ..
make clean-all
make all
make clean-all
make all
make clean-all
make all
make clean-all
make clean-all
make all
exit
