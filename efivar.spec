Name:           efivar
Version:        36
Release:        12%{?dist}
Summary:        Tools to manage UEFI variables
License:        LGPLv2+
URL:            https://github.com/rhinstaller/efivar
Requires:       %{name}-libs = %{version}-%{release}
ExclusiveArch:  x86_64 aarch64

BuildRequires:  popt popt-devel popt-static git glibc-static
Source0:        https://github.com/rhinstaller/efivar/releases/download/efivar-%{version}/efivar-%{version}.tar.bz2
Patch0001: 0001-libabigail-isn-t-in-RHEL-yet-so-nerf-the-abi-check.patch
Patch0002: 0002-Move-the-syntastic-file-I-use-out-of-the-repo.patch
Patch0003: 0003-Move-verbosity-headers-to-be-public.patch
Patch0004: 0004-Pacify-some-coverity-nits.patch
Patch0005: 0005-efivar-Fix-some-types-in-L-behavior-to-pacify-coveri.patch
Patch0006: 0006-Promote-_make_hd_dn-to-make_hd_dn-and-get-rid-of-the.patch
Patch0007: 0007-Try-to-convince-covscan-that-sysfs_read_file-doesn-t.patch
Patch0008: 0008-Make-efidp_make_file-have-even-more-better-input-con.patch
Patch0009: 0009-Make-path-helpers.c-also-import-fix_coverity.h.patch
Patch0010: 0010-Fix-a-makeguids-building-problem-with-generics.h.patch
Patch0011: 0011-Improve-ACPI-device-path-formatting.patch
Patch0012: 0012-Give-linux-s-parse-functions-the-unmodified-device-l.patch
Patch0013: 0013-Move-ACPI-ID-parsing-to-a-shared-location.patch
Patch0014: 0014-Make-a-platform-ACPI-root-parser-separate-from-PCI-r.patch
Patch0015: 0015-Make-a-way-to-say-e-3-isn-t-viable-for-a-kind-of-dev.patch
Patch0016: 0016-Make-a-linux-device-root-for-SOC-devices-that-use-FD.patch
Patch0017: 0017-If-we-can-t-parse-part-of-the-device-link-skip-it-an.patch
Patch0018: 0018-Pacify-clang-analyzer-just-a-little.patch
Patch0019: 0019-Try-even-harder-to-convince-coverity-that-get_file-i.patch
Patch0020: 0020-Make-the-debug-code-less-intrusive.patch
Patch0021: 0021-efiboot-Make-the-device-node-skipping-code-pass-cove.patch
Patch0022: 0022-efiboot-don-t-error-on-unknown-type-with-DEV_ABBREV_.patch
Patch0023: 0023-efiboot-fix-a-bad-error-check.patch
Patch0024: 0024-efiboot-parse_scsi_link-fix-the-offset-searching-for.patch
Patch0025: 0025-Coverity-still-doesn-t-believe-in-error-codes.patch
Patch0026: 0026-Don-t-require-NVME-to-have-an-EUI.patch
Patch0027: 0027-Fix-another-buggy-fake-acpi-pci-root-driver.patch
Patch0028: 0028-Fix-dev-probes-intialization-test.patch
Patch0029: 0029-Deal-with-devices-that-don-t-have-a-device-link-in-s.patch
Patch0030: 0030-Handle-partition-name-parsing-and-formatting-for-par.patch
Patch0031: 0031-Fix-partition-number-detection-when-it-s-not-provide.patch

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
* Tue Nov 13 2018 Javier Martinez Canillas <javierm@redhat.com> - 36-12
- Fix partition number detection when it's not provided (pjones)
  Resolves: rhbz#1616305

* Mon Sep 17 2018 Peter Jones <pjones@redhat.com> - 36-11
- Fix device probing with no matching probes where HD() will work
  Resolves: rhbz#1613698
- Detect partitiond md devices correctly
  Resolves: rhbz#1602414
  Resolves: rhbz#1613370

* Mon Sep 10 2018 Peter Jones <pjones@redhat.com> - 36-10
- Work around platform ACPI PCI(e) root drivers that don't fill in the
  "driver" symlink in sysfs.
  Resolves: rhbz#1614944

* Mon Jul 16 2018 Peter Jones <pjones@redhat.com> - 36-9
- Don't require NVME to have an EUI
  Resolves: rhbz#1593784

* Thu Jun 21 2018 Peter Jones <pjones@redhat.com> - 36-8
- Fix another minor covscan complaint
  Related: rhbz#1558937
  Related: rhbz#1591853

* Thu Jun 21 2018 Peter Jones <pjones@redhat.com> - 36-7
- Fix a couple more weird Aarch64 machines
  Related: rhbz#1558937
  Resolves: rhbz#1591853

* Wed Jun 20 2018 Peter Jones <pjones@redhat.com> - 36-6
- Fix device path generation for block devices on nonstandard device path
  roots.
  Related: rhbz#1558937
  Resolves: rhbz#1591853

* Thu Jun 14 2018 Peter Jones <pjones@redhat.com> - 36-5
- Try to fix some minor coverity nits.
  Related: rhbz#1520533
  Related: rhbz#1570032

* Wed Jun 13 2018 Peter Jones <pjones@redhat.com> - 36-4
- Try to fix some minor coverity nits.
  Related: rhbz#1520533
  Related: rhbz#1570032

* Tue Jun 12 2018 Peter Jones <pjones@redhat.com> - 36-3
- Try to fix some minor coverity nits.
  Related: rhbz#1520533
  Related: rhbz#1570032

* Sat Jun 09 2018 Peter Jones <pjones@redhat.com> - 36-2
- Minor specfile cleanup to pacify rpmdiff
  Related: rhbz#1520533
  Related: rhbz#1570032

* Fri Jun 08 2018 Peter Jones <pjones@redhat.com> - 36-1
- Rebase to efivar 36
  Resolves: rhbz#1520533
  Related: rhbz#1570032

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
