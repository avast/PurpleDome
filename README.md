![main branch test](https://github.com/avast/PurpleDome/actions/workflows/main_by_makefile.yml/badge.svg?branch=main)
![develop branch test](https://github.com/avast/PurpleDome/actions/workflows/develop_by_makefile.yml/badge.svg?branch=develop)

**Important: During the next months the main developer is mostly AFK. There are fallback maintainers, but you can expect reduced response time. Please plan accordingly, fork and cooperate. Thanks** 

# PurpleDome creates simulated systems which hack each other 

It creates several virtual machines to simulate a target network. A Kali attacker will be spawned and use configured attacks to blast at the targets. Those attacks can be Kali command line tools, Caldera abilities or Metasploit tools.

The goal is to test sensors and detection logic on the targets and in the network and improve them.

The system is at the same time reproducible and quite flexible (target system wise, vulnerabilities on the targets, attacks).

## Installation

On a current Ubuntu 21.10 system, just execute the *init.sh* to install the required packages and set up the virtual env. 

You need python 3.9 (which is part of this Ubuntu)

And it will not run properly in a VM as it spawns its own VMs ... unless VT-x is available.
We confirmed it is working in VirtualBox. Please reserve enough disk space. The simple hello_world will already download a kali and an ubuntu image. They must be stored on your VM. 

```
./init.sh
```

Default vm will be vagrant and virtualbox

Before using any PurpleDome commands switch into the python environment:

```
source venv/bin/activate
```

## My first experiment

Run and be very patient. The first time it runs it will build target and attacker VMs which is time consuming and will need some bandwidth. 

```
python3 ./experiment_control.py -vvv  run --configfile hello_world.yaml
```

This will:

* Use vagrant to generate attacker and target
* run them
* run several attacks from the attacker to the target
* zip sensor logs and attack logs together

Building the machines from vagrant will take some time ont he first run. Please be patient.

After the experiment ran, open the zip file with the attack log and all the sensor logs:

```
file-roller loot/2021_11_11___12_13_14/2021_11_11___12_13_14.zip
```

or jump directly into the human readable attack log 

```
evince tools/human_readable_documentation/build/latex/purpledomesimulation.pdf
```

(which is included in the zip as well)

### Potential issues here

The vagrant configuration file systems/Vagrantfile defines a bridged network shared between the VirtualBox VMs. If you do not have one or yours has a different name, please create one and change the config. Currently every machine uses:

```
attacker.vm.network "public_network", bridge: "enp4s0"
```


## Fixing issues

### Machine creation

One of the big steps is creation of attacker and target machines. If this fails, you can do the step manually and check why it fails.

```
cd systems
vagrant up attacker
vagrant up target3
vagrant ssh attacker
# do someting
exit
vagrant ssh target
# do something
exit
vagrant destroy target3
vagrant destroy attacker
```

### Caldera issues

The caldera server is running on the attacker. It will be contacted by the implants installed on the client and remote controlled by PurpleDome using a REST Api. This can be tested using curl:

```
curl -H 'KEY: ADMIN123' http://attacker:8888/api/rest -H 'Content-Type: application/json' -d '{"index":"adversaries"}'
```

If there are errors, connect to the attacker using ssh and monitor the server while contacting it. Maybe kill it first.

```
cd caldera
python3 server.py --insecure
```

## Running the basic commands

All command line tools have a help included. You can access it by the "--help" parameter

```
python3 ./experiment_control.py -v  run
```

* -v is verbosity. To spam stdout use -vvv
* run is the default command
* --configfile <filename> is optional. If not supplied it will take experiment.yaml

Most of the configuration is done in the yaml config file. For more details check out the full documentation

## Testing

Basic code and unit tests can be run by

```
make test
```

That way you can also see if your env is set up properly.

It will also check the plugins you write for compatibility. 

the tool

```
./pydantic_test.py
```

is *not* included in the make test. But you can use it manually to verify your yaml config files. As they tend to become quite complex this is a time safer.

## More documentation

This README is just a short overview. In depth documentation can be found in the *doc* folder.

Documentation is using sphinx. To compile it, go into this folder and call

```
make html
```

Use your browser to open build/html/index.html and start reading.

## Development

The code is stored in [https://github.com/avast/PurpleDome](https://github.com/avast/PurpleDome). Feel free to fork it and create a pull request. 

Development happens in *feature branches* branched of from *develop* branch. And all PRs go back there.
The branch *release* is a temporary branch from *develop* and will be used for bug fixing before a PR to *main* creates a new release. Commits in main will be marked with tags and the *changelog.txt* file in human readable form describe the new features.

https://nvie.com/posts/a-successful-git-branching-model/

Short:

* As a user, the *main* branch is relevant for you
* Start a feature branch from *develop*
* When doing a hotfix, branch from *main* 

### GIT

Branching your own feature branch

```
$ git checkout development
$ git pull --rebase=preserve
$ git checkout -b my_feature
```

Do some coding, commit.

Rebase before pushing

```
$ git checkout development
$ git pull --rebase=preserve
$ git checkout my_feature
$ git rebase development
```

Code review will be happening on github. If everything is nice, you should squash the several commits you made into one (so one commit = one feature). This will make code management and debugging a lot simpler when you commit is added to develop and main branches

```
git rebase --interactive
git push --force
```

### Argcomplete

https://kislyuk.github.io/argcomplete/

Is a argparse extension that registers the command line arguments for bash. It requires a command line command to register it globally. This is added to init.sh

The configuration will be set in /etc/bash_completion.d/ . Keep in mind: It will require a shell restart to be activated

## BibTeX

When doing scientific research using Purple Dome, please use this BibTeX snippet in your paper:

```
@misc{PurpleDome:internet,
author = {Thorsten Sick and Fabrizio Biondi},
title = {GitHub - avast/PurpleDome: Simulation environment for attacks on computer networks},
note = {(visited on 09.02.2022)},
howpublished = "\url{https://github.com/avast/PurpleDome}",
}
```
