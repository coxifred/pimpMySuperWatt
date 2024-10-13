# Use the official image as a parent image
FROM python:3.9.18-alpine

# Set the working directory
WORKDIR /

# ASSUME ROOT
USER 0

# CREATING PIMP DIR
RUN mkdir /pimpmysuperwatt

# Copy all
COPY . /pimpmysuperwatt

# Install dependencies
RUN apk update && apk add --no-cache gcc linux-headers libc-dev musl-dev bash

# Install grafana
RUN wget https://dl.grafana.com/oss/release/grafana-11.2.2.linux-amd64.tar.gz
RUN tar -zxvf grafana-11.2.2.linux-amd64.tar.gz
COPY ./grafana/conf/defaults.ini /grafana-v11.2.2/conf
RUN rm -rf /grafana-v11.2.2/conf
RUN cp -Rp /pimpmysuperwatt/grafana/conf /grafana-v11.2.2
RUN cp -Rp /pimpmysuperwatt/grafana/plugins /grafana-v11.2.2
RUN mkdir /grafana-v11.2.2/data

# Install influxdb
RUN wget https://download.influxdata.com/influxdb/releases/influxdb-1.8.10-static_linux_amd64.tar.gz
RUN tar xvfz influxdb-1.8.10-static_linux_amd64.tar.gz
RUN cp /pimpmysuperwatt/influxdb/conf/influxdb.conf /influxdb-1.8.10-1/influxdb.conf
RUN mkdir /influxdb-1.8.10-1/data
RUN mkdir /influxdb-1.8.10-1/data/wal
RUN mkdir /influxdb-1.8.10-1/data/meta


# Cleanup tar files
RUN rm influxdb-1.8.10-static_linux_amd64.tar.gz /grafana-11.2.2.linux-amd64.tar.gz

# Creating venv
RUN python3 -m venv /pimpmysuperwatt/venv
RUN bash /pimpmysuperwatt/venv/bin/activate
RUN /pimpmysuperwatt/venv/bin/pip3 install -r /pimpmysuperwatt/requirements.txt 

# Removing herited ENTRYPOINT
ENTRYPOINT []

# Listening on port 60000
EXPOSE 60000
# Listening on port 3000 (grafana)
EXPOSE 3000

# Run the specified command within the container.
CMD [ "/pimpmysuperwatt/start.sh" ]
