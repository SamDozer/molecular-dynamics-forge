# mdforge -- reproducible container image.
# Build:  docker build -t mdforge .
# Run:    docker run --rm -v /data/sim:/sim mdforge analyze --input /sim --output /sim/results
FROM mambaorg/micromamba:1.5-jammy

WORKDIR /app
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /app/environment.yml
RUN micromamba install -y -n base -f /app/environment.yml && \
    micromamba clean --all --yes

COPY --chown=$MAMBA_USER:$MAMBA_USER . /app
ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN pip install --no-deps -e .

ENTRYPOINT ["mdforge"]
CMD ["--help"]
