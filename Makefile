# Override the upstream tarball for testing
VERSION := $(shell rpmspec -q hstsparser.spec --queryformat='%{version}')

tar:
	mkdir -p rpmbuild/SOURCES/
	tar --exclude='./rpmbuild' --transform 's,^,hstsparser-$(VERSION)/,' -czvhf rpmbuild/SOURCES/$(VERSION).tar.gz .

rpm: tar
	sudo dnf builddep -y hstsparser.spec
	rpmbuild -br --define "_topdir `pwd`/rpmbuild" ./hstsparser.spec
	sudo dnf builddep -y rpmbuild/SRPMS/hstsparser*buildreqs.nosrc.rpm
	rpmbuild -ba --define "_topdir `pwd`/rpmbuild" ./hstsparser.spec