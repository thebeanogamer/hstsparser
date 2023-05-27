# Override the upstream tarball for testing
VERSION := $(shell rpmspec -q hstsparser.spec --queryformat='%{version}')

tar:
	mkdir -p rpmbuild/SOURCES/
	tar --exclude='./rpmbuild' --exclude='./review-hstsparser' --transform 's,^,hstsparser-$(VERSION)/,' -czvhf rpmbuild/SOURCES/hstsparser-$(VERSION).tar.gz .

srpm: tar
	rpmbuild -bs --define "_topdir `pwd`/rpmbuild" ./hstsparser.spec
ifdef outdir
	cp ./rpmbuild/SRPMS/* $(outdir)
endif

rpm: tar
	sudo dnf builddep --setopt=install_weak_deps=False -y hstsparser.spec
	# rpmbuild -bd returns 1 even though it's doing what we asked for
	rpmbuild -bd --define "_topdir `pwd`/rpmbuild" ./hstsparser.spec || true
	ls -d rpmbuild/SRPMS/* | grep buildreqs | xargs -r sudo dnf builddep --setopt=install_weak_deps=False -y
	rpmbuild -ba --define "_topdir `pwd`/rpmbuild" ./hstsparser.spec

mock: srpm
	mock -r fedora-38-x86_64 ./rpmbuild/SRPMS/hstsparser-$(VERSION)-1.fc38.src.rpm

clean:
	rm -rf rpmbuild

fakeci:
	podman run -tv .:/repo:z fedora:38 sh -c "dnf install rpmdevtools rpm-build make tar dnf-plugins-core -y && cd /repo && make rpm"

fedora-review: clean srpm
	rm -rf review-hstsparser
	cp ./rpmbuild/SRPMS/*.src.rpm .
	fedora-review -n hstsparser
	rm -f *.rpm
