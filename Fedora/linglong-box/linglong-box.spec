%global debug_package %{nil}
Name:           linglong-box
Version:        2.1.2
Release:        1
Summary:        Linglong sandbox runtime.
License:        LGPL v3
URL:            https://gitee.com/LFRon/linyaps-box-linux-generic
Source0:        https://github.com/LFRon/linyaps-box-linux-generic/archive/refs/tags/2.1.2-1.zip

BuildRequires:  cmake gcc-c++ glib2-devel glibc-static libstdc++-static gtest-devel gmock-devel libseccomp-devel libcap-devel
Requires:       desktop-file-utils
Requires:       glib2 shared-mime-info erofs-utils
Recommends:    erofs-fuse

%description
Linyaps sandbox with OCI standard.It is used by Linyaps.

%prep
%autosetup -p1 -n linyaps-box-linux-generic-%{version}-%{release}

%define _debugsource_template %{nil}

%build
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_SHARED_LIBS=OFF \
      -Dlinyaps-box_CPM_LOCAL_PACKAGES_ONLY=ON ..
%make_build

%install
cd build
%make_install INSTALL_ROOT=%{buildroot}

%files
%license LICENSE
%{_bindir}/ll-box


%changelog
* Mon Nov 17 2025 LFRon <ronforever@qq.com> - 2.1.2-1
- Follow the upstream 2.1.2-1

* Wed Oct 15 2025 LFRon <ronforever@qq.com> - 2.1.1-1
- Follow the upstream 2.1.1-1

* Thu Sep 4 2025 LFRon <ronforever@qq.com> - 2.1.0-2
- Follow the upstream 2.1.0-1

* Thu Aug 07 2025 LFRon <ronforever@qq.com> - 2.1.0-1
- Follow the upstream 2.1.0
- fix: /tmp share with host

* Thu Jun 26 2025 LFRon <ronforever@qq.com> - 2.0.4-0
- Follow the Master-branch upstream 2.0.4-0

* Thu Jun 26 2025 chenchenjun <chenjiehai1024@gmail.com> - 2.0.0-1
- Follow the upstream version 2.0.0-1
