Name:           apply-default-acl
Version:        0.4.4
Release:        3%{?dist}.whissi
Summary:        Utility to apply default POSIX ACLs to files and directories

License:        AGPL-3.0-only
URL:            https://michael.orlitzky.com/code/apply-default-acl.xhtml
Source0:        https://michael.orlitzky.com/code/releases/apply-default-acl-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libacl-devel
BuildRequires:  acl

%description
A utility to apply default POSIX ACLs to files and directories.

%package devel
Summary:        Development files for the apply-default-acl library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libacl-devel

%description devel
Headers and linker files for applications using libadacl.


%prep
%autosetup


%build
%configure --disable-static
%make_build


%check
%make_build check


%install
%make_install
find %{buildroot} -name '*.la' -delete


%files
%{_bindir}/%{name}
%{_libdir}/libadacl.so.*
%license doc/LICENSE
%{_mandir}/man1/%{name}.1*
%doc doc/README

%files devel
%{_libdir}/libadacl.so
%{_libdir}/pkgconfig/libadacl.pc
%{_includedir}/libadacl.h


%changelog
* Mon Nov 16 2026 Thomas Deutschmann <whissi@whissi.de> - 0.4.4-2
- Prepare for Whissi Overlay: use SPDX license and split development files
- Disable static libraries and remove libtool archives

* Wed Sep 07 2022 Thomas Deutschmann <whissi@whissi.de> - 0.4.4-1
- Initial version of the package
