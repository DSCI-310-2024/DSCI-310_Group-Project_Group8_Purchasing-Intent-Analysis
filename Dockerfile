FROM quay.io/jupyter/scipy-notebook:2024-02-24

# Install Python packages using conda
RUN conda install --yes \
    numpy=1.26.4 \
    click=8.1.7 \
    pyYAML=6.0.1 \
    tabulate=0.9.0 \
    click=8.1.7


# Quarto Installation

# Use root to install system-level packages
USER root

# Install system dependencies for Quarto
RUN apt-get update && apt-get install -y \
    make \
    gdebi \ 
    lmodern

# Download and install Quarto
ARG QUARTO_VERSION="1.4.537"
RUN curl -o quarto-linux-amd64.deb -L https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb && \
    gdebi --non-interactive quarto-linux-amd64.deb

# Install ucimlrepo using pip
RUN pip install ucimlrepo

# Switch back to the jovyan user
USER $NB_UID
