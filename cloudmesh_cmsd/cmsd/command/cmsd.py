#
# This command is python2 and 3 compatible
#

from __future__ import print_function
from cloudmesh_cmsd.cmsd.__version__ import version
from pprint import pprint

try:
    from pathlib import Path
except:
    from pathlib2 import Path

import os
import shutil
import textwrap

from cloudmesh.common.util import writefile
from cloudmesh.configuration.Config import Config
from docopt import docopt
import sys

dockercompose = """
version: '3'
services:
  cloudmesh:
    container_name: cmsd
    build: .
    volumes:
      - .:/code
      - ~/.cloudmesh:/root/.cloudmesh
      - ~/.ssh/id_rsa.pub:/root/.ssh/id_rsa.pub
    depends_on:
      - mongo
    links:
      - mongo
  mongo:
    image: mongo:latest
    container_name: mongodb
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: <your-username>
      MONGO_INITDB_ROOT_PASSWORD: <your-password>
      MONGO_INITDB_DATABASE: cloudmesh
    ports:
      - "27017-27019:27017-27019"
    volumes:
      - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
"""

dockerfile = """
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

#
# keep the version fixed
#
RUN echo "mongodb-org-shell hold" | sudo dpkg --set-selections

# RUN echo "mongodb-org hold" | sudo dpkg --set-selections
# RUN echo "mongodb-org-server hold" | sudo dpkg --set-selections
# RUN echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
# RUN echo "mongodb-org-tools hold" | sudo dpkg --set-selections

RUN mkdir cm
WORKDIR cm
RUN cloudmesh-installer git clone cloud
RUN cloudmesh-installer install cloud -e

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
"""

entry = """
db.createUser(
    {
        user: "<your-username>",
        pwd: "<your-password>",
        roles: [
            {
                role: "readWrite",
                db: "cloudmesh"
            }
        ]
    }
);
"""


# you can use writefile(filename, entry) to for example write a file. make
# sure to use path_expand and than create a dir. you can resuse commands form
# cloudmesh.common, but no other class

