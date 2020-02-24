# Cloudmesh cmsd

Cloudmesh cmsd is a command to run cloudmesh in a container regardless of
the OS. Thus it is extremely easy to install and use.

cmsd will, however, use locally installed keys in `~/.ssh` and typically
cloud configurations stored in `~/.cloudmesh/cloudmesh.yaml`. The YAML
file is created upon the first call of `cmsd` if it is not available.


### Prerequesites

* Docker
* Python 3.8 or newer
* We strongly recommended using a python virtual environment

## How to use *cmsd*

Important. You must have cms in debug off mode. to use the cmsd command

```
$ cms debug off
```


### User instalation

Please use a python virtualenv as to not interfere with your system
python and activate your python venv.

Linux, osx: 

```bash
$ python3.8 -m venv ~/ENV3
$ source ~/ENV3/bin/activate
$ pip install pip -U 
```

In Windows you can do this with 

```bash
$ python -m venv ENV3
$ ENV3\Scripts\activate
$ pip install pip -U 
```

Now you can install cloudmesh cmsd simply with 

```bash
$ pip install cloudmesh-cmsd
```
    
It will install cloudmesh in containers. The containers are called

- `cloudmesh-cms` 
- `cloudmesh-mongo` 


### Developer Source install    

For developers, it can be installed in an easy fashion with 

Linux, osx: 

```bash
$ python3.8 -m venv ~/ENV3
$ source ~/ENV3/bin/activate
$ pip install pip -U
$ mkdir cm   
$ cd cm  
$ pip install cloudmesh-installer -U 
$ cloudmesh-installer git clone cmsd 
$ cloudmesh-installer install cmsd   
```

Windows:

```bash
$ python -m venv ENV3
$ ENV3\Scripts\activate
$ pip install pip -U
$ mkdir cm   
$ cd cm  
$ pip install cloudmesh-installer -U 
$ cloudmesh-installer git clone cmsd 
$ cloudmesh-installer install cmsd   
```

### Defult setup

The defualt setup is simply done with 

```bash
$ cmsd --setup
```

### Custom cmsd setup 

To run cmsd, you would need a configuration directory that is mounted
into the container. 

Let us call this `CLOUDMESH_CONFIG_DIR`. Set
`CLOUDMESH_CONFIG_DIR` as an environment variable.

For Unix:
```
$ export CLOUDMESH_CONFIG_DIR=<path to CLOUDMESH_HOME_DIR>
```

For Windows:
```
> set CLOUDMESH_CONFIG_DIR=<path to CLOUDMESH_HOME_DIR>
```

> NOTE: 
> - `CLOUDMESH_CONFIG_DIR` path must not have in any spaces.
> - Clarification for Windows users: 
>  - For example `C:\.cloudmesh` will work, so does 
> `C:\Users\gregor\.cloudmesh`, but not `C:\Users\gregor von Laszewski\.cloudmesh`)
>   - Make sure that the drive of the `CLOUDMESH_CONFIG_DIR` is granted file 
>     access in Docker settings

Run setup. If you are running setup on an empty `CLOUDMESH_CONFIG_DIR`,  you 
will be asked to key in some details that are required for the setup, such as 
profile details, Mongo DB credentials, etc. 

```  
$ cmsd --setup 
```

Run the following command to see if the `cloudmesh-cms-container` is running! 
Additionally, check `CLOUDMESH_CONFIG_DIR` contains the `cloudmesh.yaml` file. 

### Commands

To list the containers, pleas use

```
$ cmsd --ps
```

Run the following to verify if the configurations you entered have been 
properly reflected in the `cloudmesh.yaml` file. 

```
$ cmsd config cat
```

Initialize cloudmesh using the following command. 

```
$ cmsd init
```

To test if things are working, issue the command,

```
$ cmsd key list 
```

To stop the containers use

`cmsd --stop`

To start the containers use

`cmsd --start`

To remove the containers use

`cmsd --clean`

To login to the container via a shell use

`cmsd --shell`



### Example Usecase - Creating a vm in Chameleon Cloud 

To modify the parameters use the command

```
cmsd --gui quick
```

and make sure the MongoDB MODE is set to running. This is automatically
done by the setup. Make sure you add your username, and password, as
well as the network id and the project id and name. Test if it works with 


```
cmsd flavor list --refresh
```

### Example Usecase - Creating a vm in AWS 

