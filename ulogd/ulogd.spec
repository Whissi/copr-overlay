Name:           ulogd
Version:        2.0.9
Release:        3%{?dist}.whissi
Summary:        Userspace logging daemon for Netfilter
License:        GPL-2.0-only AND GPL-2.0-or-later
URL:            https://www.netfilter.org/projects/ulogd/
Source0:        https://ftp.netfilter.org/pub/%{name}/%{name}-%{version}.tar.xz
Source1:        ulogd.service
Source2:        ulogd.conf
Source3:        ulogd.logrotate
Source4:        README.Fedora
Source5:        sqlite-packets.sql
Patch0:         ulogd-pgsql-no-oids.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libnfnetlink) >= 1.0.2
BuildRequires:  pkgconfig(libnetfilter_log) >= 1.0.2
BuildRequires:  pkgconfig(libnetfilter_conntrack) >= 1.1.0
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  mariadb-connector-c-devel
BuildRequires:  pkgconfig(libpq)
BuildRequires:  systemd-rpm-macros
Requires:       logrotate
# Match upstream's minimum version; the SONAME alone does not encode it.
Requires:       libnetfilter_log%{?_isa} >= 1.0.2
%{?systemd_requires}

%description
ulogd receives Netfilter packet and connection tracking events and writes them
to configurable outputs. This package includes NFLOG and NFCT inputs, text
outputs, a default NFLOG-to-file configuration, and a systemd service.
Database outputs are available as optional subpackages.

%package sqlite
Summary:        SQLite output plugin for ulogd
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description sqlite
SQLite output plugin and an example packet schema for ulogd.

%package mysql
Summary:        MySQL and MariaDB output plugin for ulogd
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description mysql
MySQL-compatible output plugin for ulogd, built with the MariaDB client library.
Example database schemas are included. A database server is not installed.

%package pgsql
Summary:        PostgreSQL output plugin for ulogd
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description pgsql
PostgreSQL output plugin and example database schemas for ulogd.
A database server is not installed.

%prep
%autosetup -p1
cp %{SOURCE4} README.Fedora
cp %{SOURCE5} doc/sqlite-packets.sql

%build
%configure --with-ulogd2libdir=%{_libdir}/ulogd \
    --enable-nflog --enable-nfct --disable-nfacct \
    --enable-sqlite3 --enable-mysql --with-mysql-config=%{_bindir}/mariadb_config \
    --enable-pgsql --disable-dbi --disable-pcap --disable-json
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/ulogd.service
sed -i 's|@SBINDIR@|%{_sbindir}|g' %{buildroot}%{_unitdir}/ulogd.service
install -Dpm 0600 %{SOURCE2} %{buildroot}%{_sysconfdir}/ulogd.conf
sed -i 's|@LIBDIR@|%{_libdir}|g' %{buildroot}%{_sysconfdir}/ulogd.conf
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/ulogd
install -dm 0750 %{buildroot}%{_localstatedir}/log/ulogd

%check
%make_build check
./src/ulogd --version
# Resolve each module's shared libraries and exported plugin metadata.
for plugin in $(find input filter output -name '*.so'); do
    # --info itself returns success even if dlopen fails; require metadata.
    ./src/ulogd --info "$plugin" > plugin-info.txt
    grep '^Name: ' plugin-info.txt || exit 1
done

%post
%systemd_post ulogd.service

%preun
%systemd_preun ulogd.service

%postun
%systemd_postun_with_restart ulogd.service

%files
%license COPYING
%doc README README.Fedora ulogd.conf
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/ulogd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/ulogd
%{_sbindir}/ulogd
%{_unitdir}/ulogd.service
%{_mandir}/man8/ulogd.8*
%dir %attr(0750,root,root) %{_localstatedir}/log/ulogd
%dir %{_libdir}/ulogd
%{_libdir}/ulogd/ulogd_inp*.so
%{_libdir}/ulogd/ulogd_filter_*.so
%{_libdir}/ulogd/ulogd_raw2packet_BASE.so
%{_libdir}/ulogd/ulogd_output_LOGEMU.so
%{_libdir}/ulogd/ulogd_output_SYSLOG.so
%{_libdir}/ulogd/ulogd_output_OPRINT.so
%{_libdir}/ulogd/ulogd_output_GPRINT.so
%{_libdir}/ulogd/ulogd_output_NACCT.so
%{_libdir}/ulogd/ulogd_output_XML.so
%{_libdir}/ulogd/ulogd_output_GRAPHITE.so
%{_libdir}/ulogd/ulogd_output_IPFIX.so

%files sqlite
%doc doc/sqlite3.table doc/sqlite-packets.sql
%{_libdir}/ulogd/ulogd_output_SQLITE3.so

%files mysql
%doc doc/mysql-ulogd2.sql doc/mysql-ulogd2-flat.sql
%{_libdir}/ulogd/ulogd_output_MYSQL.so

%files pgsql
%doc doc/pgsql-ulogd2.sql doc/pgsql-ulogd2-flat.sql
%{_libdir}/ulogd/ulogd_output_PGSQL.so

%changelog
* Mon Nov 23 2026 Thomas Deutschmann <whissi@whissi.de> - 2.0.9-3.whissi
- Rebuild from Git-managed packaging sources

* Mon Nov 16 2026 Thomas Deutschmann <whissi@whissi.de> - 2.0.9-1
- Package ulogd with a systemd service and NFLOG text output
- Split SQLite, MySQL/MariaDB and PostgreSQL outputs into optional subpackages
- Remove obsolete OIDS table options from PostgreSQL schema examples
