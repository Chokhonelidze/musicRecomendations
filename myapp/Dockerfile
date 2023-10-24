FROM python:3.9 as base 

RUN pip install pipenv

RUN pip install psycopg2-binary

ENV PROJECT_DIR /usr/local/src/webapp
ENV SRC_DIR ${PROJECT_DIR}/src

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/

WORKDIR ${PROJECT_DIR}

ENV PYTHONUNBUFFERED=1

FROM base as dev

RUN pipenv install --system --dev

COPY  . ${SRC_DIR}/

WORKDIR ${SRC_DIR}

EXPOSE 5000

CMD ["flask","--debug run,"-h", "0.0.0.0"]




