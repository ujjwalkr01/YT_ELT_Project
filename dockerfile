ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.10

FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

ENV AIRFLOW_HOME=/opt/airflow

COPY requirements.txt /

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt





# COPY → copy files into Docker image

# RUN → execute a command while building image

# pip install → install Python packages

# -r requirements.txt → install packages listed in requirements.txt

# --no-cache-dir → don't retain pip's package cache
