FROM navikey/raspbian-buster
EXPOSE 8000

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        python3-pip \
        libatlas-base-dev \
        golang-go \
        build-essential \
        pkg-config \
        libzmq5-dev \
        supervisor \
        git

# Create the folders for the application
RUN mkdir -p /var/log/supervisor \
    && mkdir -p /src/zmq_proxy/static \
    && mkdir -p /src/zmq_proxy/Tests \
    && mkdir -p /src/zmq_proxy/Tests/TestData

WORKDIR /src/zmq_proxy

# Build the golang component
COPY main.go /src/zmq_proxy
COPY static /src/zmq_proxy/static

RUN go get -x -v github.com/pebbe/zmq4 \
    && go get -x -v github.com/gorilla/websocket \
    && go build -x -v

# Install the Python dependencies
COPY requirements.txt /src/zmq_proxy
RUN pip3 install \
        --extra-index-url=https://www.piwheels.org/simple \
        -r /src/zmq_proxy/requirements.txt

# Copy the Python application files
COPY *.py /src/zmq_proxy/
COPY Tests/TestData/20200609T2358Z_patrickData.txt \
     /src/zmq_proxy/Tests/TestData

# Setup the services
COPY services.conf /etc/supervisor/conf.d/services.conf
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
