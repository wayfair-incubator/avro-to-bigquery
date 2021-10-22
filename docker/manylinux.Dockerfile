ARG IMAGE=quay.io/pypa/manylinux1_x86_64
FROM ${IMAGE}

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN /opt/python/cp38-cp38/bin/pip install -r requirements.txt -r requirements-test.txt

RUN /opt/python/cp38-cp38/bin/pip install -e .
