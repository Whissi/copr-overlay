Name:           dracut-networkd-config
Version:        1.0.0
Release:        1%{?dist}.whissi
Summary:        Select systemd-networkd configuration files for the initramfs

License:        GPL-3.0-or-later
URL:            https://github.com/Whissi/dracut-networkd-config
Source0:        https://github.com/Whissi/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires: bash

Requires:      bash
Requires:      coreutils
Requires:      dracut-network
Requires:      findutils
# dracut's systemd-networkd -> net-lib module requires awk even in minimal roots.
Requires:      gawk
Requires:      systemd-networkd

%description
A dracut module that replaces /etc/systemd/network inside the initramfs with
an explicit selection of local .network, .netdev and .link files. This allows
the initramfs to use different network configuration from the running host.

The module is included by normal dracut discovery. By default it requires
/etc/systemd/network/99-dhcp.network; configure networkd_config_files to select
other files, or omit the module using omit_dracutmodules. Missing or invalid
configuration aborts initramfs generation. No host network configuration is
supplied, and package installation does not rebuild existing initramfs images.

%prep
%autosetup

%build
# Shell module; no compilation required.

%install
mkdir -p %{buildroot}%{_prefix}/lib/dracut/modules.d
cp -a 99networkd-config %{buildroot}%{_prefix}/lib/dracut/modules.d/

%check
bash test/check.sh

%files
%license COPYING
%doc README.md example/90-networkd-config.conf
%{_prefix}/lib/dracut/modules.d/99networkd-config/

%changelog
* Sun Nov 22 2026 Thomas Deutschmann <whissi@whissi.de> - 1.0.0-1.whissi
- Package the upstream 1.0.0 GitHub release
- Install the complete module directory and run the upstream local checks

* Sat Nov 21 2026 Thomas Deutschmann <whissi@whissi.de> - 0.9.0-1.whissi
- Initial package for networkd-config
- Run the supplied module tests and ship configuration documentation
- Require gawk for dracut's net-lib dependency in minimal runtime installations
