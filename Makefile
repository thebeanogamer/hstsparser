# Override the upstream tarball for testing
VERSION := $(shell rpmspec -q hstsparser.spec --queryformat='%{version}')

tar:
	mkdir -p rpmbuild/SOURCES/
	tar --exclude='./rpmbuild' --transform 's,^,hstsparser-$(VERSION)/,' -czvhf rpmbuild/SOURCES/$(VERSION).tar.gz .

rpm: tar
	sudo dnf builddep -y hstsparser.spec
	rpmbuild -ba ./hstsparser.spec