class CmsdCommand():

    def __init__(self):
        self.config_path = os.path.expanduser("~/.cloudmesh/cmsd")
        self.compose = "docker-compose -f " + self.config_path + "/docker-compose.yml "
        self.username = ''
        self.password = ''

    def docker_compose(self, command):
        os.system(self.compose + command)

    def update(self):
        self.docker_compose("down")

        self.delete_image()
        try:
            os.system("docker rmi cmsd_cloudmesh")
        except:
            pass
        self.clean()
        self.setup()
        self.up()
        self.create_image()

    def create_image(self):
        """
        reates image locally
        :return:
        """
        self.docker_compose('build')

    def download_image(self):
        """
        downloads image from dockerhub
        :return:
        """
        self.docker_compose('pull mongo')

    def delete_image(self):
        """
        deletes the cloudmesh image locally
        :return:
        """
        self.docker_compose('rm')

    def run(self, command=""):
        """
        run the command via the docker container

        :param command: the cms command to be run in the container
        """
        self.docker_compose('run ' + command)

    def cms(self, command=""):
        """
        run the command via the docker container

        :param command: the cms command to be run in the container
        """
        self.run("cloudmesh cms " + command)

    def up(self):
        """
        starts up the containers for cms
        """
        self.docker_compose('up -d')

    def ps(self):
        """
        docker-compose ps
        """
        self.docker_compose('ps')

    def stop(self):
        """
        docker-compose stop
        """
        self.docker_compose('stop')

    def shell(self):
        """
        docker-compose stop
        """
        self.docker_compose('exec cmsd sh')

    def setup(self, config_path="~/.cloudmesh/cmsd"):
        """
        this will copy the docker compose yaml and json file into the config_path
        only if the files do not yet esixt
        :param config_path:
        :return:
        """

        self.config_path = os.path.expanduser(config_path)

        d = Path(self.config_path)
        if not d.exists():
            print("creating",  self.config_path)
            Path(self.config_path).mkdir(parents=True, exist_ok=True)

        self.username = Config()["cloudmesh"]["data"]["mongo"]["MONGO_USERNAME"]
        self.password = Config()["cloudmesh"]["data"]["mongo"]["MONGO_PASSWORD"]
        if not os.path.exists(self.config_path):
            print(self.config_path)
            os.makedirs(self.config_path)

        if not os.path.exists(self.config_path + '/Dockerfile'):
            writefile(self.config_path + '/Dockerfile', dockerfile)

        if not os.path.exists(self.config_path + '/docker-compose.yml'):
            dc = dockercompose.replace("<your-username>", self.username).replace("<your-password>", self.password)
            writefile(self.config_path + '/docker-compose.yml', dc)

        if not os.path.exists(self.config_path + '/mongo-init.js'):
            et = entry.replace("<your-username>", self.username).replace("<your-password>", self.password)
            writefile(self.config_path + '/mongo-init.js', et)

    def clean(self):
        """
        remove the ~/.cloudmesh/cmsd dir
        :return:
        """
        print(self.config_path)
        if os.path.exists(self.config_path):
            shutil.rmtree(self.config_path)
            print('deleting', self.config_path)

    def do_cmsd(self):
        """
        ::

          Usage:
                cmsd --help
                cmsd --yaml (native | docker)
                cmsd --setup [--download]
                cmsd --clean
                cmsd --version
                cmsd --update
                cmsd --image
                cmsd --start
                cmsd --stop
                cmsd --ps
                cmsd --shell
                cmsd COMMAND...
                cmsd


          This command passes the arguments to a docker container
          that runs cloudmesh.

          Arguments:
              COMMAND the commands we bass along

          Description:

            cmsd --help

                prints this manual page

            cmsd --yaml (native | docker)

                switches the cloudmesh.yaml file to be used in native or docker
                mode, for cmsd to work, it must be in docker mode.


            cmsd --image

                list the container

            cmsd --setup [--download]

                downloads the source distribution, installes the image loaclly

                [--download is not yet supported, and will be implemented when the
                source setup works]

            cmsd --clean

                removes the container form docker

            cmsd --version

                prints out the verison of cmsd and the version of the container

            cmsd --update

                gets a new container form dockerhub

            cmsd COMMAND

                The command will be executed within the container, just as in
                case of cms.

            cmsd

                When no command is specified cms will be run in interactive
                mode.


        """

        doc = textwrap.dedent(self.do_cmsd.__doc__)
        arguments = docopt(doc, help=False)

        config = Config()

        #
        # check for yaml file consistency for mongo
        #

        #ok
        if config["cloudmesh.data.mongo.MODE"] != "docker" and \
            config["cloudmesh.data.mongo.MONGO_HOST"] != "mongo":
            print ("ERROR: The cloudmesh.yaml file is not configured for docker. Please use")
            print()
            print(" cmsd --yaml docker")
            print()
            return ""

        if arguments["--yaml"] and arguments["native"]: # implemented not tested

            print ("switch to native cms mode")

            config["cloudmesh.data.mongo.MODE"] = "native"
            config["cloudmesh.data.mongo.MONGO_HOST"] = "127.0.0.1"
            config.save()

        elif arguments["--yaml"] and arguments["docker"]: # implemented not tested

            print("switch to docker cms mode")
            config["cloudmesh.data.mongo.MODE"] = "docker"
            config["cloudmesh.data.mongo.MONGO_HOST"] = "mongo"
            config.save()

        elif arguments["--setup"]:
            self.setup()
            os.system(' '.join(['ls -l', self.config_path]))
            if arguments["--download"]:
                self.download_image()
            else:
                self.create_image()

        elif arguments["--version"]:
            print ("cmsd:", version)

            container_version = "not yet implemented"
            print("container:", container_version)
            print ()
            raise NotImplementedError

        elif arguments["--clean"]:
            self.delete_image()
            self.clean()

        elif arguments['--help']:
            print(doc)

        elif arguments['--image']:
            #
            # BUG does not work on windows. fix
            #
            if sys.platform == 'win32':
                raise NotImplementedError
            print("REPOSITORY                              TAG                 IMAGE ID            CREATED             SIZE")
            os.system("docker images | fgrep cmsd_cloudmesh")

        elif arguments["--stop"]:
            self.stop()

        elif arguments["--start"]:
            self.up()

        elif arguments["--ps"]:
            self.ps()

        elif arguments["--update"]:
            self.update()

        elif arguments["--shell"]:
            self.shell()

        elif arguments["COMMAND"]:
            command = ' '.join(arguments["COMMAND"])
            self.cms(command)

        elif arguments["COMMAND"] is None:

            print("start cms interactively")
            os.system("docker exec -ti cmsd /bin/bash")
            #self.docker_compose("exec cmsd /bin/bash")

        else:

            print(doc)

        return ""


def main():
    command = CmsdCommand()
    command.do_cmsd()


if __name__ == "__main__":
    main()