FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu20.04

# Install dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
  default-libmysqlclient-dev \
  default-mysql-server \
  default-mysql-client \
  dumb-init \
  htop \
  sudo \
  git \
  bzip2 \
  libx11-6 \
  locales \
  man \
  nano \
  telnet \
  traceroute \
  zip \
  unzip \
  procps \
  openssh-client \
  vim

ARG DEBIAN_FRONTEND=noninteractive
RUN apt install software-properties-common -y \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get install ffmpeg libsm6 libxext6 -y \
    && apt install --no-install-recommends -y \
    python3.10 python3.10-dev python3.10-venv python3-pip python3-opencv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory
RUN mkdir /app

RUN python3.10 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install torch
RUN pip install --no-cache-dir -U pip && \
  pip install --no-cache-dir torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt

WORKDIR /app

EXPOSE 9876