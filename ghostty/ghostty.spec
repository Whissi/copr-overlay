%global project_id com.mitchellh.ghostty
%global simdutf_version 9.4.0

# Upstream release signing key.
%global pubkey RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV

Name:           ghostty
Version:        1.4.0
Release:        4%{?dist}.whissi
Summary:        Fast, feature-rich terminal emulator
License:        MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND GPL-2.0-or-later AND GPL-3.0-or-later AND LGPL-2.1-only AND MPL-2.0 AND OFL-1.1 AND Unicode-3.0 AND (WTFPL OR CC0-1.0)
URL:            https://ghostty.org

Source0:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
Source1:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz.minisig
# Source-only replacement of the upstream bundled simdutf; no system ABI change.
Source3:        https://github.com/simdutf/simdutf/releases/download/v%{simdutf_version}/simdutf.cpp#/simdutf-%{simdutf_version}.cpp
Source4:        https://github.com/simdutf/simdutf/releases/download/v%{simdutf_version}/simdutf.h#/simdutf-%{simdutf_version}.h
Source5:        https://raw.githubusercontent.com/simdutf/simdutf/v%{simdutf_version}/LICENSE-MIT#/simdutf-%{simdutf_version}-MIT-LICENSE
Source6:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt#/GPL-2.0-or-later.txt
Source7:        collect-licenses.py
Source8:        sources.sha256

# Ghostty dependency archives, including themes and fonts.
# aro
Source100:      https://codeberg.org/ziglang/arocc/archive/d0c8c4d9c55daa7ef6e40cf0f630a5b5e900989b.tar.gz#/aro-d0c8c4d9c55daa7ef6e40cf0f630a5b5e900989b.tar.gz
# bindings
Source101:      https://deps.files.ghostty.org/DearBindings_v0.17_ImGui_v1.92.5-docking.tar.gz
# glslang
Source102:      https://deps.files.ghostty.org/glslang-12201278a1a05c0ce0b6eb6026c65cd3e9247aa041b1c260324bf29cee559dd23ba1.tar.gz
# gobject
Source103:      https://deps.files.ghostty.org/gobject-2026-10-02-38-1.tar.zst
# imgui
Source104:      https://deps.files.ghostty.org/N-V-__8AAEbOfQBnvcFcCX2W5z7tDaN8vaNZGamEQtNOe0UI.tar.gz
# iterm2_themes
Source105:      https://deps.files.ghostty.org/ghostty-themes-release-20261019-151001-86a776d.tgz
# jetbrains_mono
Source106:      https://deps.files.ghostty.org/JetBrainsMono-2.304.tar.gz
# libxev
Source107:      https://deps.files.ghostty.org/libxev-819ffa180ca20e31c7eded74e2e1aceb1eab557f.tar.gz
# nerd_fonts_symbols_only
Source108:      https://deps.files.ghostty.org/NerdFontsSymbolsOnly-3.4.0.tar.gz
# pixels
Source109:      https://deps.files.ghostty.org/pixels-12207ff340169c7d40c570b4b6a97db614fe47e0d83b5801a932dcd44917424c8806.tar.gz
# plasma_wayland_protocols
Source110:      https://deps.files.ghostty.org/plasma_wayland_protocols-12207e0851c12acdeee0991e893e0132fc87bb763969a585dc16ecca33e88334c566.tar.gz
# translate_c
Source111:      https://deps.files.ghostty.org/translate_c-02ff0c523fb92a38939b04d0145c4a9602a74d56.tar.gz
# uucode
Source112:      https://deps.files.ghostty.org/uucode-ea62149739404a73c202b48a33bf6dd2af4bd9b0.tar.gz
# vaxis
Source113:      https://deps.files.ghostty.org/vaxis-6fd944a27fb3d6f596e981076381a3131f2448b4.tar.gz
# wayland
Source114:      https://deps.files.ghostty.org/wayland-9cb3d7aa9dc995ffafdbdef7ab86a949d0fb0e7d.tar.gz
# wayland_protocols
Source115:      https://deps.files.ghostty.org/N-V-__8AAFdWDwA0ktbNUi9pFBHCRN4weXIgIfCrVjfGxqgA.tar.gz
# wayland_protocols
Source116:      https://deps.files.ghostty.org/wayland-protocols-258d8f88f2c8c25a830c6316f87d23ce1a0f12d9.tar.gz
# wuffs
Source117:      https://deps.files.ghostty.org/wuffs-7411f488fe2e2c205c3d3b3d28638b7356522930.tar.gz
# z2d
Source118:      https://deps.files.ghostty.org/z2d-40af3e84a4e15a9f31d126b3f281f23ce6a3dae5.tar.gz
# zf
Source119:      https://deps.files.ghostty.org/zf-87153bb86b75d21fbac897b738f316d449f5d0c9.tar.gz
# zig_wayland
Source120:      https://deps.files.ghostty.org/zig_wayland-27dda01712ddf3cb46ebd93380d88b01a7c828f8.tar.gz
# zigimg
Source121:      https://github.com/sergot/zigimg/archive/c701c9f99779d7ddf594dcc6da8f858fd277d61f.tar.gz#/zigimg-c701c9f99779d7ddf594dcc6da8f858fd277d61f.tar.gz

