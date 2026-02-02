%global debug_package %{nil}
Name:           linglong
Version:        1.11.1
Release:        2
Summary:        Linglong package manager for Linux
License:        LGPL v3
URL:            https://gitee.com/LFRon/linyaps-generic-linux
Source0:        https://github.com/LFRon/linyaps-generic-linux/archive/refs/tags/1.11.1-2.zip

# ========== BuildRequires ==========
BuildRequires:  cmake gcc-c++ gettext intltool systemd-devel sudo unzip libuuid-devel
BuildRequires:  glibc-devel glibc-devel-static

# 处理Qt编译版本, OpenSUSE风滚草使用Qt6编译
# 反之使用Qt5编译
%if 0%{?suse_version} > 1600
%define distro_use_qt_ver 6
BuildRequires:  qt6-base-devel
%else
%define distro_use_qt_ver 5
BuildRequires:  libqt5-qtbase-devel
%endif

BuildRequires:  clang llvm llvm-devel pkgconf-pkg-config
BuildRequires:  glib2-devel nlohmann_json-devel ostree-devel yaml-cpp-devel libcap-devel
BuildRequires:  gtest gmock
BuildRequires:  libseccomp-devel libelf-devel
BuildRequires:  libcurl-devel openssl-devel unzip

# ========== Runtime Requires ==========
Requires:       linglong-bin = %{version}-%{release}
Requires:       desktop-file-utils linglong-box fuse-overlayfs

# shadow 在 SUSE，shadow-utils 在其他
Requires:       shadow libuuid1
Requires:       glib2 shared-mime-info systemd
Requires:       google-noto-sans-mono-fonts wqy-zenhei-fonts
Recommends:     erofs-fuse erofs-utils

%description
Linyaps is a secondary package manager on Linux.It could run apps with stable and fast container powered by Linyaps-box on Linux.

%package        -n linglong-bin
Summary:        Linglong package manager
%if 0%{?suse_version}
Requires:       linglong-box google-noto-sans-mono-fonts wqy-zenhei-fonts shadow
%else
Requires:       linglong-box google-noto-sans-mono-fonts wqy-zenhei-fonts shadow-utils
%endif
%description    -n linglong-bin
Linyaps package management command line tool.

%package        -n linglong-builder
Summary:        Linglong build tools
Requires:       linglong-box linglong-bin = %{version}-%{release} git
%description    -n linglong-builder
This Linyaps sub-package is a tool that makes it easy to build applications and dependencies.

%prep
%autosetup -p1 -n linyaps-generic-linux-%{version}-%{release}

%define _debugsource_template %{nil}

%build
echo "INFO: 当前OpenSUSE版本号为: %{?suse_version}"
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
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_C_COMPILER=clang \
      -DCMAKE_CXX_COMPILER=clang++ \
      -DCMAKE_C_FLAGS="-O3 -flto=full" \
      -DCMAKE_CXX_FLAGS="-O3 -flto=full" \
      -DQT_VERSION_MAJOR=%{distro_use_qt_ver} ..

make -j$(nproc)

%install
cd build
%make_install INSTALL_ROOT=%{buildroot}

# ========== systemd / tmpfiles 宏 ==========
%if 0%{?suse_version}
%pre -n linglong-bin
%service_add_pre org.deepin.linglong.PackageManager.service

%post -n linglong-bin
%service_add_post org.deepin.linglong.PackageManager.service
%tmpfiles_create %{_tmpfilesdir}/linglong.conf

%preun -n linglong-bin
%service_del_preun org.deepin.linglong.PackageManager.service

%postun -n linglong-bin
%service_del_postun org.deepin.linglong.PackageManager.service
%else
%pre -n linglong-bin
%service_add_pre org.deepin.linglong.PackageManager.service

%post -n linglong-bin
%systemd_post org.deepin.linglong.PackageManager.service
%tmpfiles_create %{_tmpfilesdir}/linglong.conf

%preun -n linglong-bin
%systemd_preun org.deepin.linglong.PackageManager.service

%postun -n linglong-bin
%systemd_postun_with_restart org.deepin.linglong.PackageManager.service
%endif

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
%{_libexecdir}/%{name}/ll-driver-detect
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
* Sat Jan 31 2026 LFRon <ronforever@qq.com> - 1.11.1-2
- feat: Improve NVIDIA Linux driver passthrough
- fix: Do not unbind host rootfs as default
- revert: tray icon rewrite

* Tue Jan 27 2026 LFRon <ronforever@qq.com> - 1.11.1-1
- feat: Follow 1.11.1 update upstream
- feat: Improve the tray icon loader
- feat: Improve NVIDIA Linux driver passthrough

* Sun Jan 18 2026 LFRon <ronforever@qq.com> - 1.11.0-3
- fix: Known issues
- fix: follow extension config by upstream

* Sat Jan 17 2026 LFRon <ronforever@qq.com> - 1.11.0-2
- fix: Linyaps Apps cannot passthrough IPC system

* Fri Jan 16 2026 LFRon <ronforever@qq.com> - 1.11.0-1
- fix: NVIDIA driver fallback cause ll-builder cannot work
- feat: Follow extension force-load by upstream
- bump version 1.11.0-1

* Thu Jan 15 2026 LFRon <ronforever@qq.com> - 1.10.4-1
- Merge extension loading policy from upstream
- Fix ll-builder cannot work

* Tue Dec 23 2025 Packager <ronforever@qq.com> - 1.10.3-2
- Add Clang+LLVM support for OpenSUSE

* Sat Nov 08 2025 Packager <you@example.com> - 1.9.13-2
- Adapt spec for openSUSE Leap 15.6:
- switch shadow-utils -> shadow on SUSE
- drop glibc-static/libstdc++-static on SUSE
- use libqt5-qtbase-devel and systemd service macros on SUSE
- replace hard-coded systemd paths with macros
- force C++17 with gcc-12 toolchain and dynamic glibc link
- pass SUSE hardening flags via %%set_build_flags / PIE
- fix rpmlint: tmpfiles_create, remove env shebangs, own ghost directories
- keep dbus/polkit items for later security review
