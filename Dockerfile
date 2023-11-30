FROM python:3.12.0-slim-bullseye AS base

ENV PYROOT /usr/local/lib/python3.12


FROM base AS builder

RUN pip install pipenv && \
    apt-get update -y && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile* /home/src/

WORKDIR /home/src

RUN PIP_IGNORE_INSTALLED=1 pipenv install --system --deploy

FROM base

COPY --from=builder $PYROOT/site-packages $PYROOT/site-packages
COPY run.py /bin

CMD ["run.py"]