Create an AWS account and add the authentication information in the 
`CLOUDMESH_HOME_DIR/cloudmesh.yaml` file. Refer [Cloudmesh Manual - AWS](https://cloudmesh.github.io/cloudmesh-manual/accounts/aws.html)

Set cloud to `aws`

```
$ cmsd set cloud=aws 
```

Set AWS key name 

```
$ cmsd set key=<key name> 
```

Boot a vm with the default config

```
$ cmsd vm boot 
```

### MongoDB and Mongo client connections  

cmsd is running an official MongoDB container from Docker Hub. Refer [here](https://hub.docker.com/_/mongo).

Mongo server container is bound to `127.0.0.1:27071` port. Therefore you can use 
any Mongo client to explore the database by connecting to this port. 

## Manual Page

```bash
  Usage:
        cmsd --help
        cmsd --setup
        cmsd --clean
        cmsd --version
        cmsd --update
        cmsd --start
        cmsd --stop
        cmsd --ps
        cmsd --gui COMMAND...
        cmsd --shell
        cmsd --pipe
        cmsd COMMAND...


  This command passes the arguments to a docker container
  that runs cloudmesh.

  Arguments:
      COMMAND the commands we bass along

  Description:

    cmsd --help

        prints this manual page

    cmsd --setup

        downloads the source distribution, installs the image locally

    cmsd --clean

        removes the container form docker

    cmsd --version

        prints out the verison of cmsd and the version of the container

    cmsd --gui
        runs cloudmesh gui on the docker container

    cmsd --update

        gets a new container form dockerhub

    cmsd COMMAND

        The command will be executed within the container, just as in
        case of cms.

    cmsd

        When no command is specified cms will be run in interactive
        mode.



```
## Quickstart

### macOS with python 3.8.1 from python.org

1. Requirements:

   * Have a sername without a space.
   * Have docker installed and accessible to the user. 
   * Have python 3.8.1 from python.org installed.

   Create a key `~/.ssh/id_rsa` if you do not already have one 
   
   ```bash
   $ ssh-keygen
   ```

2. Install:

   Open a new terminal, 

   ```bash
   $ python3.8 -m venv ~/ENV3
   $ source ~/ENV3/bin/activate
   $ pip install cloudmesh-cmsd
   ```
   

3. Setup:

   ```bash
   $ cmsd --setup
   $ cmsd init
   ```
4. Do some simple tests to see if it works

   Testing help command: 
   
   ```bash
   $ cmsd help
   ```
   
   Output:
   
   ```
   Documented commands (type help <topic>):
   ========================================
   EOF       config     help       man        quit      ssh        vcluster      
   admin     container  host       open       register  start      version       
   aws       data       image      openstack  sec       stop       vm            
   azure     debug      info       pause      service   stopwatch  workflow_draft
   banner    default    init       plugin     set       sys      
   check     echo       inventory  provider   shell     test     
   clear     flavor     ip         py         sleep     var      
   commands  group      key        q          source    vbox 
   ```
   
   Testing banner command:
   
   ```bash
   $ cmsd banner hello
   ```
   
   Output: 
   
   ```
   banner
   ######################################################################
   # hello
   ######################################################################
   ```
   
   Testing sec command:
   
   ```bash
   $ cmsd sec rule list
   ```
   
   Output: 
   
   ```
   +-------+----------+-----------+-----------+
   | Name  | Protocol | Ports     | IP Range  |
   +-------+----------+-----------+-----------+
   | ssh   | tcp      | 22:22     | 0.0.0.0/0 |
   | icmp  | icmp     |           | 0.0.0.0/0 |
   | flask | tcp      | 8000:8000 | 0.0.0.0/0 |
   | http  | tcp      | 80:80     | 0.0.0.0/0 |
   | https | tcp      | 443:443   | 0.0.0.0/0 |
   +-------+----------+-----------+-----------+
   ```
   
## Demonstartion of the different uses of cmsd

1. Commandline

   ```bash
   $ cmsd banner hallo
   
   banner
   ######################################################################
   # hello
   ######################################################################
   ```

2. Pipe

   ```
   $ echo "banner hello" | cmsd --pipe
   
   +-------------------------------------------------------+
   |   ____ _                 _                     _      |
   |  / ___| | ___  _   _  __| |_ __ ___   ___  ___| |__   |
   | | |   | |/ _ \| | | |/ _` | '_ ` _ \ / _ \/ __| '_ \  |
   | | |___| | (_) | |_| | (_| | | | | | |  __/\__ \ | | | |
   |  \____|_|\___/ \__,_|\__,_|_| |_| |_|\___||___/_| |_| |
   +-------------------------------------------------------+
   |                  Cloudmesh CMD5 Shell                 |
   +-------------------------------------------------------+
   
   cms> banner
   ######################################################################
   # hello
   ######################################################################   ```
   ```
   
3. Interactive

   ```
   $ cmsd
   start cms interactively
   
   +-------------------------------------------------------+
   |   ____ _                 _                     _      |
   |  / ___| | ___  _   _  __| |_ __ ___   ___  ___| |__   |
   | | |   | |/ _ \| | | |/ _` | '_ ` _ \ / _ \/ __| '_ \  |
   | | |___| | (_) | |_| | (_| | | | | | |  __/\__ \ | | | |
   |  \____|_|\___/ \__,_|\__,_|_| |_| |_|\___||___/_| |_| |
   +-------------------------------------------------------+
   |                  Cloudmesh CMD5 Shell                 |
   +-------------------------------------------------------+
   
   cms> banner hello
   banner
   ######################################################################
   # hello
   ######################################################################
   cms> quit
   ```
 
 4. Access container shell for development
 
    ```bash
    $ cmsd --shell

    root@docker-desktop:/cm# ls -1
    cloudmesh-aws
    cloudmesh-azure
    cloudmesh-cloud
    cloudmesh-cmd5
    cloudmesh-common
    cloudmesh-configuration
    cloudmesh-inventory
    cloudmesh-openstack
    cloudmesh-sys
    cloudmesh-test
    root@docker-desktop:/cm# 
    ```
