from python:3

ARG USER_ID
ARG GROUP_ID
ARG INPUT_GROUP_ID
ARG AUDIO_GROUP_ID

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
    && mkdir -p /etc/sudoers.d  \
    && echo "magicbandreader ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/magicbandreader-all-nopasswd

# Add the input group
RUN groupadd -g ${INPUT_GROUP_ID} input \
    && usermod -a -G input magicbandreader

# Add the audio group
RUN groupadd -g ${AUDIO_GROUP_ID} audio \
    && usermod -a -G audio magicbandreader


RUN apt-get update && apt-get -y install --no-install-recommends \
    less \
    libfreetype6-dev \
    libportmidi-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    sudo \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY ./docker-files/home/.* /home/magicbandreader/

COPY ./requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

USER magicbandreader

WORKDIR /magicband-reader
