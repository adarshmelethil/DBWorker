
PY_SRCS:=$(shell find . -name "*.py" -not -path "./build/*" -not -path "./dist/*")

.PHONY: build clean 

build: $(PY_SRCS)
	python -m PyInstaller --name MSAccess app.py

clean:
	rm -rf build
	rm -rf dist 
	rm -rf MSAccess.spec

sourcelist:
	@echo "Py source files:"
	@echo $(PY_SRCS)