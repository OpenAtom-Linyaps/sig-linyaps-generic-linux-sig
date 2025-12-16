%global debug_package %{nil}
Name:           linglong
Version:        1.10.3
Release:        2
Summary:        Linglong is a Package Manager on Linux.
License:        LGPL v3
URL:            https://gitee.com/LFRon/linyaps-generic-linux
Source0:        https://github.com/LFRon/linyaps-generic-linux/archive/refs/tags/1.10.3-1.zip

BuildRequires:  cmake clang llvm gettext intltool systemd-devel sudo
BuildRequires:  qt5-qtbase-devel qt5-qtbase-private-devel shadow-utils
BuildRequires:  glib2-devel nlohmann-json-devel ostree-devel yaml-cpp-devel libcap-devel
BuildRequires:  gtest-devel libseccomp-devel elfutils-libelf-devel
BuildRequires:  glibc-static libstdc++-static
BuildRequires:  libcurl-devel openssl-devel libcap-devel
BuildRequires:  gtest-devel gmock-devel
Requires:       linglong-bin = %{version}-%{release}
Requires:       desktop-file-utils linglong-box fuse-overlayfs shadow-utils
Requires:       glib2 shared-mime-info systemd
Recommends:    erofs-fuse erofs-utils google-noto-sans-mono-fonts wqy-zenhei-fonts

%description
Linyaps is a secondary package manager on Linux.It could run apps with stable and fast container powered by Linyaps-box on Linux.

%package        -n linglong-bin
Summary:        Linglong package manager
Requires:       linglong-box
%description    -n linglong-bin
Linyaps package management command line tool.

%package        -n linglong-builder
Summary:        Linglong build tools
Requires:       linglong-box linglong-bin = %{version}-%{release} git
%description    -n linglong-builder
This Linyaps sub-package is a tool that makes it easy to build applications and dependencies.

%prep
%autosetup -p1 -n linyaps-generic-linux-%{version}-1

%define _debugsource_template %{nil}

%build
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DCMAKE_POSITION_INDEPENDENT_CODE=ON  \
      -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
      -DLIB_INSTALL_DIR:PATH=%{_libdir} \
      -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
      -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
      -DBUILD_SHARED_LIBS=OFF \
      -DCMAKE_BUILD_TYPE=Release \
      -DCPM_LOCAL_PACKAGES_ONLY=ON \
      -DENABLE_LINGLONG_INSTALLER=ON \
      -DLINGLONG_EXPORT_PATH=apps/share \
      -DCMAKE_C_COMPILER=clang \
      -DCMAKE_CXX_COMPILER=clang++ \
      -DCMAKE_C_FLAGS="-O3 -flto=full" \
      -DCMAKE_CXX_FLAGS="-O3 -flto=full" \
      -DQT_VERSION_MAJOR=5 ..

make

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
%{_datadir}/zsh/*
%{_datadir}/icons/*
%{_datadir}/applications/*
%{_datadir}/locale/*


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
* Tue Dec 16 2025 LFRon <ronforever@qq.com> - 1.10.3-2
- Enable Clang O3+Full-LTO optimization

* Sun Dec 14 2025 LFRon <ronforever@qq.com> - 1.10.3-1
- bump version 1.10.3

* Sat Dec 13 2025 LFRon <ronforever@qq.com> - 1.10.2-7
- feat: improve the control of force-loading extensions and mount-dirs

* Fri Dec 12 2025 LFRon <ronforever@qq.com> - 1.10.2-6
- feat: improve the control of force-loading extensions and mount-dirs
- refactor(utils): improve namespace isolation implementation
- refactor: improve task management code quality and safety

* Sat Dec 6 2025 LFRon <ronforever@qq.com> - 1.10.2-5
- feat: implement the control of force-loading extensions and mount-dirs

* Fri Dec 5 2025 LFRon <ronforever@qq.com> - 1.10.2-3
- fix: Minor fixes
- fix: can't rely on ssi_pid when cross pid_namespaces
- feat: add jmgpu device node to container bind list
- fix: replace unsafe temp-dir creation and fix fmt API usage
- build: add hardend compile/link flags

* Thu Nov 20 2025 LFRon <ronforever@qq.com> - 1.10.2-2
- fix: Minor fixes

* Mon Nov 17 2025 LFRon <ronforever@qq.com> - 1.10.2-1
- fix: Duplicate initialization causes incorrect stderr redirection
- fix: There will be multiple versions of the application when an error occurs during the upgrade process
- fix: base field is empty when use ll-cli search
- fix: fix repo config comparison and add debug logs
- fix: add DBusPrivate to Qt6 find_package
- feat: still implement loading of extensions from config files
- feat: Adding process-aware fileLock implementation
- feat: Disable backtrace by default
- fix: the application was abnormally removed due to an error in executing hooks

* Mon Nov 10 2025 LFRon <ronforever@qq.com> - 1.9.13-9
- feat: Fully support xdg-desktop-portal

* Tue Oct 21 2025 LFRon <ronforever@qq.com> - 1.9.13-8
- feat: Early support for strict sandbox config

* Tue Oct 21 2025 LFRon <ronforever@qq.com> - 1.9.13-7
- feat: Initial support for env config

* Sat Oct 18 2025 LFRon <ronforever@qq.com> - 1.9.13-6
- feat: allow loading extension while appointed base loaded
- fix: some known bugs

* Fri Oct 17 2025 LFRon <ronforever@qq.com> - 1.9.13-5
- feat: change the way of extension loading
- fix: some known bugs

* Wed Oct 15 2025 LFRon <ronforever@qq.com> - 1.9.13-4
- fix: fixing extensions force loading problem
- fix some known bugs
- feat: follow Linyaps-box 2.1.1

* Mon Oct 13 2025 LFRon <ronforever@qq.com> - 1.9.13-3
- feat: allow load multiple extensions
- fix some known bugs

* Sun Oct 12 2025 LFRon <ronforever@qq.com> - 1.9.13-2
- feat: add force load extensions by setting env "LL_FORCE_EXTENSION"
- fix some known bugs

* Sun Sep 28 2025 LFRon <ronforever@qq.com> - 1.9.13-1
- feat: add no-clean-objects option for remove command
- feat: add mirror enable/disable functionality for repositories
- feat: enable git submodule fetching with environment variable control
- refactor: simplify container entrypoint generation
- fix: fix env is cleared by "env -i"
- Follow the upstream release 1.9.13

* Fri Sep 19 2025 LFRon <ronforever@qq.com> - 1.9.12-1
- fix: correct no-dbus flag logic
- Follow the upstream release 1.9.12

* Fri Sep 12 2025 LFRon <ronforever@qq.com> - 1.9.10-2
- fix: build runtime error
- Follow the upstream release 1.9.10-2

* Thu Sep 4 2025 LFRon <ronforever@qq.com> - 1.9.10-1
- fix: runtime dependencies were not being correctly deduplicated
- Follow the upstream release 1.9.10-1

* Tue Jul 29 2025 LFRon <ronforever@qq.com> - 1.9.9-1
- fix AppIndicator issue on low-electron-version apps
- fix media device like USB failed to open in the linyaps apps
- Follow the upstream release 1.9.9-1

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
