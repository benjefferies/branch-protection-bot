FROM python:3.7-slim-stretch AS base

ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT


FROM base AS builder

RUN pip install pipenv==2020.6.2 && \
    apt-get update -y && \
    apt-get install -y git

COPY Pipfile* /home/src/

WORKDIR /home/src

RUN PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --system --deploy --ignore-pipfile

FROM base

COPY --from=builder $PYROOT/lib/ $PYROOT/lib/
COPY run.py /bin

CMD ["run.py"]
