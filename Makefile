# Makefile for standard actions
#
#

.PHONY: test init deinit shipit pylint

test: tox.ini
	tox;
	coverage html;
	coverage report;

shipit: test
	cd doc; make html; cd ..
	git log --pretty="format: %aD %an:  %s" > shipit_log.txt
	python3 tools/shipit.py

# More detailed pylint tests.
pylint:
	pylint --rcfile=pylint.rc  *.py app/*.py plugins/base/*.py