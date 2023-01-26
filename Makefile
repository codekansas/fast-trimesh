# Makefile

define HELP_MESSAGE
			tmesh
			-----

Implementation of some operations on triangular meshes, with C++ and CUDA backends.

Getting Started:
	1. Create a new Conda environment: 'conda create --name tmesh python=3.10'
	2. Activate the environment: 'conda activate tmesh'
	3. Install dependencies: 'make install-conda ; make install-pip'
	4. Build the project: 'make build'

Usage:
	make: Show this help message
	make initialize: Install conda and mamba
	make install-conda: Install conda dependencies
	make format: Format C++ and CMake files

endef
export HELP_MESSAGE

all:
	@echo "$$HELP_MESSAGE"
.PHONY: all

# -----------------
# Conda environment
# -----------------

initialize:
ifeq (, $(shell which mamba))
ifeq (, $(shell which conda))
	$(error Conda is not installed)
else ifeq (, $(CONDA_DEFAULT_ENV))
	$(error Conda not installed or not initialized)
else ifeq (base, $(CONDA_DEFAULT_ENV))
	$(error Don't install this package into the base environment. Run 'conda create --name ml python=3.10' then 'conda activate ml`)
else
	conda install -c conda-forge mamba
endif
endif
.PHONY: initialize

install-conda: initialize
	@mamba install \
		-c conda-forge \
		cmake-format \
		clang-format
.PHONY: install-conda

install-pip: initialize
	@python -m pip install \
		black \
		cmake \
		darglint \
		flake8 \
		isort \
		mypy \
		pybind11 \
		pylint \
		pytest \

install: initialize
	python -m pip install .
.PHONY: install

develop: initialize
	python setup.py develop
.PHONY: develop

# -----
# Build
# -----

build: initialize
	[[ -d build ]] || mkdir build
	cd build && cmake ../src && make -j
	cp build/tmesh.*.so .
	stubgen -p tmesh -o .
.PHONY: build

build-ext-inplace: initialize
	python setup.py build_ext --inplace
.PHONY: build-ext-inplace

# ----------
# Formatting
# ----------

cpp-files := $$(git ls-files '*.c' '*.cpp' '*.h' '*.hpp' '*.cu' '*.cuh')
cmake-files := $$(git ls-files '*/CMakeLists.txt')

format: initialize
	cmake-format -i $(cmake-files)
	clang-format -i $(cpp-files)
.PHONY: format

# -----
# Clean
# -----

clean:
	rm -rf build dist *.so **/*.so **/*.pyi **/*.pyc **/*.pyd **/*.pyo **/__pycache__ *.egg-info .eggs/ tmesh/
.PHONY: clean

# ------------
# Distribution
# ------------

dist: initialize
	python -m build

upload: initialize
	python -m twine upload dist/*
.PHONY: upload

# --------
# Examples
# --------

examples: initialize
	cd examples && make build
.PHONY: examples
