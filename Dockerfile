FROM quay.io/jupyter/scipy-notebook:2024-02-24

RUN conda install --yes \
    numpy=1.26.4 \
    click=8.1.7
    