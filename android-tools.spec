%global date 20110816
%global git_commit 80d508f
%global packdname core-%{git_commit}

Name:          android-tools
Version:       %{date}.%{git_commit}
Release:       3%{?dist}
Summary:       Android platform tools (adb, fastboot, etc.)

Group:         Applications/System
License:       ASL 2.0 and BSD
URL:           http://www.android.com/
Source0:       http://android.git.kernel.org/?p=platform/system/core.git;a=snapshot;h=%{git_commit};sf=tgz;/%{packdname}.tar.gz
Source1:       core-Makefile
Source2:       adb-Makefile
Source3:       fastboot-Makefile
Source4:       51-android.rules

BuildRequires: zlib-devel

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
install -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/udev/rules.d
install -D -m 0644 %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/udev/rules.d/51-android.rules
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir}

%files
%doc adb/OVERVIEW.TXT adb/SERVICES.TXT adb/protocol.txt
%{_bindir}/adb
%{_bindir}/fastboot
%{_sysconfdir}/udev/rules.d/51-android.rules


%changelog
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