Patch0:         ghostty-1.4.0-bzip2-dependency.patch
# Upstream fix: app builds must not install the separate libghostty-vt SDK.
# This also avoids shipping the broken DESTDIR-containing .pc files described
# in scottames/copr commit dc4a1fa80e46ca1b84e21316f217db2794663fac.
Patch1:         ghostty-1.4.0-libghostty-install-a-CMake-package-config-and-fix-li.patch

ExclusiveArch:  x86_64
BuildRequires:  (zig >= 0.17.1 with zig < 0.18.0~)
BuildRequires:  zig-rpm-macros
BuildRequires:  pkgconf-pkg-config
BuildRequires:  minisign
BuildRequires:  pandoc
BuildRequires:  blueprint-compiler
BuildRequires:  gettext
BuildRequires:  ncurses
BuildRequires:  desktop-file-utils
BuildRequires:  systemd-rpm-macros
BuildRequires:  python3
BuildRequires:  hostname
BuildRequires:  valgrind
BuildRequires:  bzip2-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig) >= 2.18.3
# freetype2.pc uses a different version scheme from the upstream release.
BuildRequires:  freetype-devel >= 2.13.2
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(harfbuzz) >= 11.0.0
BuildRequires:  pkgconfig(libpng) >= 1.6.43
BuildRequires:  pkgconfig(zlib) >= 1.3.1
BuildRequires:  pkgconfig(oniguruma) >= 6.9.9
BuildRequires:  pkgconfig(gtk4-layer-shell-0) >= 1.1.0
BuildRequires:  pkgconfig(libhwy) >= 1.2.0
BuildRequires:  SPIRV-Cross-devel >= 1.4.363.0
BuildRequires:  pkgconfig(spirv-cross-c-shared)
BuildRequires:  pkgconfig(gtk4) >= 4.18
BuildRequires:  pkgconfig(libadwaita-1) >= 1.7

Requires:       %{name}-terminfo = %{version}-%{release}
Requires:       hicolor-icon-theme
Requires:       vim-filesystem
Requires:       dbus-common
%{?systemd_ordering}
# GTK's GL dispatch loads libGLESv2.so.2 dynamically during application startup.
Requires:       libglvnd-gles%{?_isa}
# SONAME requirements alone do not express our minimum source-library versions.
Requires:       fontconfig%{?_isa} >= 2.18.3
Requires:       freetype%{?_isa} >= 2.13.2
Requires:       harfbuzz%{?_isa} >= 11.0.0
Requires:       libpng%{?_isa} >= 1.6.43
Requires:       zlib%{?_isa} >= 1.3.1
Requires:       oniguruma%{?_isa} >= 6.9.9
Requires:       gtk4-layer-shell%{?_isa} >= 1.1.0
Requires:       highway%{?_isa} >= 1.2.0
Requires:       SPIRV-Cross-libs%{?_isa} >= 1.4.363.0
Provides:       bundled(simdutf) = %{simdutf_version}
# Fedora ships glslang only as GCC-built static archives; use Ghostty's source
# copy with Zig's C++ toolchain, as agreed.
Provides:       bundled(glslang) = 14.2.0
Provides:       bundled(imgui) = 1.92.5
Provides:       bundled(dearbindings) = 0.17
Provides:       bundled(wuffs) = 0~git7411f488fe2e2c205c3d3b3d28638b7356522930
Provides:       bundled(libxev) = 0~git819ffa180ca20e31c7eded74e2e1aceb1eab557f
Provides:       bundled(libvaxis) = 0.6.0
Provides:       bundled(z2d) = 0.13.0
Provides:       bundled(zf) = 0.11.0
Provides:       bundled(zigimg) = 0.1.0
Provides:       bundled(uucode) = 0.2.0
Provides:       bundled(ghostty-gobject) = 0.3.2
Provides:       bundled(zig-wayland) = 0.7.0~dev
Provides:       bundled(font(JetBrainsMonoNoNF)) = 2.304
Provides:       bundled(font(NerdFontSymbolsOnly)) = 3.4.0

