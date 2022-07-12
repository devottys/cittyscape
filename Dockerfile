# Build from within the directory: docker build -t asciitty .
# Run: docker run -it --rm asciitty

FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install wcwidth

ENV HOME /home/viewuser
RUN useradd --create-home --home-dir $HOME viewuser \
    && chown -R viewuser:viewuser $HOME


USER viewuser
WORKDIR $HOME

ENV TERM="xterm-256color"
COPY . ./
ENV PYTHONPATH=.
CMD python3 -m asciitty
