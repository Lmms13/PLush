# Use Ubuntu 20.04 LTS as the base image
FROM ubuntu:20.04

# Avoid timezone interactive dialog
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    clang \
    llvm \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . /app

# Set the working directory in the container to /app
WORKDIR /app

# Install PLY Python library
RUN pip3 install ply

# Convert any Windows-style line endings in plush.sh to Unix-style line endings
RUN dos2unix plush.sh