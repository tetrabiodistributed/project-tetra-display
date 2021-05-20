# Developing with Docker for a Raspberry Pi

## Prerequisites

1. Install Docker on your local computer.

    https://docs.docker.com/engine/install/

2. Install Docker on your Pi.
   
    1. Install Docker
    
        ```
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
       ```

    2. Add your user to the docker group
    
        To be able to use docker on the Pi you will need to add your user to the docker group.
        After adding yourself to the group you will need to log out and back in again.
       
        ```
        sudo usermod -aG docker [username]
        ```

## Building the Docker image

The Docker image can be built on your development PC and run on the Pi. You do not need to build it
on the Pi itself as everything will be cross compiled for ARM.

Build the docker image by running the following. This will take a long time the first time you run it.

```
docker buildx build --platform linux/arm/v6 -t zmq_proxy:latest .
```

After building, you can run the image locally to test by running the following.

```
 docker run -p 8000:8000 zmq_proxy:latest
```

Go to http://localhost:8000 to test it's working.

## Running the Docker image on the Pi

1. Save the Docker image on your development PC.

    ```
    docker save zmq_proxy:latest | gzip > zmq_proxy_latest.tar.gz
    ```

2. Copy the file to your PI using scp or any other method you use to transfer files.

    ```
    scp zmq_proxy_latest.tar.gz pi@raspberrypi:/home/pi
    ```

3. ssh to the Pi, load and run the docker image.

    ```
    ssh pi@raspberrypi
    gunzip -c zmq_proxy_latest.tar.gz | docker load
    docker run -p 8000:8000 -ti zmq_proxy:latest
    ```
