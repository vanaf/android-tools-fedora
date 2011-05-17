%global date 20110516
%global git_commit 327b2b7
%global packdname core-%{git_commit}

# FHS 2.3 compliant tree structure - http://www.pathname.com/fhs/2.3/
%global basedir %{_var}/lib/%{name}
%global appdir %{basedir}/webapps
%global bindir %{_datadir}/%{name}/bin
%global confdir %{_sysconfdir}/%{name}
%global homedir %{_datadir}/%{name}
%global libdir %{_javadir}/%{name}
%global logdir %{_var}/log/%{name}
%global cachedir %{_var}/cache/%{name}
%global tempdir %{cachedir}/temp
%global workdir %{cachedir}/work
%global _initrddir %{_sysconfdir}/init.d

Name:          android-tools
Epoch:         0
Version:       %{date}.%{git_commit}
Release:       1%{?dist}
Summary:       Android platform tools (adb, fastboot, etc)

Group:         Applications/System
License:       ASL 2.0
URL:           http://www.android.com/
Source0:       http://android.git.kernel.org/?p=platform/system/core.git;a=snapshot;h=327b2b7;sf=tgz;/%{packdname}.tar.gz
Source1:       core-Makefile
Source2:       adb-Makefile
Source3:       fastboot-Makefile

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
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir}

%files
%defattr(-,root,root,-)
%doc adb/OVERVIEW.TXT adb/SERVICES.TXT adb/protocol.txt
%{_bindir}/adb
%{_bindir}/fastboot


%changelog
* Wed May 18 2011 Ivan Afonichev <ivan.afonichev@gmail.com> - 20110516.327b2b7-1
- Initial spec
- Initial makefiles

