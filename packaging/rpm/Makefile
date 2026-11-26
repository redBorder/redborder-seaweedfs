PACKAGE_NAME?=  redborder-seaweedfs

VERSION?= $(shell git describe --abbrev=6 --tags HEAD --always | sed 's/-/_/g')

BUILD_NUMBER?= 1

MOCK_CONFIG?=default

RESULT_DIR?=pkgs

# SeaweedFS source release. To upgrade, change WEED_VERSION here and weed_version in the
# spec, and WEED_SHA256 with the sha256sum of the new tarball
WEED_VERSION?= 4.55
WEED_SHA256?= 725282228d39edc4327bbba4e4a31867660cafbec6adb5f43005ba3e3960d25c
WEED_TARBALL= seaweedfs-$(WEED_VERSION).tar.gz
WEED_URL= https://github.com/seaweedfs/seaweedfs/archive/refs/tags/$(WEED_VERSION).tar.gz

all: rpm


SOURCES:
	mkdir -p SOURCES

archive: SOURCES
	cd ../../ && \
	git archive --prefix=$(PACKAGE_NAME)-$(VERSION)/ \
            -o packaging/rpm/SOURCES/$(PACKAGE_NAME)-$(VERSION).tar.gz HEAD

# Download the SeaweedFS source once and check it against the pinned sha256
weed_source: SOURCES
	@if [ ! -f SOURCES/$(WEED_TARBALL) ]; then \
		curl -fsSL -o SOURCES/$(WEED_TARBALL).tmp $(WEED_URL) && \
		mv SOURCES/$(WEED_TARBALL).tmp SOURCES/$(WEED_TARBALL); \
	fi
	@echo "$(WEED_SHA256)  SOURCES/$(WEED_TARBALL)" | sha256sum -c - || \
		{ echo "ERROR: SOURCES/$(WEED_TARBALL) does not match the pinned sha256"; rm -f SOURCES/$(WEED_TARBALL); exit 1; }

build_prepare: archive weed_source
	mkdir -p $(RESULT_DIR)
	rm -f $(RESULT_DIR)/$(PACKAGE_NAME)*.rpm


srpm: build_prepare
	/usr/bin/mock \
            -r $(MOCK_CONFIG) \
            --define "__version $(VERSION)" \
            --define "__release $(BUILD_NUMBER)" \
            --resultdir=$(RESULT_DIR) \
            --buildsrpm \
            --spec=${PACKAGE_NAME}.spec \
            --sources=SOURCES
	@echo "======= Source RPM now available in $(RESULT_DIR) ======="

rpm: srpm
	/usr/bin/mock \
            -r $(MOCK_CONFIG) \
            --define "__version $(VERSION)"\
            --define "__release $(BUILD_NUMBER)"\
            --resultdir=$(RESULT_DIR) \
            --rebuild $(RESULT_DIR)/$(PACKAGE_NAME)*.src.rpm
	@echo "======= Binary RPMs now available in $(RESULT_DIR) ======="

clean:
	rm -rf SOURCES pkgs

distclean: clean
	rm -f build.log root.log state.log available_pkgs installed_pkgs \
            *.rpm *.tar.gz
