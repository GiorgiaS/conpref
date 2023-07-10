# To run docker:
# 1. build the image: 
#    $ docker build -t device-image .
#    where "device-example" is a name that you choose
#    If there is the error: "permission denied", run:
#    $ sudo chmod 666 /var/run/docker.sock
# 2. Start the application container:
#    $ docker run -dp 8080:8080 --network host --name device --cpus 8 -m 8g -v $(pwd)/TestingResultsSmartphone:/src/device/TestingResultsSmartphone device-image
# 3. To logs stats:
#    $ docker stats >> ./TestingStatsLogs/realistic.logs
#    $ docker stats >> ./TestingStatsLogs/synthetic.logs
#
# 4. To access the docker container during the execution:
#    $ docker exec -it device bash



# For more information, please refer to https://aka.ms/vscode-docker-python
FROM ubuntu:20.04

EXPOSE 8080

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/

# Install java, and pip
RUN apt-get update -y 
# RUN apt-get install -y apt-utils 
RUN apt-get install -y software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa 
RUN apt-get install default-jdk -y 
RUN apt-get install python3-pip -y 
RUN export JAVA_HOME 
RUN apt-get clean 
RUN rm -rf /var/lib/apt/lists/*


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt


WORKDIR /src/device
# Takes the files in the first parameter to copy into the image at the location specified in the second parameter
COPY /device .
COPY /psica ./psica

# create directory for storing results
RUN mkdir -p ./TestingResultsSmartphone

CMD ["python3", "./test.py"]
