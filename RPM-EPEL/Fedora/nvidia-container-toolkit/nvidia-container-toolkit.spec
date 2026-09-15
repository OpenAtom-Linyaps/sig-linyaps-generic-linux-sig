# NVIDIA's official RPMs are built by their docker pipeline (binaries injected
# as Source0..10, rpmbuild run with -D macros). That is unusable on COPR, so
# this spec builds everything from source, following the single-self-contained-
# spec style of our linglong-box.spec:
#   - Source0: nvidia-container-toolkit v1.20.0 GitHub archive
#   - Source1: libnvidia-container v1.20.0 GitHub archive
#   - autosetup -n controls the directory each tarball lands in
#   - libnvidia-container-tools is produced as a subpackage of this same spec,
#     so the upstream "Requires: libnvidia-container-tools == version-release"
#     pin is satisfied without a second COPR package / buildorder.
%global debug_package %{nil}

Name:           nvidia-container-toolkit
Version:        1.20.0
Release:        1
Summary:        NVIDIA Container Toolkit
License:        Apache-2.0 AND BSD-3-Clause AND GPL-3.0-or-later AND LGPL-3.0-or-later AND MIT AND GPL-2.0-only
URL:            https://github.com/NVIDIA/nvidia-container-toolkit

Source0:        https://github.com/NVIDIA/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/NVIDIA/libnvidia-container/archive/refs/tags/v%{version}.tar.gz#/libnvidia-container-%{version}.tar.gz

# libnvidia-container (C; %build downloads nvidia-modprobe utils source):
BuildRequires:  make gcc git golang >= 1.25
BuildRequires:  libcap-devel libseccomp-devel elfutils-libelf-devel pkgconf
BuildRequires:  libtirpc-devel /usr/bin/rpcgen
%if 0%{?rhel} == 7 || 0%{?amzn} == 2
BuildRequires:  systemd
%else
BuildRequires:  systemd-rpm-macros
%endif

ExclusiveArch:  x86_64 aarch64 ppc64le

Obsoletes:      nvidia-container-runtime <= 3.5.0-1, nvidia-container-runtime-hook <= 1.4.0-2
Provides:       nvidia-container-runtime
Provides:       nvidia-container-runtime-hook
Requires:       libnvidia-container-tools == %{version}-%{release}, libnvidia-container-tools < 2.0.0
Requires:       nvidia-container-toolkit-base == %{version}-%{release}

%description
Provides tools and utilities to enable GPU support in containers, including
the NVIDIA Container Runtime, the NVIDIA Container Toolkit CLI, and the
libnvidia-container runtime library and tools.

%prep
# Extract both archives here explicitly so we control exactly the directories
# the sources land in (avoids multi-tarball %autosetup edge cases).
rm -rf %{_builddir}/nvidia-container-toolkit-%{version} %{_builddir}/libnvidia-container-%{version}
tar -xf %{SOURCE0} -C %{_builddir}
tar -xf %{SOURCE1} -C %{_builddir}

%define tk_src %{_builddir}/nvidia-container-toolkit-%{version}
%define lnc_src %{_builddir}/libnvidia-container-%{version}

%build
export GOTOOLCHAIN=local
export CGO_ENABLED=1
export GOFLAGS=-mod=vendor

# libnvidia-container:
#  - WITH_LIBELF=yes links against the system elfutils instead of downloading
#    elftoolchain from SourceForge.
#  - glibc >= 2.34 dropped the SunRPC headers, but the bundled libtirpc 1.3.2
#    no longer compiles on modern GCC; point the SunRPC includes at the system
#    libtirpc-devel and link -ltirpc via the makefiles' CPPFLAGS/LDLIBS append.
#  - REVISION/LIB_VERSION must be passed because the source archive has no .git.
#  - The same path variables are passed to %build and %install so the bundled
#    deps tree and the install stage stay consistent.
export CPPFLAGS="-I%{_includedir}/tirpc"
export LDLIBS="-ltirpc"
%make_build -C %{lnc_src} \
    LIB_VERSION=%{version} REVISION=v%{version} \
    WITH_LIBELF=yes WITH_TIRPC=no \
    prefix=%{_prefix} exec_prefix=%{_exec_prefix} \
    bindir=%{_bindir} libdir=%{_libdir} includedir=%{_includedir} \
    docdir=%{_docdir} \
    all

# nvidia-container-toolkit: build the Go commands with the vendored modules.
mkdir -p %{_builddir}/bin
%make_build -C %{tk_src} cmds \
    PREFIX=%{_builddir}/bin \
    GIT_COMMIT=v%{version} \
    VERSION=%{version}

