FROM ubuntu:19.04

# Gregor's version

RUN apt-get -y update 
RUN apt-get -y upgrade 
RUN apt-get -y --no-install-recommends install \
    build-essential \
    git \
    curl \
    wget \
    sudo \
    net-tools \
    gnupg
RUN apt-get -y install \
    python3 \
    python3-pip
RUN rm -rf /var/lib/apt/lists/* 
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
    
RUN pip install cloudmesh-installer

RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list

RUN apt-get -y update 

RUN apt-get install -y mongodb-org-shell

# RUN echo "mongodb-org hold" | sudo dpkg --set-selections
# RUN echo "mongodb-org-server hold" | sudo dpkg --set-selections
# RUN echo "mongodb-org-shell hold" | sudo dpkg --set-selections
# RUN echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
# RUN echo "mongodb-org-tools hold" | sudo dpkg --set-selections

RUN mkdir cm
WORKDIR cm
