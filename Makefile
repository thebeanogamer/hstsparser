VERSION := $(shell rpmspec -q hstsparser.spec --queryformat='%{version}')
RELEASE := $(shell rpmspec -q hstsparser.spec --queryformat='%{release}')
FEDORARELEASE := 38

tar:
	mkdir -p rpmbuild/SOURCES/
	tar --transform 's,^,hstsparser-$(VERSION)/,' -czvhf rpmbuild/SOURCES/hstsparser-$(VERSION).tar.gz hstsparser.spec pyproject.toml LICENSE hstsparser.py README.md .git

srpm: tar
	rpmbuild -bs --define "_topdir `pwd`/rpmbuild" ./hstsparser.spec
ifdef outdir
	cp ./rpmbuild/SRPMS/* $(outdir)
endif

rpm:
	echo "Native building is deprecated. Use \`make mock\` instead."
	exit 1

mock: srpm
	mock -r fedora-$(FEDORARELEASE)-x86_64 ./rpmbuild/SRPMS/hstsparser-$(VERSION)-$(RELEASE).src.rpm

clean:
	rm -rf rpmbuild fedora-review

fedora-review: clean srpm
	rpm -q fedora-review || sudo dnf install fedora-review -y
	rm -rf review-hstsparser
	cp ./rpmbuild/SRPMS/*.src.rpm .
	fedora-review -n hstsparser
	rm -f *.rpm
