
# PY_SRCS:=$(shell find . -name "*.py" -not -path "./build/*" -not -path "./dist/*")

# .PHONY: build clean 

# build: $(PY_SRCS)
# 	python -m PyInstaller --name MSAccess app.py

# clean:
# 	rm -rf build
# 	rm -rf dist 
# 	rm -rf MSAccess.spec

# sourcelist:
# 	@echo "Py source files:"
# 	@echo $(PY_SRCS)

current_directory = $(shell pwd)

.PHONY: dev
dev: 
	FLASK_APP="DataWorker:create_app()" \
	FLASK_ENV=development \
	DW_SETTINGS=$(current_directory)/dev_config.py \
	flask run

.PHONY: db
db:
	FLASK_APP="DataWorker:create_app()" \
	flask init-db

