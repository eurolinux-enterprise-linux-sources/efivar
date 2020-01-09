Name:           efivar
Version:        31
Release:        4%{?dist}
Summary:        Tools to manage UEFI variables
License:        LGPLv2.1
URL:            https://github.com/rhinstaller/efivar
Requires:       %{name}-libs = %{version}-%{release}
ExclusiveArch:	x86_64 aarch64

BuildRequires:  popt popt-devel popt-static git glibc-static
Source0:        https://github.com/rhinstaller/efivar/releases/download/efivar-%{version}/efivar-%{version}.tar.bz2
Patch0001:	0001-libabigail-isn-t-in-RHEL-yet-so-nerf-the-abi-check.patch
Patch0002:	0002-Don-t-use-_Generic-because-gcc-4.x-doesn-t-have-it.patch
Patch0003:	0003-popt-devel-in-RHEL-7.4-doesn-t-provide-popt.pc-so-in.patch
Patch0004:	0004-efi_loadopt_args_from_file-fix-leaked-file-descripto.patch
Patch0005:	0005-make_mac_path-fix-leaked-file-descriptor.patch
Patch0006:	0006-gpt_disk_get_partition_info-free-our-allocations-on-.patch
Patch0007:	0007-efi_generate_file_device_path-fix-one-error-case-s-f.patch
Patch0008:	0008-efi_va_generate_file_device_path_from_esp-handle-err.patch
Patch0009:	0009-efi_variable_import-fix-memory-leak-on-failure-path.patch
Patch0010:	0010-efidp_append_path-error-check-the-right-variable.patch
Patch0011:	0011-efi_variable_import-make-sure-var.data_size-is-set.patch
Patch0012:	0012-makeguids-free-our-input-buffer.patch
Patch0013:	0013-efi_variable_import-constrain-our-inputs-better.patch
Patch0014:	0014-efi_loadopt_create-check-buf-for-NULLness.patch
Patch0015:	0015-efidp_duplicate_extra-error-if-our-allocation-is-too.patch
Patch0016:	0016-show_errors-make-the-useful-part-here-not-be-dead-co.patch
Patch0017:	0017-efi_loadopt_args_from_file-make-sure-buf-is-only-NUL.patch
Patch0018:	0018-calls-to-sysfs_readlink-check-linkbuf-for-NULLness.patch
Patch0019:	0019-efivar-main-explain-efi_well_known_guids-to-the-comp.patch
Patch0020:	0020-dp.h-Try-to-make-covscan-believe-format-is-checking-.patch
Patch0021:	0021-gpt-try-to-avoid-trusting-unverified-partition-table.patch
Patch0022:	0022-Simplify-efidp_append_node-even-more.patch
Patch0023:	0023-efi_loadopt_create-avoid-NULL-dereference.patch
Patch0024:	0024-efi_generate_file_device_path-make-all-error-paths-u.patch
Patch0025:	0025-linux.c-fix-a-pile-of-sscanf-NULL-.-possibilities.patch

%description
efivar provides a simple command line interface to the UEFI variable facility.

%package libs
Summary: Library to manage UEFI variables

%description libs
Library to allow for the simple manipulation of UEFI variables.

%package devel
Summary: Development headers for libefivar
Requires: %{name}-libs = %{version}-%{release}

%description devel
development headers required to use libefivar.

%prep
%setup -q -n %{name}-%{version}
git init
git config user.email "example@example.com"
git config user.name "RHEL Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name

%build
make libdir=%{_libdir} bindir=%{_bindir} CFLAGS="$RPM_OPT_FLAGS -flto" LDFLAGS="$RPM_LD_FLAGS -flto"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{_bindir}/efivar
%exclude %{_bindir}/efivar-static
%{_mandir}/man1/*

%files devel
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files libs
%{_libdir}/*.so.*

%changelog
* Tue May 09 2017 Peter Jones <pjones@redhat.com> - 31-4
- Fix a bunch of coverity issues.
  Related: rhbz#1380825
  Related: rhbz#1310779

* Tue May 09 2017 Peter Jones <pjones@redhat.com> - 31-3
- Fix a bunch of coverity issues.
  Related: rhbz#1380825
  Related: rhbz#1310779

* Tue May 09 2017 Peter Jones <pjones@redhat.com> - 31-2
- Fix a bunch of coverity issues.
  Related: rhbz#1380825
  Related: rhbz#1310779

* Mon Mar 13 2017 Peter Jones <pjones@redhat.com> - 31-1
- Update to efivar 31
  Related: rhbz#1380825
  Related: rhbz#1310779

* Wed Aug 20 2014 Peter Jones <pjones@redhat.com> - 0.11-1
- Update to 0.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Peter Jones <pjones@redhat.com> - 0.10-1
- Update package to 0.10.
- Fixes a build error due to different cflags in the builders vs updstream
  makefile.

* Fri May 02 2014 Peter Jones <pjones@redhat.com> - 0.9-0.1
- Update package to 0.9.

* Tue Apr 01 2014 Peter Jones <pjones@redhat.com> - 0.8-0.1
- Update package to 0.8 as well.

* Fri Oct 25 2013 Peter Jones <pjones@redhat.com> - 0.7-1
- Update package to 0.7
- adds --append support to the binary.

* Fri Sep 06 2013 Peter Jones <pjones@redhat.com> - 0.6-1
- Update package to 0.6
- fixes to documentation from lersek
- more validation of uefi guids
- use .xz for archives

* Thu Sep 05 2013 Peter Jones <pjones@redhat.com> - 0.5-0.1
- Update to 0.5

* Mon Jun 17 2013 Peter Jones <pjones@redhat.com> - 0.4-0.2
- Fix ldconfig invocation

* Mon Jun 17 2013 Peter Jones <pjones@redhat.com> - 0.4-0.1
- Initial spec file