%install
# Keep the same SunRPC flags in case the make install stage needs to relink.
export CPPFLAGS="-I%{_includedir}/tirpc"
export LDLIBS="-ltirpc"
# libnvidia-container library, CLI tool, headers, pkgconfig, static lib.
# The Makefile uses lower-case prefix/exec_prefix/libdir/... variables;
# pkgconfdir and libdbgdir are derived from prefix and libdir.
%{__make} -C %{lnc_src} install \
    LIB_VERSION=%{version} REVISION=v%{version} \
    WITH_LIBELF=yes WITH_TIRPC=no \
    prefix=%{_prefix} exec_prefix=%{_exec_prefix} \
    bindir=%{_bindir} libdir=%{_libdir} includedir=%{_includedir} \
    docdir=%{_docdir} \
    DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_presetdir}
mkdir -p %{buildroot}%{_sysconfdir}/nvidia-container-toolkit
mkdir -p %{buildroot}%{_licensedir}/%{name}-%{version}

install -m 644 %{tk_src}/LICENSE %{buildroot}%{_licensedir}/%{name}-%{version}/LICENSE

install -m 755 -t %{buildroot}%{_bindir} %{_builddir}/bin/nvidia-container-runtime-hook
install -m 755 -t %{buildroot}%{_bindir} %{_builddir}/bin/nvidia-container-runtime
install -m 755 -t %{buildroot}%{_bindir} %{_builddir}/bin/nvidia-container-runtime.cdi
install -m 755 -t %{buildroot}%{_bindir} %{_builddir}/bin/nvidia-container-runtime.legacy
install -m 755 -t %{buildroot}%{_bindir} %{_builddir}/bin/nvidia-ctk
install -m 755 -t %{buildroot}%{_bindir} %{_builddir}/bin/nvidia-cdi-hook
install -m 644 -t %{buildroot}%{_unitdir} %{tk_src}/deployments/systemd/nvidia-cdi-refresh.service
install -m 644 -t %{buildroot}%{_unitdir} %{tk_src}/deployments/systemd/nvidia-cdi-refresh.path
install -m 644 -t %{buildroot}%{_presetdir} %{tk_src}/deployments/systemd/90-nvidia-container-toolkit.preset
install -m 644 -t %{buildroot}%{_sysconfdir}/nvidia-container-toolkit %{tk_src}/deployments/systemd/nvidia-cdi-refresh.env

%post
if [ $1 -gt 1 ]; then  # only on package upgrade
  mkdir -p %{_localstatedir}/lib/rpm-state/nvidia-container-toolkit
  cp -af %{_bindir}/nvidia-container-runtime-hook %{_localstatedir}/lib/rpm-state/nvidia-container-toolkit
fi

%posttrans
if [ ! -e %{_bindir}/nvidia-container-runtime-hook ]; then
  # repairing lost file nvidia-container-runtime-hook
  cp -avf %{_localstatedir}/lib/rpm-state/nvidia-container-toolkit/nvidia-container-runtime-hook %{_bindir}
fi
rm -rf %{_localstatedir}/lib/rpm-state/nvidia-container-toolkit
ln -sf %{_bindir}/nvidia-container-runtime-hook %{_bindir}/nvidia-container-toolkit

%postun
if [ "$1" = 0 ]; then  # package is uninstalled, not upgraded
  if [ -L %{_bindir}/nvidia-container-toolkit ]; then rm -f %{_bindir}/nvidia-container-toolkit; fi
fi

%files
%license %{_licensedir}/%{name}-%{version}/LICENSE
%{_bindir}/nvidia-container-runtime-hook

%changelog
* Tue Sep 15 2026 Linglong SIG <sig@linglong.dev> - 1.20.0-1
- Repackaged for Fedora COPR: build nvidia-container-toolkit and
  libnvidia-container from the GitHub v1.20.0 source archives.

# ============================================================================
# libnvidia-container runtime library (built from Source1)
# ============================================================================
%package -n libnvidia-container1
Summary: NVIDIA container runtime library
License: BSD-3-Clause AND Apache-2.0 AND GPL-3.0-or-later AND LGPL-3.0-or-later AND MIT
Provides: libnvidia-container = %{version}-%{release}

%description -n libnvidia-container1
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package requires the NVIDIA driver (>= 340.29) to be installed separately.

%files -n libnvidia-container1
%doc %{_docdir}/libnvidia-container-%{version}/
%{_libdir}/libnvidia-container.so.*
%{_libdir}/libnvidia-container-go.so.*

%package -n libnvidia-container-tools
Summary: NVIDIA container runtime library (command-line tools)
Requires: libnvidia-container1 = %{version}-%{release}

%description -n libnvidia-container-tools
This package contains command-line tools that facilitate using the library.

%files -n libnvidia-container-tools
%{_bindir}/nvidia-container-cli

%package -n libnvidia-container-devel
Summary: NVIDIA container runtime library (development files)
Requires: libnvidia-container1 = %{version}-%{release}

%description -n libnvidia-container-devel
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware.

This package contains the files required to compile programs with the library.

%files -n libnvidia-container-devel
%{_includedir}/nvc.h
%{_libdir}/libnvidia-container.so
%{_libdir}/libnvidia-container-go.so
%{_libdir}/pkgconfig/libnvidia-container.pc

