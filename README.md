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

