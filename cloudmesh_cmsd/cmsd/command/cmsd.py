from __future__ import print_function

import os

from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.dotdict import dotdict
#
#  DO NOT USE A CMD5 plugin, but just a regular python program
#  use plain docopts here
#
import sys


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
        print(os.path.exists('docker-compose.yml'))

    def clean(self):
        """
        remove the ~/.cloudmesh/cmsd dir
        :return:
        """
        os.removedirs('~/.cloudmesh/cmsd')

    @staticmethod
    def do_cmsd(args):
        """
        ::

          Usage:
                cmsd COMMAND...

          This command passes the arguments to a docker container
          that runs cloudmesh.

          Arguments:
              COMMAND the commands we bass along


        """
        #arguments.FILE = arguments['--file'] or None

        arguments = dotdict(args)
        VERBOSE(arguments)

        if arguments.FILE:
            print("option a")

        elif arguments.list:
            print("option b")

        Console.error("This is just a sample")
        os.system('docker-compose start')
        return ""


if __name__ == "__main__":
    command = CmsdCommand()
    command.do_cmsd(sys.argv)
