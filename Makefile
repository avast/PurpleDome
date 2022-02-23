# Makefile for standard actions
#
#

.PHONY: test init deinit shipit pylint

# This is for CI on Github
check: tox.ini
	tox -e py

# Manual tests
test: tox.ini
	tox;
	coverage html;
	coverage report;
	pylint --rcfile=pylint.rc  *.py app/*.py plugins/base/*.py

shipit: test
	cd doc; make zip; cd ..
	git log --pretty="format: %aD %an:  %s" > shipit_log.txt
	python3 tools/shipit.py

# More detailed pylint tests.
pylint:
	pylint --rcfile=pylint.rc  *.py app/*.py plugins/base/*.py

# Testing if types are used properly
mypy:
	mypy --strict-optional  app/ plugins/base/

# Fixing mypy file by file
stepbystep:
	mypy --strict-optional --disallow-untyped-defs --check-untyped-defs plugins/base/ app/