ARG IMAGE_PYTHON_VER=3.10.15
FROM python:${IMAGE_PYTHON_VER} AS main

ARG WORKDIR=/app

RUN --mount=type=cache,target=/var/lib/apt,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update \
    && apt-get install -y \
    git

# Install pip packages
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -U pip \
    && pip install -r requirements.txt

RUN git config --global --add safe.directory /var/git

WORKDIR ${WORKDIR}
