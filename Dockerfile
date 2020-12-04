from pygame

RUN apt-get update && apt-get -y install --no-install-recommends \
    less \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

WORKDIR /magicband-reader
