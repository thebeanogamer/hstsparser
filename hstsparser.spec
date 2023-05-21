Name:           hstsparser
Version:        1.1.6
Release:        1%{?dist}
Summary:        HSTS Digital Forensics parser

License:        MIT
URL:            https://github.com/thebeanogamer/hstsparser
Source:         %{url}/archive/refs/tags/%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%description Parse Firefox and Chrome HSTS databases into Digital Forensics artifacts

%prep
%autosetup -p1 -n hstsparser-%{version}


%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel


%install
%pyproject_install


%pyproject_save_files hstsparser


%check
%tox

%files -f %{pyproject_files}
%doc README.md
%{_bindir}/hstsparser

%changelog
%autochangelog
