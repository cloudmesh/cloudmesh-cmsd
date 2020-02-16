# Cloudmesh cmsd

Cloudmesh cmsd is a command to run cloudmesh in a container regardles of
the OS. Thus it is extreemly easy to install and use.

cmsd will however use locally installed keys in `~/.ssh` and cloud
configurations stred in `~/.cloudmesh/cloudmehs.yaml`. The yaml file
will be created upon first call of cmsd if it is not available.

## How to use *cmsd*

### Prerequesites

* python 3.8 or newer
* We recommended to use a python virtual environment
* Install *cloudmesh-installer*. Refer [Cloudmesh manual](https://cloudmesh.github.io/cloudmesh-manual/installation/install.html#installation-of-cloudmesh-source-install-for-developers)


### cmsd installation 

- Activate python virtual environment

- Clone cloundmesh-cmsd repository to a directory of your preference. 
```
  cloudmesh-installer git clone cmsd
```

- Install cloudmesh-cmsd using cloudmesh-installer 

```
  cloudmesh-installer install cmsd
```

- Check installation 
```
cmsd --help
```

### cmsd initial setup 

To run cmsd, you would need a directory that would be mounted as the `~/.cloudmesh` directory in the container. Let's call this `CLOUDMESH_HOME_DIR`.

- Run initial setup 

```  
cmsd --setup <CLOUDMESH_HOME_DIR>
```

- Run `cmsd --ps` to see if the `cloudmesh-cms-container` is running! Additionally, check `CLOUDMESH_HOME_DIR` contains the `cloudmesh.yaml` file. 

- When running this setup initially, you would have to setup a password for the MongoDB. 

```
  cmsd config set cloudmesh.data.mongo.MONGO_PASSWORD=<some password>
```

- Run `cmsd --setup` again to complete the process. 

- Check if both `cloudmesh-cms-container` and `cloudmesh-mongo-container` both are running, using `cmsd --ps`

- You can check the `cloudmesh.yaml` file content by running, 

```
  cmsd config cat
```

### cmsd subsequent usages 

- To stop the containers, use `cmsd --stop`. Synonyms to `docker container stop ...`

- To start/restart the containers, use `cmsd --start`. Synonyms to `docker container start ...`

- To clean the containers (remove stopped containers), use `cmsd --clean`. Synonyms to `docker container rm ...`

- To log into the running `cloudmesh-cms-container`, use `cmsd --shell`. Synonyms to `docker exec -it ... /bin/bash`


### MongoDB and Mongo client connections  

cmsd is running an official MongoDB container from Docker Hub. Refer [here](https://hub.docker.com/_/mongo) and the mongo server instance is bound to the `127.0.0.1:27071` port. Therefore you can use any Mongo client to explore the database by connecting to this port. 

> NOTE:

> Unix - 
> At the setup, `CLOUDMESH_HOME_DIR/mongodb`  directory will be created and used as the data directory for mongo DB

> Windows - 
> Docker windows directory mounting does not work properly with mongo container. See [here](https://github.com/docker/for-win/issues/2189). Hence, a docker volume will be mounted as the data directory. 


### Example usecase - Creating a vm in AWS 

- Create an AWS account and add the authentication information in the `CLOUDMESH_HOME_DIR/cloudmesh.yaml` file. Refer [Cloudmesh Manual - AWS](https://cloudmesh.github.io/cloudmesh-manual/accounts/aws.html)

- Set cloud to `aws`
```
  cmsd set cloud=aws 
```

- Set AWS key name 
```
  cmsd set key=<key name> 
```

- Boot a vm with the default config
```
  cmsd vm boot 
```

## End user deployment 

Please uese a python virtualenv as to not interfere with your system python.
Activate your python venv. Next just call

    pip install cloudmesh-cmsd
    
This will install a command `cmsd` in your environment that you can use
as in place replacement for the cms command.

## Developer Source install

For developers it can be installed in an easy fashion with

    mkdir cm
    cd cm
    pip install cloudmesh-installer -U
    cloudmesh-installer git clone cmsd
    cloudmesh-installer git install cmsd
 
Now you can use the command 

    cmsd help

The source code is contained in 

    cloudmesh-cmsd


## Manual Page

```bash

  Usage:
        cmsd --help
        cmsd --setup [CLOUDMESH_HOME_DIR]
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

    cmsd --image

        list the container

    cmsd --setup [CLOUDMESH_HOME_DIR]

        Sets up cmsd 

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
