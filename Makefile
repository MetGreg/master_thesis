#Makefile for creating master thesis' documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
PACKAGE_FOLDER = python/ModuleSetup/MasterModule
DOCS_FOLDER = docs
DOCS_RST_FOLDER = docs/source/rst

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

.PHONY: docs
docs: 
	sphinx-apidoc -M -f -o $(DOCS_RST_FOLDER) $(PACKAGE_FOLDER)
	cd $(DOCS_FOLDER) && make html

.PHONY: clean
clean: 
	cd $(DOCS_FOLDER) && make clean
