# Cloudmesh cmsd

Cloudmesh cmsd is a command to run cloudmesh in a container regardles of
the OS. Thus it is extreemly easy to install and use.

cmsd will however use locally installed keys in `~/.ssh` and cloud
configurations stred in `~/.cloudmesh/cloudmehs.yaml`. The yaml file
will be created upon first call of cmsd if it is not available.

## End user deployment 

Please uese a python virtualenv as to not interfere with your system python.
Activate your python venv. Next just call

    pip install cloudmesh-cmsd
    
This will install a command `cmsd' in your environment that you can use
as in place replacement for the cms command.

## Developer Source install

For developers it can be installed in an easy fashion with

    mkdir cm
    cd cm
    pip install cloudmesh-installer -U
    cloudmesh-installer git clone docker
    cloudmesh-installer git install docker
 
Now you can use the command 

    cmsd help

The source code is contained in 

    cloudmesh-cmsd


## Mongo Configuration in ~/.cloudmesh/cloudmesh.yaml

You will need to set the configuration MODE from native to running

Native setup (typicall you will have)

      MONGO_AUTOINSTALL: true
      MONGO_BREWINSTALL: false
      MONGO_URL: mongodb://mongodb:27017
      MODE: native
      LOCAL: ~/local
      MONGO_DBNAME: cloudmesh
      MONGO_HOST: 127.0.0.1
      MONGO_PORT: '27017'

docker setup (you need to change this to)

      MONGO_AUTOINSTALL: true
      MONGO_BREWINSTALL: false
      # MONGO_URL: 'mongodb://mongo:27017'
      MODE: running
      LOCAL: ~/local
      MONGO_DBNAME: cloudmesh
      MONGO_HOST: 'mongo'
      MONGO_PORT: '27017'



## Manual Page

```bash

  Usage:
        cmsd --help
        cmsd --yaml (native | docker)
        cmsd --setup [CLOUDMESH_HOME_DIR] [--download]
        cmsd --clean
        cmsd --version
        cmsd --update
        cmsd --image
        cmsd --start
        cmsd --stop
        cmsd --ps
        cmsd --shell
        cmsd COMMAND... [--refresh]
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

```
