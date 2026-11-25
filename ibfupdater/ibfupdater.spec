Name:           ibfupdater
Version:        1.0.1
Release:        1%{?dist}.whissi
Summary:        Update downloaded files with HTTP caching and versioned backups

License:        GPL-3.0-or-later
URL:            https://github.com/Whissi/ibfupdater
Source0:        https://github.com/Whissi/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
# Full license text from https://www.gnu.org/licenses/gpl-3.0.txt
Source1:        COPYING

BuildArch:      noarch
BuildRequires:  bash >= 4.2
BuildRequires:  coreutils
BuildRequires:  curl
BuildRequires:  diffutils
BuildRequires:  gawk
BuildRequires:  python3
BuildRequires:  util-linux-core

Requires:       bash >= 4.2
Requires:       coreutils
Requires:       curl
Requires:       diffutils
Requires:       gawk
Requires:       util-linux-core

%description
The Intelligent Background File Updater downloads a file and replaces it only
when its contents change. HTTP cache validation with ETag or Last-Modified
avoids unnecessary downloads. Optional versioned backups preserve earlier
contents, and locking serializes updates to the same output file.

%prep
%autosetup
cp -p %{SOURCE1} COPYING

%build
# Bash script; no compilation required.

%install
install -Dpm 0755 ibfupdater %{buildroot}%{_bindir}/ibfupdater

%check
python3 tests/integration.py -v

%files
%license COPYING
%doc README.md
%{_bindir}/ibfupdater

%changelog
* Wed Nov 25 2026 Thomas Deutschmann <whissi@whissi.de> - 1.0.1-1.whissi
- Update to 1.0.1

* Tue Nov 24 2026 Thomas Deutschmann <whissi@whissi.de> - 1.0.0-1.whissi
- Initial package
