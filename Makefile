PYTHON := python3

ACTIONLINT_VERSION := v1.6.9
SHELLCHECK_VERSION := v0.8.0

AUTHOR := thombashi
PACKAGE := pytablewriter

DOCS_DIR := docs
BUILD_WORK_DIR := _work
PKG_BUILD_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)

CACHE_VERSION := 0
PKG_CACHE_ROOT_DIR := $(HOME)/.cache/downloaded
PKG_CACHE_DIR := $(PKG_CACHE_ROOT_DIR)/$(CACHE_VERSION)
SHELLCHECK_CACHE_DIR := $(PKG_CACHE_DIR)/shellcheck-$(SHELLCHECK_VERSION)


$(SHELLCHECK_CACHE_DIR):
	@echo "installing shellcheck $(SHELLCHECK_VERSION)"
	@mkdir -p $(SHELLCHECK_CACHE_DIR)
	@curl -sSLf https://github.com/koalaman/shellcheck/releases/download/${SHELLCHECK_VERSION}/shellcheck-${SHELLCHECK_VERSION}.linux.x86_64.tar.xz | tar -xJv -C $(SHELLCHECK_CACHE_DIR) --strip-components 1 --no-anchored shellcheck
	@$(SUDO) mv $(SHELLCHECK_CACHE_DIR)/shellcheck /usr/local/bin/shellcheck
	shellcheck --version

.PHONY: actionlint
actionlint: setup-actionlint
	@actionlint -ignore=SC204 -ignore=SC2086 -ignore=SC2129

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
	@$(MAKE) docs

.PHONY: fmt
fmt:
	@$(PYTHON) -m tox -e fmt

.PHONY: readme
readme:
	@$(PYTHON) -m tox -e readme

.PHONY: release
release:
	cd $(PKG_BUILD_DIR) && $(PYTHON) setup.py release --verbose --search-dir $(PACKAGE)
	$(MAKE) clean

.PHONY: setup-actionlint
setup-actionlint:
	@go install github.com/rhysd/actionlint/cmd/actionlint@${ACTIONLINT_VERSION}
	actionlint --version

.PHONY: setup-ci
setup-ci:
	@$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade tox

.PHONY: setup-shellcheck
setup-shellcheck: $(SHELLCHECK_CACHE_DIR)

.PHONY: setup
setup: setup-actionlint setup-ci setup-shellcheck
	@$(PYTHON) -m pip install --upgrade -q --disable-pip-version-check -e .[test] releasecmd
	@$(PYTHON) -m pip check

.PHONY: test
test:
	@tox --verbose -e py
