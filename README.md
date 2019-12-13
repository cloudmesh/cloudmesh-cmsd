# Cloudmesh cmsd

Cloudmesh cmsd is a command to run cloudmesh in a container regardles of
the OS. Thus it is extreemly easy to install and use.

cmsd will however use locally installed keys in `~/.ssh` and cloud
configurations stred in `~/.cloudmesh/cloudmehs.yaml`. The yaml file
will be created upon first call of cmsd if it is not available.

## End user deployment (not yet supported)

Please uese a python virtualenv as to not interfere with your system python.
Activate your python venv. Next just call

    pip install cloudmesh-cmsd
    
This will install a command `cmsd' in your environment that you can use
as in place replacement for the cms command.

## Source install


For developers it can be installed in an easy fashion with

    mkdir cm
    cd cm
    pip install cloudmesh-installer
    cloudmesh-installer git clone docker
    cloudmesh-installer git install docker
 
Now you can use the command 

    cmsd help

The source code is contained in 

    cloudmesh-cmsd


## Bugs

Despite the TA reporting it works, we could not install it we get the
error.

cmsd help
ERROR: .FileNotFoundError: [Errno 2] No such file or directory: '/Users/grey/.cloudmesh/cmsd/docker-compose.yml'

Clearly the yml file need to be deployed if it can not be found. Users
must not have to install anything! This all needs to be part of the
script.

If you encounter this error. please send a mail to the instructors in
piazza that you need this tool.

## Missing setup documentation notes

This has to be cleanued up and changed once we get the agreed upon 
cmsd command whichis as we said from the beginning a plu gin replacement for cms

The only thing we may have to think about are the options. to make sure
they are not part of the command all function names not within cms are
preceeded by a --

git missing

pip install -e .

# NOT WAHAT WE ASKED FOR

NMative setup (automatize this)

      MONGO_AUTOINSTALL: true
      MONGO_BREWINSTALL: false
      MONGO_URL: mongodb://mongodb:27017
      MODE: native
      LOCAL: ~/local
      MONGO_DBNAME: cloudmesh
      MONGO_HOST: 127.0.0.1
      MONGO_PORT: '27017'

docker setup (utomatize this)

      MONGO_AUTOINSTALL: true
      MONGO_BREWINSTALL: false
      # MONGO_URL: 'mongodb://mongo:27017'
      MODE: running
      LOCAL: ~/local
      MONGO_DBNAME: cloudmesh
      MONGO_HOST: 'mongo'
      MONGO_PORT: '27017'

#docker container prune --force

# docker stop b8487498e2d4c1503b0b86d67268157598f425e05cb


MONGO setup




# terminal 1

cmsd --version

cmsd help
cmsd clean
cmsd setup
cmsd init
cmsd run

# inconvenient method too look up container id, that was outomated in gregors suggestion or suppoesd to be

#terminal 2

docker exec -it ID /bin./bash

# robo3t

we can jsut use it and bind againt localhost and 27071 with password and username