%description
Ghostty is a terminal emulator with GPU rendering, native GTK integration,
shell integration, and support for modern terminal protocols.

%package terminfo
Summary:        Terminal description for Ghostty
License:        MIT
BuildArch:      noarch
Requires:       ncurses-base
# Block monolithic packages which own this file, while permitting split builds.
Conflicts:      (%{_datadir}/terminfo/x/xterm-ghostty without ghostty-terminfo)

%description terminfo
The xterm-ghostty terminal description for applications using terminfo.
Install this package on remote hosts accessed from Ghostty.

# Shared Zig options for preparation, build, installation and tests.
%global _zig_release_mode fast
%global _zig_system_integration --system "%{_builddir}/%{buildsubdir}/zig-pkg"
%global _zig_install_options --prefix "%{_prefix}" --prefix-lib-dir "%{_lib}"
%global ghostty_options %{shrink: \
    -Demit-lib-vt=false -Dfont-backend=fontconfig_freetype \
    -Drenderer=opengl -Dsentry=false -Dsimd=true -Dgtk-x11=true -Dgtk-wayland=true \
    -Di18n=true -Demit-docs=true -Dstrip=false -Dversion-string=%{version} \
    -Dinstalled-exe-path=%{_bindir}/ghostty -Demit-themes=true \
    -Demit-terminfo=true -Demit-termcap=true \
    -fsys=fontconfig -fsys=freetype -fsys=harfbuzz -fsys=libpng -fsys=zlib \
    -fsys=oniguruma -fno-sys=glslang -fsys=spirv-cross -fsys=gtk4-layer-shell \
    -fsys=highway -fno-sys=simdutf \
}

%prep
(cd "%{_sourcedir}" && sha256sum --check "%{SOURCE8}")
minisign -Vm %{SOURCE0} -x %{SOURCE1} -P %{pubkey}
%autosetup -p1
# Populate Zig's package directory from local SRPM sources; no network access.
mkdir -p zig-pkg zig-fetch
cp build.zig zig-fetch/
while read -r archive expected; do
    cp build.zig.zon zig-fetch/
    (cd zig-fetch && ZIG_GLOBAL_CACHE_DIR="$PWD/../zig-fetch-cache" \
        zig fetch --save=rpmbuild --pkg-dir "$PWD/../zig-pkg" "$archive")
    test -d "zig-pkg/$expected"
