%global debug_package %{nil}
Name:           linyaps-web-store-installer
Version:        1.6.6
Release:        1
Summary:        Linyaps web-install helper.
License:        LGPLv3
URL:            https://github.com/OpenAtom-Linyaps/linyaps-web-store-installer
Source0:        linyaps-web-store-installer.zip

BuildRequires:  cmake pkgconf-pkg-config qt5-qtbase-devel
Requires:       linglong-bin

%description
Linyaps web install helper.

%prep
%autosetup -p1 -n linyaps-web-store-installer-%{version}

%define _debugsource_template %{nil}

%build
export PATH=%{_qt5_bindir}:$PATH
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DCMAKE_POSITION_INDEPENDENT_CODE=ON  \
      -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
      -DLIB_INSTALL_DIR:PATH=%{_libdir} \
      -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
      -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
      -DCMAKE_BUILD_TYPE=Release \
      -DQT_VERSION_MAJOR=5 \
      -DCPM_LOCAL_PACKAGES_ONLY=ON ..
%make_build

%files
%{_bindir}/ll-installer
%{_datadir}/applications/*

%install
cd build
%make_install INSTALL_ROOT=%{buildroot}

%changelog
* Wed Jul 23 2025 LFRon <ronforever@qq.com> - 1.6.6-1
- Follow the upstream version 1.6.6-1
- Use Qt5 build as default.

