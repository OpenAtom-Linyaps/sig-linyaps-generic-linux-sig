%global debug_package %{nil}
Name:           linglong
Version:        1.7.8
Release:        1
Summary:        Linglong is a Package Manager on Linux.
License:        LGPLv3
URL:            https://github.com/linuxdeepin/%{name}
Source0:        linyaps.zip

BuildRequires:  cmake gcc-c++
BuildRequires:  qt5-qtbase-devel qt5-qtbase-private-devel
BuildRequires:  glib2-devel nlohmann-json-devel ostree-devel yaml-cpp-devel
BuildRequires:  systemd-devel gtest-devel libseccomp-devel elfutils-libelf-devel
BuildRequires:  glibc-static libstdc++-static
BuildRequires:  libcurl-devel openssl-devel libcap-devel
BuildRequires:  gtest-devel gmock-devel
Requires:       linglong-bin = %{version}-%{release}
Requires:       desktop-file-utils erofs-fuse
Requires:       glib2 shared-mime-info erofs-utils
Requires:       google-noto-sans-mono-fonts wqy-zenhei-fonts wqy-microhei-fonts

%description
Linyaps is a secondary package manager on Linux.It could run apps with a stable container on Linux.

%package        -n linglong-bin
Summary:        Linglong package manager
Requires:       linglong-box = %{version}-%{release} google-noto-sans-mono-fonts wqy-zenhei-fonts wqy-microhei-fonts    
%description    -n linglong-bin
Linglong package management command line tool.

%package        -n linglong-builder
Summary:        Linglong build tools
Requires:       linglong-box = %{version}-%{release} linglong-bin = %{version}-%{release}
%description    -n linglong-builder
This package is a tool that makes it easy to build applications and dependencies.

%package        -n linglong-box
Summary:        Linglong sandbox
Requires:       desktop-file-utils erofs-fuse fuse-overlayfs
Requires:       glib2 shared-mime-info erofs-utils
%description    -n linglong-box
Linglong sandbox with OCI standard.

%prep
%autosetup -p1 -n linyaps-%{version}-1

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
      -DBUILD_SHARED_LIBS=OFF \
      -DCPM_LOCAL_PACKAGES_ONLY=ON ..
%make_build

%install
cd build
%make_install INSTALL_ROOT=%{buildroot}

%post -n linglong-bin
%systemd_post org.deepin.linglong.PackageManager.service

%preun -n linglong-bin
%systemd_preun org.deepin.linglong.PackageManager.service

%postun -n linglong-bin
%systemd_postun_with_restart org.deepin.linglong.PackageManager.service

%files
%doc README.md
%license LICENSE
%exclude %{_libdir}/cmake/linglong-*/*.cmake

%files -n linglong-bin
%doc README.md
%license LICENSE
%{_sysconfdir}/profile.d/*
%{_sysconfdir}/X11/Xsession.d/*
%{_bindir}/ll-cli
%{_bindir}/llpkg
%{_prefix}/lib/%{name}/container/*
%{_prefix}/lib/%{name}/generate-xdg-data-dirs.sh
%{_prefix}/lib/sysusers.d/*.conf
%{_prefix}/lib/tmpfiles.d/*.conf
%{_prefix}/lib/systemd/system/*.service
%{_prefix}/lib/systemd/system-preset/*.preset
%{_prefix}/lib/systemd/user/*
%{_prefix}/lib/systemd/system-environment-generators/*
%{_prefix}/lib/systemd/user-generators/*
%{_libexecdir}/%{name}/ll-package-manager
%{_libexecdir}/%{name}/ll-session-helper
%{_libexecdir}/%{name}/ld-cache-generator
%{_libexecdir}/%{name}/font-cache-generator
%{_libexecdir}/%{name}/ll-dialog
%{_libexecdir}/%{name}/dialog/99-linglong-permission
%{_datadir}/bash-completion/completions/ll-cli
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/polkit-1/actions/org.deepin.linglong.PackageManager1.policy
%{_datadir}/%{name}/config.yaml
%{_datadir}/mime/packages/*
%{_datadir}/locale/*
/usr/share/zsh/*

%files -n linglong-builder
%license LICENSE
%{_bindir}/ll-builder
%{_libexecdir}/%{name}/fetch-dsc-source
%{_libexecdir}/%{name}/fetch-git-source
%{_libexecdir}/%{name}/fetch-file-source
%{_libexecdir}/%{name}/fetch-archive-source
%{_libexecdir}/%{name}/app-conf-generator
%{_libexecdir}/%{name}/builder/helper/*.sh
%{_datadir}/bash-completion/completions/ll-builder
%{_datadir}/%{name}/builder/templates/*.yaml
/usr/share/linglong/builder/uab/*

%files -n linglong-box
%license LICENSE
%{_bindir}/ll-box

%changelog
* Thu Mar 6 2025 chenhuixing <chenhuixing@deepin.org> - 1.7.8-2
- Bump version to 1.7.8-2
- fix missing environment variable

* Wed Mar 5 2025 chenhuixing <chenhuixing@deepin.org> - 1.7.8-1
- Bump version to 1.7.8-1
- Fix known bugs

* Thu Apr 25 2024 chenhuixing <chenhuixing@deepin.org> - 1.7.5-1
- Bump version to 1.7.5-1
- Initial support for Fedora
