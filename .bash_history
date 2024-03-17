cd ..
conda install tabulate
cd reports
quarto render shopper_intention_analysis_report.qmd --to html
make clean
make all
cd ..
quarto render reports/shopper_intention_analysis_report.qmd --to html
docker-compose down
