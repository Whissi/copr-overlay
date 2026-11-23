# architecture and toolchain

%if 0%{?rhel}
# Zig depends on a C compiler (gcc) during bootstrapping.
# Older versions of gcc fail to compile the transpiled source, so limit to x86_64.
%global         zig_arches x86_64
%else
# Supported architectures: https://ziglang.org/download/VERSION/release-notes.html#Support-Table
%global         zig_arches x86_64 aarch64 riscv64 %{mips64}
%endif

# GCC < 16.0 miscompiles on RISC-V; use Clang instead on older Fedora versions
%ifarch riscv64
%if 0%{?fedora} < 44
%bcond toolchain_clang 1
%endif
%endif

%if %{with toolchain_clang}
%global toolchain clang
%endif

# minisign public key for source verification (from https://ziglang.org/download/)
%global         public_key RWSGOq2NVecA2UPNdBUZykf1CCb147pkmdtYxgb3Ti+JO/wCYvhbAb/U


# dependency versions and cache

# Compatible LLVM/Clang version definitions
%if 0%{?fedora} >= 44 || 0%{?rhel} >= 11 || (0%{?rhel} == 10 && "%{?distcore}" != ".el10_2" && "%{?dist}" != ".el10_2")
%global         llvm_compat 22
%endif
%global         llvm_version 22.1.8

%global zig_cache_dir %{_vpath_builddir}/zig-cache


# build conditionals

# Enable with --with bootstrap when no packaged Zig 0.17 compiler is available.
# stage1/zig1.wasm is the upstream seed for Fedora's CMake bootstrap path.
%bcond bootstrap 0
%bcond docs      1
%bcond macro     1
%bcond test      1


# build and install options

%global zig_build_options %{shrink: \
    --verbose \
    --release=fast \
    --summary all \
    \
    -Dtarget=native \
    -Dcpu=baseline \
    --build-id=sha1 \
    \
    --cache-dir "%{zig_cache_dir}" \
    \
    -Dversion-string="%{?dev_version}%{!?dev_version:%{version}}" \
    -Dstatic-llvm=false \
    -Denable-llvm=true \
    -Dno-langref=true \
    -Dstd-docs=false \
    -Dpie \
    -Dconfig_h="%{__cmake_builddir}/config.h" \
}

%global zig_install_options %{shrink: \
    %zig_build_options \
    --prefix "%{_prefix}" \
}

Name:           zig
Version:        0.17.1
Release:        2%{?dist}.whissi
Summary:        Programming language for maintaining robust, optimal, and reusable software

# The minisign file references a specific archive name so we store for ease of use
%global         archive_name %{name}-%{version}.tar.xz

License:        MIT AND NCSA AND LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0 AND GPL-2.0-or-later AND GPL-2.0-or-later WITH GCC-exception-2.0 AND BSD-3-Clause AND Inner-Net-2.0 AND ISC AND LicenseRef-Fedora-Public-Domain AND GFDL-1.1-or-later AND ZPL-2.1
URL:            https://ziglang.org
Source0:        %{url}/download/%{version}/%{archive_name}
Source1:        %{url}/download/%{version}/%{archive_name}.minisig
Source2:        macros.%{name}

# Remove native lib directories from rpath
# this is unlikely to be upstreamed in its current state because upstream
# wants to work around the shortcomings of NixOS
Patch0:         0001-remove-native-lib-directories-from-rpath.patch

# LLVM on RHEL/EPEL only provides fewer targets so we patch the required targets down
# Targets come from https://src.fedoraproject.org/rpms/llvm/blob/rawhide/f/llvm.spec
Patch1:         0002-Remove-unsupported-LLVM-targets-for-EPEL.patch

%if %{without toolchain_clang}
BuildRequires:  gcc
BuildRequires:  gcc-c++
%else
BuildRequires:  clang
%endif
BuildRequires:  cmake
BuildRequires:  llvm%{?llvm_compat}-devel
BuildRequires:  clang%{?llvm_compat}-devel
BuildRequires:  lld%{?llvm_compat}-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
# for man page generation
BuildRequires:  help2man
# for signature verification
BuildRequires:  minisign

%if %{without bootstrap}
BuildRequires:  (zig >= 0.17 with zig < 0.18)
%endif

%if %{with test}
# for testing
BuildRequires:  elfutils-libelf-devel
BuildRequires:  libstdc++-static
%endif

Requires:       %{name}-libs = %{version}

# These packages are bundled as source

# Apache-2.0 WITH LLVM-exception OR NCSA OR MIT
Provides: bundled(compiler-rt) = %{llvm_version}
# LGPL-2.1-or-later AND SunPro AND LGPL-2.1-or-later WITH GCC-exception-2.0 AND BSD-3-Clause AND GPL-2.0-or-later AND LGPL-2.1-or-later WITH GNU-compiler-exception AND GPL-2.0-only AND ISC AND LicenseRef-Fedora-Public-Domain AND HPND AND CMU-Mach AND LGPL-2.0-or-later AND Unicode-3.0 AND GFDL-1.1-or-later AND GPL-1.0-or-later AND FSFUL AND MIT AND Inner-Net-2.0 AND X11 AND GPL-2.0-or-later WITH GCC-exception-2.0 AND GFDL-1.3-only AND GFDL-1.1-only
Provides: bundled(glibc) = 2.44
# Apache-2.0 WITH LLVM-exception OR MIT OR NCSA
Provides: bundled(libcxx) = %{llvm_version}
# Apache-2.0 WITH LLVM-exception OR MIT OR NCSA
Provides: bundled(libcxxabi) = %{llvm_version}
# NCSA
Provides: bundled(libunwind) = %{llvm_version}
# BSD, LGPG, ZPL
Provides: bundled(mingw) = 31bd54ab7d5fe03c67ed2bb1a57e531b9c7f8cc4
# MIT
Provides: bundled(musl) = 1.2.5
# Apache-2.0 WITH LLVM-exception AND Apache-2.0 AND MIT AND BSD-2-Clause
Provides: bundled(wasi-libc) = c89896107d7b57aef69dcadede47409ee4f702ee

