# 定义SELinux相关宏
%global selinuxtype targeted
%global moduletype contrib
%global modulename ll-box

BuildArch:     noarch
Name:          linglong-selinux
Version:       1.0
Release:       1
Source0:       https://github.com/LFRon/Linyaps-SELinux-module/archive/refs/heads/main.zip
License:       LGPL-3.0
Summary:       SELinux policy module for linyaps-box

BuildRequires:      selinux-policy-devel unzip
Requires(post):     /bin/sh
Requires(postun):   /bin/sh
Requires(post):     libselinux-utils
Requires(post):     policycoreutils
Requires(post):     policycoreutils-python-utils
Requires:           linglong-bin
Requires:           linglong-box
#Requires:      rpmlib(CompressedFileNames) <= 3.0.4-1
#Requires:      rpmlib(FileDigests) <= 4.6.0-1
#Requires:      rpmlib(PayloadFilesHavePrefix) <= 4.0-1
#Requires:      rpmlib(PayloadIsZstd) <= 5.4.18-1
Requires:           selinux-policy >= 41.39
Requires(post):     selinux-policy-base >= 41.39

%description
This package contains the SELinux policy module for linyaps.

%prep
%autosetup -p1 -n Linyaps-SELinux-module-main

%build
make -f /usr/share/selinux/devel/Makefile %{modulename}.pp

%install
install -d %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}
install -m 0644 %{modulename}.pp %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/

# 安装后脚本：加载策略模块到内核
%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp

# 卸载前脚本：如果完全卸载（$1 == 0），则移除策略模块
%preun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi

%files
%attr(0644, root, root) %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp

%changelog
* Wed Feb 25 2026 LFRon <ronforever@qq.com> 1.0-1
- Initial SELinux module for Linyaps
