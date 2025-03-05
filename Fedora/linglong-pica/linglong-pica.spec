%global debug_package %{nil}
Name: linglong-pica
Version: 1.2.4.2
Release: 1
Summary: Linglong Convert tools
License: LGPLv3
URL:     https://github.com/linuxdeepin/linglong-pica
Source0: linglong-pica.zip

BuildRequires:golang
Requires:linglong-box
Requires:grep jq ostree python3 python3-pyyaml
Requires:flatpak coreutils zstd

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
* Wed Mar 5 2025 LFRon <ronforever@qq.com> - 1.2.4-2
- Bump version to follow upstream update to 1.2.4-2

* Thu Feb 27 2025 LFRon <ronforever@qq.com> - 1.2.4-1
- Initial support for Fedora
- Bump version to 1.2.4-1
