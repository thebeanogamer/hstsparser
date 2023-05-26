# Override the upstream tarball for testing
VERSION := $(shell rpmspec -q hstsparser.spec --queryformat='%{version}')

tar:
	mkdir -p rpmbuild/SOURCES/
	tar --exclude='./rpmbuild' --transform 's,^,hstsparser-$(VERSION)/,' -czvhf rpmbuild/SOURCES/$(VERSION).tar.gz .

srpm: tar
	rpmbuild -bs --define "_topdir `pwd`/rpmbuild" ./hstsparser.spec
ifdef outdir
	cp ./rpmbuild/SRPMS/* $(outdir)
endif

rpm: tar
	sudo dnf install -y python3-poetry
	sudo dnf builddep -y hstsparser.spec
	rpmbuild -br --define "_topdir `pwd`/rpmbuild" ./hstsparser.spec
	sudo dnf builddep -y rpmbuild/SRPMS/hstsparser*buildreqs.nosrc.rpm
	rpmbuild -br --define "_topdir `pwd`/rpmbuild" ./hstsparser.spec
	sudo dnf builddep -y rpmbuild/SRPMS/hstsparser*buildreqs.nosrc.rpm
	rpmbuild -ba --define "_topdir `pwd`/rpmbuild" ./hstsparser.spec

mock: srpm
	mock -r fedora-38-x86_64 .//rpmbuild/SRPMS/hstsparser-$(VERSION)-1.fc38.src.rpm