done <<'ZIG_SOURCES'
%{SOURCE100} aro-0.0.0-JSD1QtuBNwCASyBtNF3pqTl_W3oAJQGEVyFAtrBSE_Pa
%{SOURCE101} N-V-__8AANT61wB--nJ95Gj_ctmzAtcjloZ__hRqNw5lC1Kr
%{SOURCE102} N-V-__8AABzkUgISeKGgXAzgtutgJsZc0-kkeqBBscJgMkvy
%{SOURCE103} gobject-0.3.2-Skun7LuIogBbEh-6WrLeEzMaRCnOMB3eOf__RaPYSMCZ
%{SOURCE104} N-V-__8AAEbOfQBnvcFcCX2W5z7tDaN8vaNZGamEQtNOe0UI
%{SOURCE105} N-V-__8AAJ3vBQAq1fLMh5J8uWLkeDLS6WAdR2x5KcrmEyz6
%{SOURCE106} N-V-__8AAIC5lwAVPJJzxnCAahSvZTIlG-HhtOvnM1uh-66x
%{SOURCE107} libxev-0.0.0-86vtc8QQFACz0sVc7U-VDiDIgH-XfBuEY5JpABLjHNpn
%{SOURCE108} N-V-__8AAMVLTABmYkLqhZPLXnMl-KyN38R8UVYqGrxqO26s
%{SOURCE109} N-V-__8AADYiAAB_80AWnH1AxXC0tql9thT-R-DYO1gBqTLc
%{SOURCE110} N-V-__8AAKYZBAB-CFHBKs3u4JkeiT4BMvyHu3Y5aaWF3Bbs
%{SOURCE111} translate_c-2.0.0-Q_BUWltOBwBYABF84EUL208pIFeUIwbBs29FmVBaafN5
%{SOURCE112} uucode-0.2.0-ZZjBPoGFVgCiflJNFc6Io8xzC67B6PA5bUkk4LT0kCxg
%{SOURCE113} vaxis-0.6.0-BWNV_MafDAAEzkVUvrW9NFUqnnMUoeHqrs2mecnD6D7w
%{SOURCE114} N-V-__8AAKrHGAAs2shYq8UkE6bGcR1QJtLTyOE_lcosMn6t
%{SOURCE115} N-V-__8AAFdWDwA0ktbNUi9pFBHCRN4weXIgIfCrVjfGxqgA
%{SOURCE116} N-V-__8AAKw-DAAaV8bOAAGqA0-oD7o-HNIlPFYKRXSPT03S
%{SOURCE117} N-V-__8AAP5JWgCGP_AD0teWpa4krRvE9VPZzvviGdbmN4jI
%{SOURCE118} z2d-0.13.0-j5P_HgsRFABzZDH54gI35P0OSrg7HFyJwS2bXX5uBdU4
%{SOURCE119} zf-0.11.0-OIRy8XCRAAB6FiMwIrtD6FqlagnFwpI6YyOu7bXeYH5J
%{SOURCE120} wayland-0.7.0-dev-lQa1klz9AQB87V0pMKMdm8JvyOx32XR9FxcWnw9wh6XZ
%{SOURCE121} zigimg-0.1.0-8_eo2ri_FwBqF5UYiggLz4IGjHJO_n9-B6gT9Ayqg8G4
ZIG_SOURCES
rm -rf zig-fetch zig-fetch-cache
# Empty placeholders keep Zig from fetching disabled/system library packages.
# Require a complete match with the dependency inventory in the release archive.
python3 - <<'PYTHON'
import json
from pathlib import Path
manifest = json.loads(Path('build.zig.zon.json').read_text())
omitted = set('breakpad fontconfig freetype gettext gtk4_layer_shell harfbuzz highway libpng libxml2 oniguruma sentry spirv_cross zlib zig_js zig_objc'.split())
packages = Path('zig-pkg')
for package_hash, dependency in manifest.items():
    if dependency['name'] in omitted:
        (packages / package_hash).mkdir()
actual = {entry.name for entry in packages.iterdir()}
if actual != set(manifest):
    raise SystemExit(f'Zig source inventory mismatch: missing={set(manifest) - actual}, extra={actual - set(manifest)}')
PYTHON
cp -p %{SOURCE3} pkg/simdutf/vendor/simdutf.cpp
cp -p %{SOURCE4} pkg/simdutf/vendor/simdutf.h
cp -p %{SOURCE5} simdutf-MIT-LICENSE
cp -p %{SOURCE6} GPL-2.0-or-later.txt
# RPM flattens individual license paths; retain both upstream LICENSE files.
cp -p vendor/nerd-fonts/LICENSE nerd-fonts-LICENSE
# This manifest field is metadata only, but keep it accurate as well.
sed -i 's/\.version = "5.2.8"/.version = "%{simdutf_version}"/' pkg/simdutf/build.zig.zon
grep -F '#define SIMDUTF_VERSION "%{simdutf_version}"' pkg/simdutf/vendor/simdutf.h
python3 %{SOURCE7}
%zig_prep

%build
%zig_build %{ghostty_options} -Dapp-runtime=gtk