%package -n libnvidia-container-static
Summary: NVIDIA container runtime library (static library)
Requires: libnvidia-container-devel = %{version}-%{release}

%description -n libnvidia-container-static
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware.

This package contains the static build of the library.

%files -n libnvidia-container-static
%{_libdir}/libnvidia-container.a

# Debug symbols are pre-split by the Makefile (make strips the shared object
# during install), hence debug_package is disabled and the files are shipped
# explicitly, mirroring the upstream libnvidia-container packaging.
%package -n libnvidia-container1-debuginfo
Summary: NVIDIA container runtime library (debugging symbols)
Requires: libnvidia-container1 = %{version}-%{release}

%description -n libnvidia-container1-debuginfo
This package contains the debugging symbols for the library.

%files -n libnvidia-container1-debuginfo
%{_prefix}/lib/debug%{_libdir}/libnvidia-container.so.*

%post -n libnvidia-container1 -p /sbin/ldconfig
%postun -n libnvidia-container1 -p /sbin/ldconfig

# ============================================================================
# The BASE package consists of the NVIDIA Container Runtime and the NVIDIA
# Container Toolkit CLI. This allows the package to be installed on systems
# where no NVIDIA Container CLI is available.
# ============================================================================
%package base
Summary: NVIDIA Container Toolkit Base
Obsoletes: nvidia-container-runtime <= 3.5.0-1, nvidia-container-runtime-hook <= 1.4.0-2
Provides: nvidia-container-runtime
# Since this package allows certain components of the NVIDIA Container Toolkit to be installed separately
# it conflicts with older versions of the nvidia-container-toolkit package that also provide these files.
Conflicts: nvidia-container-toolkit <= 1.10.0-1

%description base
Provides tools such as the NVIDIA Container Runtime and NVIDIA Container Toolkit CLI to enable GPU support in containers.

%post base
# Generate the default config; If this file already exists no changes are made.
%{_bindir}/nvidia-ctk --quiet config --config-file=%{_sysconfdir}/nvidia-container-runtime/config.toml --in-place

%systemd_post nvidia-cdi-refresh.path nvidia-cdi-refresh.service

%preun base
%systemd_preun nvidia-cdi-refresh.path nvidia-cdi-refresh.service

%postun base
%systemd_postun nvidia-cdi-refresh.path nvidia-cdi-refresh.service

%posttrans base
# The refresh units were previously packaged in /etc/systemd/system. RPM
# removes those package-owned files on upgrade, but enablement links created by
# systemctl are unowned and can keep pointing at the old location.
stale_enabled_units_to_reenable=
for unit in nvidia-cdi-refresh.path nvidia-cdi-refresh.service; do
  old_unit="%{_sysconfdir}/systemd/system/${unit}"
  wants_link="%{_sysconfdir}/systemd/system/multi-user.target.wants/${unit}"
  if [ -L "${wants_link}" ]; then
    case "$(readlink "${wants_link}")" in
      "${old_unit}"|"../${unit}")
        rm -f "${wants_link}"
        stale_enabled_units_to_reenable="${stale_enabled_units_to_reenable} ${unit}"
        ;;
    esac
  fi
done

# Trigger CDI refresh on running systemd hosts without making install depend on
# the current system state.
if command -v systemctl >/dev/null 2>&1; then
  systemctl daemon-reload >/dev/null 2>&1 || :
  if [ -n "${stale_enabled_units_to_reenable}" ]; then
    systemctl enable ${stale_enabled_units_to_reenable} >/dev/null 2>&1 || :
  fi
  systemctl start nvidia-cdi-refresh.path >/dev/null 2>&1 || :
  systemctl start nvidia-cdi-refresh.service >/dev/null 2>&1 || :
fi

%files base
%license %{_licensedir}/%{name}-%{version}/LICENSE
%{_bindir}/nvidia-container-runtime
%{_bindir}/nvidia-ctk
%{_bindir}/nvidia-cdi-hook
%{_unitdir}/nvidia-cdi-refresh.service
%{_unitdir}/nvidia-cdi-refresh.path
%{_presetdir}/90-nvidia-container-toolkit.preset
%config(noreplace) %{_sysconfdir}/nvidia-container-toolkit/nvidia-cdi-refresh.env

# ============================================================================
# The OPERATOR EXTENSIONS package consists of components that are required to
# enable GPU support in Kubernetes. This package is not distributed as part of
# the NVIDIA Container Toolkit RPMs.
# ============================================================================
%package operator-extensions
Summary: NVIDIA Container Toolkit Operator Extensions
Requires: nvidia-container-toolkit-base == %{version}-%{release}

%description operator-extensions
Provides tools for using the NVIDIA Container Toolkit with the GPU Operator

%files operator-extensions
%license %{_licensedir}/%{name}-%{version}/LICENSE
%{_bindir}/nvidia-container-runtime.cdi
%{_bindir}/nvidia-container-runtime.legacy
