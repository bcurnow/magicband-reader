FROM python:3.13-slim

ARG USER_ID
ARG GROUP_ID

# Don't attempt to set the user to the root user (uid=0) or group (gid=0)
RUN if [ ${USER_ID:-0} -eq 0 ] || [ ${GROUP_ID:-0} -eq 0 ]; then \
        groupadd magicbandreader \
        && useradd -g magicbandreader magicbandreader \
        ;\
    else \
        groupadd -g ${GROUP_ID} magicbandreader \
        && useradd -l -u ${USER_ID} -g magicbandreader magicbandreader \
        ;\
    fi \
    && install -d -m 0755 -o magicbandreader -g magicbandreader /home/magicbandreader \
    && mkdir -p /etc/sudoers.d \
    && echo "magicbandreader ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/magicbandreader-all-nopasswd

RUN apt-get update && apt-get -y install --no-install-recommends \
    build-essential \
    git \
    less \
    libasound2-dev \
    sudo \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY ./docker-files/home/.* /home/magicbandreader/

COPY ./requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

USER magicbandreader

WORKDIR /magicband-reader
