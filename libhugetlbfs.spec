Name: libhugetlbfs
Version: 2.8
Release: 2%{?dist}
Summary: A library which provides easy access to huge pages of memory

Group: System Environment/Libraries
License: LGPLv2+
URL: http://libhugetlbfs.sourceforge.net/
Source0: http://downloads.sourceforge.net/libhugetlbfs/%{name}-%{version}.tar.gz
Patch0: libhugetlbfs-2.6-s390x-build.patch
Patch1: setup_helper-fix-the-minor-arithmetic-issue.patch
Patch2: setup_helper-check-for-permission-and-disable-defaul.patch
Patch3: setup_helper-make-r-w-ops-of-security-limits.d-.conf.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: glibc-headers
Conflicts: kernel < 2.6.16
Obsoletes: libhugetlbfs-test <= 1.1
ExcludeArch: s390 s390x

%define ldscriptdir %{_datadir}/%{name}/ldscripts

%description
libhugetlbfs is a library which provides easy access to huge pages of memory.
It is a wrapper for the hugetlbfs file system. Applications can use huge pages
to fulfill malloc() requests without being recompiled by using LD_PRELOAD.
Alternatively, applications can be linked against libhugetlbfs without source
modifications to load BSS or BSS, data, and text segments into large pages.

%package devel
Summary:	Header files for libhugetlbfs
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description devel
Contains header files for building with libhugetlbfs.

%package utils
Summary:	Userspace utilities for configuring the hugepage environment
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
%description utils
This packages contains a number of utilities that will help administrate the
use of huge pages on your system.  hugeedit modifies binaries to set default
segment remapping behavior. hugectl sets environment variables for using huge
pages and then execs the target program. hugeadm gives easy access to huge page
pool size control. pagesize lists page sizes available on the machine.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .s390x-build
%patch1 -p1 -b .math-is-hard
%patch2 -p1 -b .perms
%patch3 -p1 -b .limits

%build
# Parallel builds are not reliable
make BUILDTYPE=NATIVEONLY

%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT LDSCRIPTDIR=%{ldscriptdir} BUILDTYPE=NATIVEONLY
make install-helper PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT LDSCRIPTDIR=%{ldscriptdir} BUILDTYPE=NATIVEONLY
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/security/limits.d
touch $RPM_BUILD_ROOT%{_sysconfdir}/security/limits.d/hugepages.conf

# remove statically built libraries:
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
# remove unused sbin directory
rm -fr $RPM_BUILD_ROOT/%{_sbindir}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libhugetlbfs.so*
%{_datadir}/%{name}/
%{_mandir}/man7/libhugetlbfs.7.gz
%ghost %config(noreplace) %{_sysconfdir}/security/limits.d/hugepages.conf
%exclude %{_libdir}/libhugetlbfs_privutils.so
%doc README HOWTO LGPL-2.1 NEWS

%files devel
%defattr(-,root,root,-)
%{_includedir}/hugetlbfs.h
%{_mandir}/man3/getpagesizes.3.gz
%{_mandir}/man3/free_huge_pages.3.gz
%{_mandir}/man3/get_huge_pages.3.gz
%{_mandir}/man3/gethugepagesizes.3.gz
%{_mandir}/man3/free_hugepage_region.3.gz
%{_mandir}/man3/get_hugepage_region.3.gz

%files utils
%defattr(-,root,root,-)
%{_bindir}/hugeedit
%{_bindir}/hugeadm
%{_bindir}/hugectl
%{_bindir}/pagesize
%{_bindir}/huge_page_setup_helper.py
%exclude %{_bindir}/cpupcstat
%exclude %{_bindir}/oprofile_map_events.pl
%exclude %{_bindir}/oprofile_start.sh
%{_mandir}/man8/hugeedit.8.gz
%{_mandir}/man8/hugectl.8.gz
%{_mandir}/man8/hugeadm.8.gz
%{_mandir}/man1/pagesize.1.gz
%exclude %{_mandir}/man8/cpupcstat.8.gz
%exclude /usr/lib/perl5/TLBC

%changelog
* Tue Jul 20 2010 Jarod Wilson <jarod@redhat.com> - 2.8-2
- Fix arithmetic and permissions issues uncovered by recent
  testing (Anton Arapov) [471823]

