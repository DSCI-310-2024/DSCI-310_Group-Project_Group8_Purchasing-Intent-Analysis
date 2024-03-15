FROM continuumio/anaconda3:latest

RUN conda install --yes \
    conda=23.11.0 \
    python=3.9 \
    pandas=2.2.1 \
    jupyterlab=4.0.10 \
    numpy=1.26.4 \
    scikit-learn=1.4.0 \
    matplotlib=3.8.2 \
    seaborn=0.13.2 \
    shap=0.39.0 \
    click=8.1.7 
    