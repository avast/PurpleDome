![main branch test](https://github.com/avast/PurpleDome/.github/workflows/makefile.yml/badge.svg?branch=main)

# PurpleDome creates simulated systems which hack each other 

It creates several virtual machines to simulate a target network. A Kali attacker will be spawned and use configured attacks to blast at the targets. Those attacks can be Kali command line tools, Caldera abilities or Metasploit tools.

The goal is to test sensors and detection logic on the targets and in the network and improve them.

The system is at the same time reproducible and quite flexible (target system wise, vulnerabilities on the targets, attacks).

## Installation

Setting up the python environment:

```
./init.sh
```

The typical local use case is to create the machines using Vagrant and running them in VirtualBox:

...
sudo apt install vagrant virtualbox
...

You will have to switch into the python environment to run it

Before using any PurpleDome commands switch into the python environment:

...
source venv/bin/activate
...

(this will contain the libraries in the required versions)

## Testing

Basic code and unit tests can be run by

```
make test
```

That way you can also see if your env is set up properly

## Running the basic commands

All command line tools have a help included. You can access it by the "--help" parameter

...
python3 ./experiment_control.py -v  run
...

* -v is verbosity. To spam stdout use -vvv
* run is the default command
* --configfile <filename> is optional. If not supplied it will take experiment.yaml

Most of the configuration is done in the yaml config file. For more details check out the full documentation

## The real documentation

This README is just a short overview. In depth documentation can be found in the *doc* folder.

Documentation is using sphinx

https://www.sphinx-doc.org/en/master/index.html

Generate it switching to the directory doc and calling

*make all*

## Development

Development happens in *feature branches* branched of from *develop* branch. And all PRs go back there.
The branch *release* is a temporary branch from *develop* and will be used for bug fixing before a PR to *main* creates a new release. Commits in main will be marked with tags and the *changelog.txt* file in human readable form describe the new features.

https://nvie.com/posts/a-successful-git-branching-model/
