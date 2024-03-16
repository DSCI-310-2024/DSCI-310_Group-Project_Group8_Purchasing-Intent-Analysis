# Makefile

# This driver script completes the analysis and creates figures 
# online shopper intent data using machine learning algorithms
# This script takes no arguments.

# example usage:
# make all

# run entire analysis
all: report/shopper_intent_report.html


dats: results/output.dat \


results/isles.dat : scripts/wordcount.py data/isles.txt
	python scripts/wordcount.py \
		--input_file=data/isles.txt \
		--output_file=results/output.dat


# plot
figs : results/figure/isles.png \


results/figure/isles.png : scripts/plotcount.py results/isles.dat
	python scripts/plotcount.py \
		--input_file=results/isles.dat \
		--output_file=results/figure/isles.png


# write the report
report/count_report.html : report/count_report.qmd figs
	quarto render report/quarto_filename.qmd

clean-dats :
	rm -f results/isles.dat \

clean-figs :
	rm -f results/figure/isles.png \


clean-all : clean-dats \
	clean-figs
	rm -f report/count_report.html
	rm -rf report/count_report_files