* Tue Jun 15 2010 Anton Arapov <aarapov@redhat.com> - 2.8-1
- Update for the libhugetlbfs-2.8 release
- build 32-bit ppc package [603788]

* Wed Mar 24 2010 Anton Arapov <aarapov@redhat.com> - 2.7-3
- fixed linker options [572865]

* Tue Mar 23 2010 Anton Arapov <aarapov@redhat.com> - 2.7-2
- disable executable stacks entirely [572865]

* Tue Mar 16 2010 Anton Arapov <aarapov@redhat.com> - 2.7-1
- Update for the libhugetlbfs-2.7 release
- revert: disable executable stacks entirely [572865]

* Mon Mar 15 2010 Anton Arapov <aarapov@redhat.com> - 2.6-4
- disable executable stacks entirely [572865]

* Thu Feb  4 2010 Anton Arapov <aarapov@redhat.com> - 2.6-3.2
- fix building: sys/stat.h include missed in elflink.c [558908]

* Wed Dec  9 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.6-3.1
- Don't build on ppc, s390, s390x

* Fri Oct 02 2009 Jarod Wilson <jarod@redhat.com> 2.6-3
- Add hopefully-about-to-be-merged-upstream hugeadm enhancements
- Add huge pages setup helper script, using new hugeadm enhancements

* Thu Sep 03 2009 Nils Philippsen <nils@redhat.com> 2.6-2
- fix building on s390x

* Mon Aug 31 2009 Eric Munson <ebmunson@us.ibm.com> 2.6-1
- Updating for the libhugetlbfs-2.6 release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Eric Munson <ebmunson@us.ibm.com> 2.5-2
- Update Group for -utils package to Applications/System

* Tue Jun 30 2009 Eric Munson <ebmunson@us.ibm.com> 2.5-1
- Updating for the libhugetlbfs-2.5 release

* Tue Jun 02 2009 Eric Munson <ebmunson@us.ibm.com> 2.4-2
- Adding patch to remove S390 32 bit build

* Fri May 29 2009 Eric Munson <ebmunson@us.ibm.com> 2.4-1
- Updating for the libhugetlbfs-2.4 release

* Wed Apr 15 2009 Eric Munson <ebmunson@us.ibm.com> 2.3-1
- Updating for the libhugetlbfs-2.3 release

* Wed Feb 11 2009 Eric Munson <ebmunson@us.ibm.com> 2.2-1
- Updating for the libhugetlbfs-2.2 release

* Fri Dec 19 2008 Eric Munson <ebmunson@us.ibm.com> 2.1.2-1
- Updating for libhugetlbfs-2.1.2 release

* Fri Dec 19 2008 Eric Munson <ebmunson@us.ibm.com> 2.1.1-1
- Updating for libhugetlbfs-2.1.1 release

* Thu Dec 18 2008 Josh Boyer <jwboyer@gmail.com> 2.1-2
- Fix broken dependency caused by just dropping -test
  subpackage

* Thu Oct 16 2008 Eric Munson <ebmunson@us.ibm.com> 2.1-1
- Updating for libhuge-2.1 release
- Adding -devel and -utils subpackages for various utilities
  and devel files.

* Wed May 14 2008 Eric Munson <ebmunson@us.ibm.com> 1.3-1
- Updating for libhuge-1.3 release

* Tue Mar 25 2008 Eric Munson <ebmunson@us.ibm.com> 1.2-1
- Removing test rpm target, and excluding test files

* Mon Mar 26 2007 Steve Fox <drfickle@k-lug.org> - 1.1-1
- New release (1.1)
- Fix directory ownership

* Wed Aug 30 2006 Steve Fox <drfickle@k-lug.org> - 0.20060825-1
- New release (1.0-preview4)
- patch0 (Makefile-ldscript.diff) merged upstream

* Tue Jul 25 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-4
- Bump for build system

* Tue Jul 25 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-3
- Don't use parallel build as it has random failures

* Thu Jul 20 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-2
- Fix the Makefile so that the ld.hugetlbfs script doesn't store the
  DESTDIR in the path to the ldscripts dir

* Fri Jul 7 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-1
- New release which includes a fix for the syscall macro removal in the
  Rawhide kernels

* Thu Jun 29 2006 Steve Fox <drfickle@k-lug.org> - 0.20060628-1
- First Fedora package
