Name:           hstsparser
Version:        1.2.0
Release:        %autorelease
Summary:        HSTS Digital Forensics parser
License:        MIT
URL:            https://github.com/thebeanogamer/hstsparser
Source:         %{url}/archive/%{version}/hstsparser-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  help2man

%py_provides python3-hstsparser


%description
Parse Firefox and Chrome HSTS databases into Digital Forensics artifacts.


%prep
%autosetup -p1 -n hstsparser-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

# Fix command name in manpage
ln -s hstsparser.py hstsparser
# hstsparser finds the version number by checking the installed package
# The package isn't installed during the RPM build, so we override the version number on the man page with the one from the RPM
help2man -N ./hstsparser -o hstsparser.1 --version-string='%{version}'
rm -f hstsparser


%install
%pyproject_install
%pyproject_save_files hstsparser
mkdir -p %{buildroot}%{_mandir}/man1/
install -pm 0644 hstsparser.1 %{buildroot}%{_mandir}/man1/hstsparser.1


%check
%pyproject_check_import


%files -f %{pyproject_files}
%doc README.md
%license LICENSE
%{_bindir}/hstsparser
%{_mandir}/man1/hstsparser.1*


%changelog
%autochangelog
