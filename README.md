# Creates vulnerable systems

Uses vagrant to set up vulnerable systems. Sensors and maybe attack agents will be installed as well.

Will use vagrant config. It is quite likely that it we will need some parameters to create similar but not identical systems.

## Testing

*Prerequisites:*

Install python environment, e.g. using `conda`:
```
conda create -n purpledome python=3.8
conda activate purpledome
```

Then install the required dependencies in the crated python environment:
```
pip install -r requirements.txt
```

*Call test suite:*

```
make test
```

## Documentation

Documentation is using sphinx

https://www.sphinx-doc.org/en/master/index.html

Generate it switching to the directory doc and calling

*make all*

