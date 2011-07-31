%global date 20110731
%global git_commit 810cf41
%global packdname core-%{git_commit}

Name:          android-tools
Version:       %{date}.%{git_commit}
Release:       1%{?dist}
Summary:       Android platform tools (adb, fastboot, etc)

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

- implement various control commands (e.g. "adb shell", "adb pull", etc..)
  for the benefit of clients (command-line users, or helper programs like
  DDMS). These commands are what is called a 'service' in ADB.

%prep
%setup -q -n %{packdname}
cp -p %{SOURCE1} Makefile
cp -p %{SOURCE2} adb/Makefile
cp -p %{SOURCE3} fastboot/Makefile



%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_bindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/udev/rules.d
%{__install} -D -m 0644 %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/udev/rules.d/51-android.rules
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir}

%files
%defattr(-,root,root,-)
%doc adb/OVERVIEW.TXT adb/SERVICES.TXT adb/protocol.txt
%{_bindir}/adb
%{_bindir}/fastboot
%{_sysconfdir}/udev/rules.d/51-android.rules


%changelog
* Sun Jul 31 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 0:20110731.810cf41-1
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
