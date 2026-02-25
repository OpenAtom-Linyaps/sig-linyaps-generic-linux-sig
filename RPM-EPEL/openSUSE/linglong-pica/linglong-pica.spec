%global debug_package %{nil}
Name: linglong-pica
Version: 1.2.8
Release: 1
Summary: Linglong Convert tools
License: LGPLv3
URL:     https://github.com/linuxdeepin/linglong-pica
Source0: https://github.com/linuxdeepin/linglong-pica/archive/refs/heads/master.zip

BuildRequires: go clang llvm unzip
Requires: linglong-box
Requires: grep jq ostree python3 python3-pyyaml
Requires: flatpak coreutils zstd

%description
Linglong transform package tools to transform package to linyaps command line tool from AppImage and Flatpak.

%prep
%autosetup -p1 -n linglong-pica-master
%define _debugsource_template %{nil}

%build
make build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%attr(755,root,root) /usr/bin/*
%attr(755,root,root) /usr/libexec/*

%changelog
* Mon Nov 17 2025 LFRon <ronforever@qq.com> - 1.2.8-1
- follow master branch upstream to 1.2.8-1

* Sun Sep 14 2025 LFRon <ronforever@qq.com> - 1.2.6-1
- follow master branch upstream to 1.2.6-1

* Thu Sep 4 2025 LFRon <ronforever@qq.com> - 1.2.4-5
- follow master branch upstream to 1.2.4-5

* Tue Jul 29 2025 LFRon <ronforever@qq.com> - 1.2.4-4
- follow master branch upstream to 1.2.4-4

* Wed Jul 23 2025 LFRon <ronforever@qq.com> - 1.2.4-3
- Bump version to follow upstream update to 1.2.4-3

* Wed Mar 5 2025 LFRon <ronforever@qq.com> - 1.2.4-2
- Bump version to follow upstream update to 1.2.4-2

* Thu Feb 27 2025 LFRon <ronforever@qq.com> - 1.2.4-1
- Initial support for Fedora
- Bump version to 1.2.4-1
