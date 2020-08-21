# Use the official image as a parent image
FROM python:3.7.8-alpine

# Set the working directory
WORKDIR /

# Install OpenJDK-8
RUN apk update && apk add --no-cache openjdk8-jre 

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

# Copy all
COPY * ./

# Listening on https
EXPOSE 60000

# Run the specified command within the container.
CMD [ "start.sh"]

