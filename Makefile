AUTHOR := thombashi
PACKAGE := pytablewriter
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build
BUILD_WORK_DIR := _work
BUILD_PKG_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)


.PHONY: build-remote
build-remote:
	@rm -rf $(BUILD_WORK_DIR)
	@mkdir -p $(BUILD_WORK_DIR)
	@cd $(BUILD_WORK_DIR) && \
		git clone https://github.com/$(AUTHOR)/$(PACKAGE).git && \
		cd $(PACKAGE) && \
		tox -e build
	ls -lh $(BUILD_PKG_DIR)/dist/*

.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	travis lint
	@tox -e lint

.PHONY: clean
clean:
	@tox -e clean

.PHONY: docs
docs:
	@python setup.py build_sphinx --source-dir=$(DOCS_DIR)/ --build-dir=$(DOCS_BUILD_DIR) --all-files

.PHONY: idocs
idocs:
	@pip install --upgrade .
	@make docs

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: readme
readme:
	@cd $(DOCS_DIR) && tox -e readme

.PHONY: release
release:
	@cd $(BUILD_WORK_DIR)/$(PACKAGE); python setup.py release --sign
	@make clean

.PHONY: setup
setup:
	@pip install --upgrade -e .[test] tox
