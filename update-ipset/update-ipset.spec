Name:           update-ipset
Version:        1.0.0
Release:        2%{?dist}.whissi
Summary:        Atomically replace ipsets from blocklist or allowlist files

License:        GPL-3.0-or-later
URL:            https://github.com/Whissi/update-ipset
Source0:        https://github.com/Whissi/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
# Full license text from https://www.gnu.org/licenses/gpl-3.0.txt
Source1:        COPYING

BuildArch:      noarch

Requires:       bash
Requires:       coreutils
Requires:       findutils
Requires:       gawk
Requires:       ipset
Requires:       util-linux-core

%description
Update an ipset from a directory of blocklist or allowlist files. Supports
hash:ip and hash:net sets for IPv4 and IPv6. Input is loaded into a private
temporary set before atomically replacing the target, preserving its existing
contents if preparing or loading the update fails.

%prep
%autosetup
cp -p %{SOURCE1} COPYING

%build
# Bash script; no compilation required.

%install
install -Dpm 0755 update-ipset %{buildroot}%{_sbindir}/update-ipset

# The upstream integration suite requires root and a private network namespace.

%files
%license COPYING
%doc README.md
%{_sbindir}/update-ipset

%changelog
* Wed Nov 25 2026 Thomas Deutschmann <whissi@whissi.de> - 1.0.0-2.whissi
- Remove downstream lint and smoke checks and their build dependencies

* Tue Nov 24 2026 Thomas Deutschmann <whissi@whissi.de> - 1.0.0-1.whissi
- Initial package
