PROJECT := plumbium

.PHONY: checks test docstyle codestyle lint

checks: test docstyle codestyle lint

test:
	py.test --cov

docstyle:
	pydocstyle $(PROJECT)

codestyle:
	pycodestyle $(PROJECT)

lint:
	pylint $(PROJECT)
