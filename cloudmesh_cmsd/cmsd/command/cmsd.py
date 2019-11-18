from __future__ import print_function
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
        return ""


if __name__ == "__main__":
    command = CmsdCommand()
    command.do_cmsd(sys.argv)
