%global debug_package %{nil}
Name:           linglong
Version:        1.9.9
Release:        1
Summary:        Linglong is a Package Manager on Linux.
License:        LGPLv3
URL:            https://github.com/linuxdeepin/%{name}
Source0:        linyaps.zip

BuildRequires:  cmake gcc-c++ linglong-box
BuildRequires:  qt6-qtbase-devel qt-devel qt6-qtbase-private-devel
BuildRequires:  glib2-devel nlohmann-json-devel ostree-devel yaml-cpp-devel
BuildRequires:  systemd-devel gtest-devel libseccomp-devel elfutils-libelf-devel
BuildRequires:  glibc-static libstdc++-static
BuildRequires:  libcurl-devel openssl-devel libcap-devel
BuildRequires:  gtest-devel gmock-devel
Requires:       linglong-bin = %{version}-%{release}
Requires:       desktop-file-utils erofs-fuse linglong-box
Requires:       glib2 shared-mime-info erofs-utils
Requires:       google-noto-sans-mono-fonts wqy-zenhei-fonts wqy-microhei-fonts

%description
Linyaps is a secondary package manager on Linux.It could run apps with stable and fast container powered by Linyaps-box on Linux.

%package        -n linglong-bin
Summary:        Linglong package manager
Requires:       linglong-box google-noto-sans-mono-fonts wqy-zenhei-fonts wqy-microhei-fonts
%description    -n linglong-bin
Linyaps package management command line tool.

%package        -n linglong-builder
Summary:        Linglong build tools
Requires:       linglong-box linglong-bin = %{version}-%{release} git
%description    -n linglong-builder
This Linyaps sub-package is a tool that makes it easy to build applications and dependencies.

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
      -DCPM_LOCAL_PACKAGES_ONLY=ON \
      -DENABLE_LINGLONG_INSTALLER=ON \
      -DLINGLONG_EXPORT_PATH=apps/share \
      -DQT_VERSION_MAJOR=6 \
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
%{_libexecdir}/%{name}/ll-init
%{_libexecdir}/%{name}/dialog/99-linglong-permission
%{_datadir}/bash-completion/completions/ll-cli
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/polkit-1/actions/org.deepin.linglong.PackageManager1.policy
%{_datadir}/%{name}/config.yaml
%{_datadir}/%{name}/export-dirs.json
%{_datadir}/mime/packages/*
%{_datadir}/locale/*
%{_datadir}/zsh/*
%{_datadir}/applications/*


%files -n linglong-builder
%{_bindir}/ll-builder
%{_libexecdir}/%{name}/fetch-dsc-source
%{_libexecdir}/%{name}/fetch-git-source
%{_libexecdir}/%{name}/fetch-file-source
%{_libexecdir}/%{name}/fetch-archive-source
%{_libexecdir}/%{name}/app-conf-generator
%{_libexecdir}/%{name}/builder/helper/*.sh
%{_datadir}/bash-completion/completions/ll-builder
%{_datadir}/%{name}/builder/templates/*.yaml
%{_datadir}/%{name}/builder/uab/*


%changelog
* Tue Jul 29 2025 LFRon <ronforever@qq.com> - 1.9.9-1
- fix AppIndicator issue on low-electron-version apps.
- Follow the upstream release 1.9.8

* Sat Jul 5 2025 chenhuixing <chenhuixing@deepin.org> - 1.9.4-1
- Follow the upstream version 1.9.4-1

* Wed Jun 25 2025 chenhuixing <chenhuixing@deepin.org> - 1.9.0-1
- Follow the upstream version 1.9.0-1

* Sat Jun 14 2025 chenhuixing <chenhuixing@deepin.org> - 1.8.5-1
- Follow the upstream version 1.8.5-1

* Fri May 16 2025 chenhuixing <chenhuixing@deepin.org> - 1.8.3-1
- Follow the upstream version 1.8.3-1

* Thu Apr 24 2025 chenhuixing <chenhuixing@deepin.org> - 1.8.1-1
- Follow the upstream version 1.8.1-1

* Sat Apr 5 2025 LFRon <ronforever@qq.com> - 1.8.0-1
- Bump version to 1.8.0-1
- fix: correct path deduplication while fixmount by @ComixHe in #1079
- fix: adjust container mount items by @myml in #1085
- fix: fix compiler error by @reddevillg in #1084
- fix: skip whiteout files by @reddevillg in #1083
- fix: fix unshare error by @reddevillg in #1082
- fix: exporting systemd service may cause system error by @myml in #1081
- fix: version comparison error by @ice909 in #1087
- fix: ll-builder build failed by @ice909 in #1091
- fix: failed to umount layer dir by @dengbo11 in #1088
- feat: add share/templates dir to whitelist by @dengbo11 in #1090
- chore: adjust the builder output format by @ice909 in #1095
- fix: compatible with qt 5.11 by @ComixHe in #1094
- feat: support don't export the develop module by @ice909 in #1097
- feat: support Qt6 packaging by @dengbo11 in #1096

* Fri Mar 28 2025 LFRon <ronforever@qq.com> - 1.7.11-1
- Bump version to 1.7.11-1

* Thu Mar 6 2025 chenhuixing <chenhuixing@deepin.org> - 1.7.8-2
- Bump version to 1.7.8-2
- fix missing environment variable

* Wed Mar 5 2025 chenhuixing <chenhuixing@deepin.org> - 1.7.8-1
- Bump version to 1.7.8-1
- Fix known bugs

* Thu Apr 25 2024 chenhuixing <chenhuixing@deepin.org> - 1.7.5-1
- Bump version to 1.7.5-1
- Initial support for Fedora
