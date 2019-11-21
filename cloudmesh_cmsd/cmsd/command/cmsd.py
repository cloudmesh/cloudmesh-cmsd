from __future__ import print_function

import os

from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import writefile
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.dotdict import dotdict
import sys
from docopt import docopt
import textwrap

docercompose = """
PUT THE COMPOSE HERE
"""

entry = """
PUT THAT JSON HERE
"""

# you can use writefile(filename, entry) to for example write a file. make
# sure to use path_expand and than create a dir. you can resuse commands form
# cloudmesh.common, but no other class

class CmsdCommand():

    def create_image(self):
        """
        reates image locally
        :return:
        """
        os.system('docker-compose build')

    def download_image(self):
        """
        downloads image from dockerhub
        :return:
        """
        os.system('docker-compose pull mongo')

    def delete_image(self):
        """
        deletes the cloudmesh image locally
        :return:
        """
        os.system('docker-compose rm')

    def run(self, *args):
        """
        run the command via the docker container

        :param args:
        :return:
        """
        os.system('docker-compose up')

    def setup(self, config_path="~/.cloudmesh/cmsd"):
        """
        this will copy the docker compose yaml and json file into the config_path
        only if the files do not yet esixt
        :param config_path:
        :return:
        """
        if not os.path.exists('docker-compose.yml'):
            from shutil import copyfile
            copyfile(config_path + '/docker-compose.yml', '.')

    def clean(self):
        """
        remove the ~/.cloudmesh/cmsd dir
        :return:
        """
        os.removedirs('~/.cloudmesh/cmsd')

    def do_cmsd(self):
        """
        ::

          Usage:
                cmsd setup [--download]
                cmsd clean
                cmsd COMMAND

          This command passes the arguments to a docker container
          that runs cloudmesh.

          Arguments:
              COMMAND the commands we bass along


        """

        doc = textwrap.dedent(self.do_cmsd.__doc__)
        args = docopt(doc, help=False)
        arguments = dotdict(args)

        #print("B", arguments)
        #print("A", args)

        if arguments.setup:
            if arguments["--download"]:
                self.download_image()
            else:
                self.create_image()

        elif arguments.clean:
            self.delete_image()

        elif arguments.COMMAND:
            self.run(arguments)

        os.system('docker-compose start')
        return ""

def main():
    command = CmsdCommand()
    command.do_cmsd()

if __name__ == "__main__":
    main()
