![main branch test](https://github.com/avast/PurpleDome/actions/workflows/makefile.yml/badge.svg?branch=main)

# PurpleDome creates simulated systems which hack each other 

It creates several virtual machines to simulate a target network. A Kali attacker will be spawned and use configured attacks to blast at the targets. Those attacks can be Kali command line tools, Caldera abilities or Metasploit tools.

The goal is to test sensors and detection logic on the targets and in the network and improve them.

The system is at the same time reproducible and quite flexible (target system wise, vulnerabilities on the targets, attacks).

## Installation

On a current Ubuntu system, just execute the *init.sh* to install the required packages and set up the virtual env.

```
./init.sh
```

Default vm will be vagrant and virtualbox

Before using any PurpleDome commands switch into the python environment:

```
source venv/bin/activate
```

## My first experiment

Run

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
