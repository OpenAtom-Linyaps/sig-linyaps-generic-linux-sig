%define debug_package %{nil}
%define _enable_debug_package 0
Name:           linyaps-web-store-installer
Version:        1.6.8
Release:        2
Summary:        linyaps web store installer
License:        GPL-3.0-or-later
URL:            https://gitee.com/LFRon/linyaps-web-store-installer
Source0:        https://github.com/OpenAtom-Linyaps/linyaps-web-store-installer/archive/refs/tags/1.6.8.zip

BuildRequires:  cmake
BuildRequires:  clang llvm llvm-devel
BuildRequires:  pkgconfig
BuildRequires:  qt5-qtbase-devel
BuildRequires:  xdg-utils

Requires:       linglong-bin
Requires:       xdg-utils

%description
linglong-installer is a package installer for the linglong web store.
It provides a GUI interface for installing applications from the linglong
ecosystem with OCI standard support.

%prep
%autosetup -p1 -n linyaps-web-store-installer-%{version}

%build
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DQT_VERSION_MAJOR=5 \
      -DCMAKE_C_COMPILER=clang \
      -DCMAKE_CXX_COMPILER=clang++ \
      -DCMAKE_C_FLAGS="-O3 -flto=full" \
      -DCMAKE_CXX_FLAGS="-O3 -flto=full" \
      -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
      -DCMAKE_BUILD_TYPE=Release ..

make -j$(nproc)

%install
DESTDIR=%{buildroot} cmake --install build

%post
xdg-mime default space.linglong.Installer.desktop x-scheme-handler/og

%files
%license LICENSE
%doc README.md README_zh_CN.md
%{_bindir}/ll-installer
%{_datadir}/applications/space.linglong.Installer.desktop

%changelog
* Tue Dec 16 2025 LFRon <ronforever@qq.com> - 1.6.8-2
- Enable Clang O3+Full-LTO optimization

* Thu Sep 4 2025 LFRon <ronforever@qq.com> - 1.6.8-1
- update follow upstream 1.6.8-1
- compile using Qt5 as default

* Wed Apr 02 2025 dengbo <dengbo@deepin.org> - 1.6.6-1
- feat: support Qt6 packaging
- update follow upstream 1.6.6-1

* Thu Nov 24 2022 huqinghong <huqinghong@uniontech.com> - 1.3.3.7-1
- update version for deepin.

* Tue Aug 09 2022 huqinghong <huqinghong@uniontech.com> - 1.3.3.6-1
- fix display of QPlainTextEdit.

* Mon Aug 01 2022 liujianqiang <liujianqiang@uniontech.com> - 1.3.3.5-1
- update version for deepin.

* Mon Jul 25 2022 liujianqiang <liujianqiang@uniontech.com> - 1.3.3-1
- update version and add depends xdg-utils.

* Wed Dec 08 2021 liujianqiang <liujianqiang@uniontech.com> - 1.0.0-1
- Init package.
