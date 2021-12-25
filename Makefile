.PHONY: help clean clean-build list test test-all coverage docs release sdist

help:
	@echo "clean-build - remove build artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean:
	rm -fr .tox
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

lint:
	flake8 modeltranslation_wagtail test

test:
	PYTHONPATH="$PYTHONPATH:." py.test --ds=test.project.settings

test-all:
	tox

coverage:
	coverage run --source modeltranslation_wagtail PYTHONPATH="$PYTHONPATH:." py.test --ds=test.project.settings
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/modeltranslation_wagtail.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ modeltranslation_wagtail
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload -s dist/*

sdist: clean
	python setup.py sdist
	python setup.py bdist_wheel upload
	ls -l dist
