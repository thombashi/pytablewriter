AUTHOR := thombashi
PACKAGE := pytablewriter
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build
BUILD_WORK_DIR := _work
PKG_BUILD_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)
PYTHON := python3


.PHONY: build-remote
build-remote: clean
	@mkdir -p $(BUILD_WORK_DIR)
	@cd $(BUILD_WORK_DIR) && \
		git clone https://github.com/$(AUTHOR)/$(PACKAGE).git --depth 1 && \
		cd $(PACKAGE) && \
		$(PYTHON) -m tox -e build
	ls -lh $(PKG_BUILD_DIR)/dist/*

.PHONY: build
build: clean
	@$(PYTHON) -m tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@$(PYTHON) -m tox -e lint

.PHONY: clean
clean:
	@rm -rf $(BUILD_WORK_DIR)
	@$(PYTHON) -m tox -e clean

.PHONY: docs
docs:
	@$(PYTHON) -m tox -e docs

.PHONY: idocs
idocs:
	@$(PYTHON) -m pip install --upgrade -q --disable-pip-version-check -e .
	@make docs

.PHONY: fmt
fmt:
	@$(PYTHON) -m tox -e fmt

.PHONY: readme
readme:
	@cd $(DOCS_DIR) && tox -e readme

.PHONY: release
release:
	@cd $(PKG_BUILD_DIR) && $(PYTHON) setup.py release --sign --search-dir $(PACKAGE)
	@make clean

.PHONY: setup-ci
setup-ci:
	@$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade tox

.PHONY: setup
setup: setup-ci
	@$(PYTHON) -m pip install --upgrade -q --disable-pip-version-check -e .[test] releasecmd
	@$(PYTHON) -m pip check

.PHONY: test
test:
	@tox -e py
