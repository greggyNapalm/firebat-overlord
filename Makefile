test:
		nosetests -v

coverage:
		nosetests --with-coverage --cover-html --cover-html-dir=html_cover --cover-package=firebat-manager

doc:
		sphinx-build -a -b html docs/ html_docs

release:
		python setup.py sdist

upload:
		python setup.py sdist upload
