from __future__ import print_function

import os
import shutil
import textwrap

from cloudmesh.common.util import writefile
from cloudmesh.configuration.Config import Config
from docopt import docopt

dockercompose = """
version: '3'
services:
  cloudmesh:
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

RUN set -x \
        && apt-get -y update \
        && apt-get -y upgrade \
        && apt-get -y --no-install-recommends install build-essential \
                                                      git \
                                                      curl \
                                                      wget \
                                                      sudo \
                                                      gnupg \
                                                      ca-certificates \
                                                      vim
RUN set -x \
        && wget -q -O server.asc https://www.mongodb.org/static/pgp/server-4.2.asc \
        && apt-key add server.asc \
        && echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list \
        && apt-get -y update \
        && apt-get -y upgrade \
        && apt-get -y --no-install-recommends install mongodb-org-shell \
                                                      mongodb-org-tools
RUN set -x \
        && apt-get -y install python3 \
                              python3-pip \
        && rm -rf /var/lib/apt/lists/* \
        && update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
        && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1 \
        && pip install cloudmesh-installer

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
        self.username = ''
        self.password = ''

    def create_image(self):
        """
        reates image locally
        :return:
        """
        os.system(f'docker-compose -f {self.config_path}/docker-compose.yml build')

    def download_image(self):
        """
        downloads image from dockerhub
        :return:
        """
        os.system(f'docker-compose -f {self.config_path}/docker-compose.yml pull mongo')

    def delete_image(self):
        """
        deletes the cloudmesh image locally
        :return:
        """
        if os.path.exists(f'{self.config_path}/docker-compose.yml'):
            os.system(f'docker-compose -f {self.config_path}/docker-compose.yml rm')

    def run(self, *args):
        """
        run the command via the docker container

        :param args:
        :return:
        """
        os.system(f'docker-compose -f {self.config_path}/docker-compose.yml up')

    def setup(self, config_path="~/.cloudmesh/cmsd"):
        """
        this will copy the docker compose yaml and json file into the config_path
        only if the files do not yet esixt
        :param config_path:
        :return:
        """
        self.config_path = os.path.expanduser(config_path)
        config = Config()
        self.username = config["cloudmesh.data.mongo.MONGO_USERNAME"]
        self.password = config["cloudmesh.data.mongo.MONGO_PASSWORD"]
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
            print('deleted')

    def do_cmsd(self):
        """
        ::

          Usage:
                cmsd setup [--download]
                cmsd clean
                cmsd version
                cmsd update
                cmsd help
                cmsd run


          This command passes the arguments to a docker container
          that runs cloudmesh.

          Arguments:
              COMMAND the commands we bass along

          Description:

            cmsd setup [--download]

                Setup configurations

            cmsd clean

                Remove configurations and built images

            cmsd version

                Print out the current version

            cmsd update

                Clean up and re-configure

            cmsd help

                Print help docs

            cmsd run

                Start up VMs
        """

        doc = textwrap.dedent(self.do_cmsd.__doc__)
        arguments = docopt(doc, help=False)

        if arguments["setup"]:
            self.setup()
            os.system(' '.join(['ls -l', self.config_path]))
            if arguments["--download"]:
                self.download_image()
            else:
                self.create_image()

        elif arguments["clean"]:
            self.delete_image()
            self.clean()

        elif arguments['help']:
            print(doc)

        elif arguments['version']:
            os.system(f'cat {os.path.dirname(os.path.abspath(__file__))}/../__version__.py')

        elif arguments['update']:
            self.delete_image()
            self.clean()
            self.setup()

        elif arguments['run']:
            self.setup()
            self.run(arguments)

        else:
            print(doc)
        return ""


def main():
    command = CmsdCommand()
    command.do_cmsd()


if __name__ == "__main__":
    main()
