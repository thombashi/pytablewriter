AUTHOR := thombashi
PACKAGE := pytablewriter
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build
BUILD_WORK_DIR := _work
PKG_BUILD_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)


.PHONY: build-remote
build-remote:
	@rm -rf $(BUILD_WORK_DIR)
	@mkdir -p $(BUILD_WORK_DIR)
	@cd $(BUILD_WORK_DIR) && \
		git clone https://github.com/$(AUTHOR)/$(PACKAGE).git --depth 1 && \
		cd $(PACKAGE) && \
		tox -e build
	ls -lh $(PKG_BUILD_DIR)/dist/*

.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@tox -e lint

.PHONY: clean
clean:
	@rm -rf $(BUILD_WORK_DIR)
	@tox -e clean

.PHONY: docs
docs:
	@tox -e docs

.PHONY: idocs
idocs:
	@python3 -m pip install --upgrade .
	@make docs

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: readme
readme:
	@cd $(DOCS_DIR) && tox -e readme

.PHONY: release
release:
	@cd $(PKG_BUILD_DIR) && python setup.py release --sign
	@make clean

.PHONY: setup
setup:
	@python3 -m pip install --upgrade -e .[test] releasecmd tox
	python3 -m pip check
