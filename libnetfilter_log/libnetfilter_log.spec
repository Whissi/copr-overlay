Name:           libnetfilter_log
Version:        1.0.2
Release:        2%{?dist}.whissi
Summary:        Netfilter logging userspace library
License:        GPL-2.0-only
URL:            https://www.netfilter.org/projects/libnetfilter_log/
Source0:        https://ftp.netfilter.org/pub/%{name}/%{name}-%{version}.tar.bz2
# Retain Fedora's use of the current kernel UAPI header.
Patch0:         libnetfilter_log-sysheader.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-headers
BuildRequires:  pkgconfig(libnfnetlink) >= 1.0.0
BuildRequires:  pkgconfig(libmnl) >= 1.0.3

%description
Userspace library for receiving packets logged by the Netfilter NFLOG target.

%package devel
Summary:        Development files for libnetfilter_log
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kernel-headers

%description devel
Headers and development libraries for applications using libnetfilter_log.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-man-pages --disable-html-doc
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license COPYING
%{_libdir}/libnetfilter_log.so.1*
%{_libdir}/libnetfilter_log_libipulog.so.1*

%files devel
%{_includedir}/libnetfilter_log/
%{_libdir}/libnetfilter_log.so
%{_libdir}/libnetfilter_log_libipulog.so
%{_libdir}/pkgconfig/libnetfilter_log*.pc

%changelog
* Mon Nov 16 2026 Thomas Deutschmann <whissi@whissi.de> - 1.0.2-1
- Update Fedora's packaging to 1.0.2 for ulogd's NFLOG input
- Preserve the libipulog compatibility library and kernel UAPI headers
