#!/bin/bash

# Build the Docker image
docker build -t plush56341 .

# Run the Docker container
docker run -it --rm plush56341