ExclusiveArch: %{zig_arches}

%description
Zig is an open-source programming language designed for robustness, optimality,
and clarity. This package provides the zig compiler and the associated runtime.

# The Zig stdlib only contains uncompiled code
%package libs
Summary:        %{name} Standard Library
BuildArch:      noarch

%description libs
%{name} Standard Library

%if %{with docs}
%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}

%description doc
Documentation for %{name}. For more information, visit %{url}
%endif

%if %{with macro}
%package        rpm-macros
Summary:        Common RPM macros for %{name}
Requires:       rpm
BuildArch:      noarch

%description    rpm-macros
This package contains common RPM macros for %{name}.
%endif

%prep
minisign -V -m %{SOURCE0} -x %{SOURCE1} -P %{public_key} -Q | grep -F "file:%{archive_name}"

%autosetup -N
%patch 0 -p1
%if 0%{?rhel}
%patch 1 -p1
%endif

%if %{without bootstrap}
# Ensure that the pre-build stage1 binary is not used
rm -f stage1/zig1.wasm
%endif

%build

# Fedora supports using ccache systemwide
# Zig generates a large C file for bootstrapping which does not
# behave well with ccache so we explicitly disable it.
export CCACHE_DISABLE=1

# zig doesn't know how to dynamically link llvm on its own so we need cmake to generate a header ahead of time
# if we provide the header we need to also build zigcpp

# C_FLAGS: wasm2c output generates a lot of noise with -Wunused.
# EXTRA_BUILD_ARGS: explicitly specify a build-id
# Bootstrap C seed compilers are temporary; omit their enormous debug data.
%cmake \
    -DCMAKE_C_FLAGS:STRING="%{build_cflags} -g0" \
    -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
    -DCMAKE_C_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG -Wno-unused" \
    -DCMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG -Wno-unused" \
    \
    -DZIG_EXTRA_BUILD_ARGS:STRING="--verbose;--build-id=sha1;-Dno-langref=true;-Dstd-docs=false" \
    -DZIG_SHARED_LLVM:BOOL=true \
    -DZIG_PIE:BOOL=true \
    \
    -DZIG_TARGET_MCPU:STRING=baseline \
    -DZIG_TARGET_TRIPLE:STRING=native \
    \
    -DZIG_VERSION:STRING="%{?dev_version}%{!?dev_version:%{version}}"

%if %{with bootstrap}
%cmake_build --target stage3
%else
%cmake_build --target zigcpp
ZIG_GLOBAL_CACHE_DIR="$PWD/%{zig_cache_dir}" zig build --zig-lib=lib %{zig_build_options}
%endif

%if %{with bootstrap}
%global built_zig %{__cmake_builddir}/stage3/bin/zig
%else
%global built_zig ./zig-out/bin/zig
%endif

# Zig has no official manpage
# https://github.com/ziglang/zig/issues/715
help2man --no-discard-stderr --no-info "%{built_zig}" --version-option=version --output=zig.1


%if %{with docs}
# Use the newly made stage 3 compiler to generate docs
ZIG_GLOBAL_CACHE_DIR="$PWD/%{zig_cache_dir}" %{built_zig} build --zig-lib=lib docs %{zig_build_options}
%endif

%install
%if %{with bootstrap}
%cmake_install
%if 0%{?rhel}
rm -rf %{buildroot}%{_prefix}/doc
%endif
%else
DESTDIR="%{buildroot}" ZIG_GLOBAL_CACHE_DIR="$PWD/%{zig_cache_dir}" zig build --zig-lib=lib install %{zig_install_options}
%endif

install -D -pv -m 0644 -t %{buildroot}%{_mandir}/man1/ zig.1


%if %{with macro}
install -D -pv -m 0644 %{SOURCE2} %{buildroot}%{_rpmmacrodir}/macros.%{name}
%endif

%if %{with test}
%check
# Run reduced set of tests, based on the Zig CI
"%{buildroot}%{_bindir}/zig" test test/behavior.zig -Itest
%endif

%files
%license LICENSE
%{_bindir}/zig
%{_mandir}/man1/%{name}.1.*

%files libs
%license LICENSE
%{_prefix}/lib/%{name}

%if %{with docs}
%files doc
%doc README.md
%doc zig-out/doc/langref.html
%doc zig-out/doc/std
%endif

%if %{with macro}
%files rpm-macros
%license LICENSE
%{_rpmmacrodir}/macros.%{name}
%endif

%changelog
* Sun Nov 22 2026 Thomas Deutschmann <whissi@whissi.de> - 0.17.1-2.whissi
- Include the project license in independently installable library and RPM macro packages

* Mon Nov 16 2026 Thomas Deutschmann <whissi@whissi.de> - 0.17.1-1.whissi
- Update Fedora Rawhide packaging to Zig 0.17.1 with LLVM 22
- Bootstrap using Fedora's existing CMake path; retain docs and RPM macros
- Refresh Fedora's native library RPATH patch for Zig 0.17
- Update bundled source version metadata from the Zig 0.17 release notes
- Point the RPM build macros at Zig 0.17's package cache
- Omit debug data for the temporary C bootstrap seed compilers
- Use Zig 0.17's build-command library path option
