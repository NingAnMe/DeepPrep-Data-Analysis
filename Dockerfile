# syntax = docker/dockerfile:1.5
FROM ubuntu:jammy-20240627.1

LABEL authors="anning"

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Etc/UTC

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl bzip2 ca-certificates \
        && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /
RUN curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
ENV MAMBA_ROOT_PREFIX="/opt/conda"
RUN micromamba create -y -n deepprep -c conda-forge python=3.10.14 pip
RUN micromamba shell init -s bash && echo "micromamba activate deepprep" >> $HOME/.bashrc

## Python
RUN micromamba shell init -s bash && \
    echo "micromamba activate deepprep" >> $HOME/.bashrc
ENV PATH="/opt/conda/envs/deepprep/bin:$PATH" \
    CPATH="/opt/conda/envs/deepprep/include:$CPATH" \
    LD_LIBRARY_PATH="/opt/conda/envs/deepprep/lib:$LD_LIBRARY_PATH" \
    UV_USE_IO_URING=0

RUN pip3 install \
    numpy==1.26.4 pandas==2.2.2 nibabel==5.2.1 bids \
    && pip3 cache purge && rm -rf /tmp/* /var/tmp/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgfortran5 \
        && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

## Create a shared $HOME directory
RUN useradd -m -s /bin/bash -G users deepprep
WORKDIR /home/deepprep
ENV HOME="/home/deepprep"

COPY denoise /opt/DeepPrep/denoise
RUN chmod 755 -R /opt/DeepPrep/denoise

RUN find $HOME -type d -exec chmod go=u {} + && \
    find $HOME -type f -exec chmod go=u {} +

## CMD
ENTRYPOINT ["/opt/DeepPrep/denoise/bold_denoise.py"]
