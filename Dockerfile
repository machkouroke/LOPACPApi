# Set base image (host OS)
FROM python:3.10-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./requirements.txt .

# Install any dependencies
RUN apk update && apk add build-base python3-dev \
    && pip wheel -r requirements.txt  \
    && apk add ffmpeg libsm6 libxext6

# Copy the content of the local src directory to the working directory
COPY . .


EXPOSE 5000
# Specify the command to run on container start
CMD gunicorn wsgi:app