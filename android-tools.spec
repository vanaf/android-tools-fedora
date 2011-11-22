%global date 20111120
%global git_commit 4a25390
%global packdname core-%{git_commit}

Name:          android-tools
Version:       %{date}git%{git_commit}
Release:       2%{?dist}
Summary:       Android platform tools

Group:         Applications/System
License:       ASL 2.0 and BSD
URL:           http://www.android.com/

#  using git archive since upstream hasn't created tarballs. 
#  git archive --format=tar --prefix=%%{packdname}/ %%{git_commit} adb fastboot libzipfile libcutils  mkbootimg include/cutils include/zipfile | xz  > %%{packdname}.tar.xz
#  https://android.googlesource.com/platform/system/core.git

Source0:       %{packdname}.tar.xz
Source1:       core-Makefile
Source2:       adb-Makefile
Source3:       fastboot-Makefile
Source4:       51-android.rules

Requires:      udev
BuildRequires: zlib-devel

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
%setup -q -n %{packdname}
cp -p %{SOURCE1} Makefile
cp -p %{SOURCE2} adb/Makefile
cp -p %{SOURCE3} fastboot/Makefile



%build
make %{?_smp_mflags}

%install
install -d -m 0755 ${RPM_BUILD_ROOT}%{_bindir}
install -d -m 0755 ${RPM_BUILD_ROOT}/lib/udev/rules.d
install -D -m 0644 %{SOURCE4} ${RPM_BUILD_ROOT}/lib/udev/rules.d/51-android.rules
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir}

%files
%doc adb/OVERVIEW.TXT adb/SERVICES.TXT adb/NOTICE adb/protocol.txt
#ASL2.0
%{_bindir}/adb
#ASL2.0 and BSD.
%{_bindir}/fastboot
/lib/udev/rules.d/51-android.rules


%changelog
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
