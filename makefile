
.PHONY: build
build: 
	python -m build

.PHONY: publish
publish: 
	python -m twine upload --repository testpypi dist/*

.PHONY: build_deploy
build_deploy: build publish

.PHONY: clean
clean:
	rm -rf dist