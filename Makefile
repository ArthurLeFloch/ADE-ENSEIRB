
install:
	python3 setup.py sdist bdist_wheel && pip install .

test:
	cd tst && python3 -m unittest

clean:
	rm -rf ade_enseirb/__pycache__
	rm -rf ade_enseirb.egg-info
	rm -rf build
	rm -rf dist
	rm -f .rooms.json
	rm -f tst/.rooms.json
