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
COPY /device .
COPY /psica ./psica


RUN mkdir -p ./TestingResultsSmartphone

CMD ["python3", "./test.py"]
