Name:           hstsparser
Version:        1.1.7
Release:        1%{?dist}
Summary:        HSTS Digital Forensics parser
Group:          Applications/Engineering

License:        MIT
URL:            https://github.com/thebeanogamer/hstsparser
Source:         %{url}/archive/refs/tags/%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(poetry)
BuildRequires:  python3dist(tox-current-env)
BuildRequires:  help2man

%description %{expand:
Parse Firefox and Chrome HSTS databases into Digital Forensics artifacts}

%prep
%autosetup -p1 -n hstsparser-%{version}


%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files hstsparser
mkdir -p %{buildroot}%{_mandir}/man1/

# Fix command name in manpage
ln -s hstsparser.py hstsparser

# This runs outside the venv, so --version will return the default
help2man -N ./hstsparser -o %{buildroot}%{_mandir}/man1/hstsparser.1 --version-string='%{version}'
rm -f hstsparser

%check
%tox

%files -f %{pyproject_files}
%doc README.md
%{_bindir}/hstsparser
%{_mandir}/man1/hstsparser.1*

%changelog
%autochangelog