%install
%zig_install %{ghostty_options} -Dapp-runtime=gtk
# Fedora's ncurses-term already supplies the compatibility alias.
rm %{buildroot}%{_datadir}/terminfo/g/ghostty
# Source descriptions belong in the independently installable terminfo package.
install -d %{buildroot}%{_docdir}/%{name}-terminfo
mv %{buildroot}%{_datadir}/terminfo/ghostty.{terminfo,termcap} \
    %{buildroot}%{_docdir}/%{name}-terminfo/
%find_lang %{project_id}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{project_id}.desktop
%{buildroot}%{_bindir}/ghostty --version
TERMINFO=%{buildroot}%{_datadir}/terminfo infocmp -x xterm-ghostty >/dev/null
# Upstream requires Debug assertions for the unit tests; no graphical session.
%zig_test %{ghostty_options} -Doptimize=debug -Dapp-runtime=none

%post
%systemd_user_post app-%{project_id}.service

%preun
%systemd_user_preun app-%{project_id}.service

%postun
%systemd_user_postun app-%{project_id}.service

%files -f %{project_id}.lang
%license LICENSE simdutf-MIT-LICENSE GPL-2.0-or-later.txt src/font/res/OFL.txt nerd-fonts-LICENSE bundled-licenses
%doc README.md
%{_bindir}/ghostty
%{_datadir}/ghostty/
%{_datadir}/applications/%{project_id}.desktop
%{_datadir}/metainfo/%{project_id}.metainfo.xml
%{_userunitdir}/app-%{project_id}.service
%{_datadir}/dbus-1/services/%{project_id}.service
%dir %{_datadir}/icons/hicolor/1024x1024
%dir %{_datadir}/icons/hicolor/1024x1024/apps
%{_datadir}/icons/hicolor/*/apps/%{project_id}.png
%{_mandir}/man1/ghostty.1*
%{_mandir}/man5/ghostty.5*
%{_datadir}/bash-completion/completions/ghostty.bash
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/zsh/site-functions/_ghostty
%dir %{_datadir}/bat
%dir %{_datadir}/bat/syntaxes
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax
%dir %{_datadir}/nvim
%dir %{_datadir}/nvim/site
%dir %{_datadir}/nvim/site/compiler
%dir %{_datadir}/nvim/site/ftdetect
%dir %{_datadir}/nvim/site/ftplugin
%dir %{_datadir}/nvim/site/syntax
%{_datadir}/nvim/site/*/ghostty.vim
%{_datadir}/vim/vimfiles/*/ghostty.vim
%dir %{_datadir}/nautilus-python
%dir %{_datadir}/nautilus-python/extensions
%{_datadir}/nautilus-python/extensions/ghostty.py
%dir %{_datadir}/kio
%dir %{_datadir}/kio/servicemenus
%{_datadir}/kio/servicemenus/%{project_id}.desktop

%files terminfo
%license LICENSE
%{_datadir}/terminfo/x/xterm-ghostty
%doc %{_docdir}/%{name}-terminfo/

%changelog
* Sun Nov 22 2026 Thomas Deutschmann <whissi@whissi.de> - 1.4.0-4.whissi
- Own integration and icon directories and require the Vim directory layout
- Require the directory owners for D-Bus activation and standalone terminfo
- Handle user service installation and removal without restarting terminals on upgrade

* Sun Nov 22 2026 Thomas Deutschmann <whissi@whissi.de> - 1.4.0-3.whissi
- Include individual upstream dependency archives in the source RPM
- Prepare and verify dependency sources offline during the package build

* Mon Nov 16 2026 Thomas Deutschmann <whissi@whissi.de> - 1.4.0-2.whissi
- Require the dynamically loaded OpenGL ES runtime for graphical startup

* Mon Nov 16 2026 Thomas Deutschmann <whissi@whissi.de> - 1.4.0-1.whissi
- Package Ghostty and an independently installable terminfo subpackage
- Prefer system libraries at least as new as the bundled sources
- Bundle simdutf 9.4.0 without replacing Fedora's incompatible system ABI
- Bundle upstream glslang sources for a consistent C++ build toolchain
- Preserve upstream themes and resources; build offline from verified sources
