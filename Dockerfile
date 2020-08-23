# Use the official image as a parent image
FROM python:3.7.8-alpine

# Set the working directory
WORKDIR /

# Install gcc
RUN apk update && apk add --no-cache gcc linux-headers libc-dev musl-dev

# Copy all
ADD python/. ./

# Install dependencies
RUN apk update && pip install -r requirements.txt


# Listening on https
EXPOSE 60000

# Run the specified command within the container.
#CMD [ "sleep", "600"]
CMD [ "python","superwatt.py","--debug","superwatt.json" ]

