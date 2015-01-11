%global date 20141219
%global git_commit 8393e50

%global packdname core-%{git_commit}
%global extras_git_commit 1e7d4f3
%global extras_packdname extras-%{extras_git_commit}

%global _hardened_build 1

Name:          android-tools
Version:       %{date}git%{git_commit}
Release:       2%{?dist}
Summary:       Android platform tools(adb, fastboot)

Group:         Applications/System
# The entire source code is ASL 2.0 except fastboot/ which is BSD
License:       ASL 2.0 and (ASL 2.0 and BSD)
URL:           http://developer.android.com/guide/developing/tools/

#  using git archive since upstream hasn't created tarballs. 
#  git archive --format=tar --prefix=%%{packdname}/ %%{git_commit} adb fastboot libzipfile libcutils libmincrypt libsparse mkbootimg include/cutils include/zipfile include/mincrypt include/utils include/private | xz  > %%{packdname}.tar.xz
#  https://android.googlesource.com/platform/system/core.git
#  git archive --format=tar --prefix=extras/ %%{extras_git_commit} ext4_utils f2fs_utils | xz  > %%{extras_packdname}.tar.xz
#  https://android.googlesource.com/platform/system/extras.git

Source0:       %{packdname}.tar.xz
Source1:       %{extras_packdname}.tar.xz
Source2:       core-Makefile
Source3:       adb-Makefile
Source4:       fastboot-Makefile
Source5:       51-android.rules
Source6:       adb.service
# None of the code *we* compile uses anything from selinux/android.h, but 
# other code may, so not upstreaming these patches
Patch1:        0001-Remove-android-selinux-header.patch
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: zlib-devel
BuildRequires: openssl-devel
BuildRequires: libselinux-devel
BuildRequires: f2fs-tools-devel
BuildRequires: systemd

Provides:      adb
Provides:      fastboot

%description

The Android Debug Bridge (ADB) is used to:

- keep track of all Android devices and emulators instances
  connected to or running on a given host developer machine

- implement various control commands (e.g. "adb shell", "adb pull", etc.)
  for the benefit of clients (command-line users, or helper programs like
  DDMS). These commands are what is called a 'service' in ADB.

Fastboot is used to manipulate the flash partitions of the Android phone. 
It can also boot the phone using a kernel image or root filesystem image 
which reside on the host machine rather than in the phone flash. 
In order to use it, it is important to understand the flash partition 
layout for the phone.
The fastboot program works in conjunction with firmware on the phone 
to read and write the flash partitions. It needs the same USB device 
setup between the host and the target phone as adb.

%prep
%setup -q -b 1 -n extras
%patch1 -p1
%setup -q -b 0 -n %{packdname}
cp -p %{SOURCE2} Makefile
cp -p %{SOURCE3} adb/Makefile
cp -p %{SOURCE4} fastboot/Makefile
cp -p %{SOURCE5} 51-android.rules

%build
make %{?_smp_mflags}

%install
install -d -m 0755 ${RPM_BUILD_ROOT}%{_bindir}
install -d -m 0775 ${RPM_BUILD_ROOT}%{_sharedstatedir}/adb
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir}
install -p -D -m 0644 %{SOURCE6} \
    %{buildroot}%{_unitdir}/adb.service

%post
%systemd_post adb.service

%preun
%systemd_preun adb.service

%postun
%systemd_postun_with_restart adb.service

%files
%doc adb/OVERVIEW.TXT adb/SERVICES.TXT adb/NOTICE adb/protocol.txt 51-android.rules
%{_unitdir}/adb.service
%attr(0755,root,root) %dir %{_sharedstatedir}/adb
#ASL2.0
%{_bindir}/adb
#ASL2.0 and BSD.
%{_bindir}/fastboot


%changelog
* Sun Jan 11 2015 Ivan Afonichev <ivan.afonichev@gmail.com> - 20141224git8393e50-2
- Resolves: rhbz 1062095 Harden android-tools
- Remove 0002-Add-missing-headers.patch

* Wed Dec 24 2014 Jonathan Dieter <jdieter@lesbg.com> - 20141224git8393e50-1
- Update to 5.0.2 release

* Fri Sep 19 2014 Ivan Afonichev <ivan.afonichev@gmail.com> - 20130123git98d0789-5
- Added more udev devices
- Resolves: rhbz 967216 Adb service now stores keys in /var/lib/adb

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130123git98d0789-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130123git98d0789-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130123git98d0789-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jan 28 2013 Ivan Afonichev <ivan.afonichev@gmail.com> - 20130123git98d0789-1
- Update to upstream git commit 98d0789
- Resolves: rhbz 903074 Move udev rule to docs as example
- Resolves: rhbz 879585 Introduce adb.service with PrivateTmp

* Tue Nov 20 2012 Ivan Afonichev <ivan.afonichev@gmail.com> - 20121120git3ddc005-1
- Update to upstream git commit 3ddc005
- Added more udev devices
- Added ext4_utils from extras for fastboot
- Updated makefiles
- Resolves: rhbz 869624 start adb server by udev

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120510gitd98c87c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 10 2012 Ivan Afonichev <ivan.afonichev@gmail.com> - 20120510gitd98c87c-1
- Update to upstream git commit d98c87c
- Added more udev devices
- Resolves: rhbz 819292 secure udev permissions

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20111220git1b251bd-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 20111220git1b251bd-1
- Update to upstream git commit 1b251bd

* Wed Nov 23 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 20111120git4a25390-3
- Fix license
- More specific URL

* Tue Nov 22 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 20111120git4a25390-2
- Require udev

* Sun Nov 20 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 20111120git4a25390-1
- Versioning changes
- Use only needed sources
- Udev rules moved to lib
- More license info added
- adb and fastboot moved to provides from summary

* Tue Nov 15 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 20111115.4a25390-1
- Change upstream git repo URL
- Update to upstream git commit 4a25390
- Added more udev devices

* Mon Oct 17 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 20110816.80d508f-3
- Update udev rules (s/SYSFS/ATTR/g) 

* Sat Aug 27 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 20110816.80d508f-2
- Remove the rm in the install section
- Remove defattr
- Use install command(not macro)
- Add description of fastboot

* Tue Aug 16 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 20110816.80d508f-1
- Update to upstream git commit 80d508f
- Added more udev devices

* Sun Jul 31 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 20110731.810cf41-1
- Update to upstream git commit 810cf41
- Fix License
- Use optflags
- Added more udev devices
- Remove Epoch

* Tue Jul 26 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 0:20110726.212282c-1
- Update to upstream git commit 212282c

* Wed May 18 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 0:20110516.327b2b7-1
- Initial spec
- Initial makefiles
- Initial udev rule
