Summary:	Filesystem in Userspace
Name:		fuse
Version:	2.9.3
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/fuse/%{name}-%{version}.tar.gz
# Source0-md5:	33cae22ca50311446400daf8a6255c6a
Source1:	%{name}.conf
URL:		http://fuse.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	sed >= 4.0
Requires(pre,postun):	pwdutils
Requires:	%{name}-libs = %{version}-%{release}
Provides:	group(fuse)
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FUSE (Filesystem in Userspace) is a simple interface for userspace
programs to export a virtual filesystem to the Linux kernel. FUSE also
aims to provide a secure method for non privileged users to create and
mount their own filesystem implementations.

%package libs
Summary:	FUSE libraries
Group:		Libraries

%description libs
This package contains a shared libraries.

%package devel
Summary:	Filesytem in Userspace - Development header files
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Libfuse library header files.

%prep
%setup -q

%{__sed} -i "s|/sbin|%{_sbindir}|" configure.ac

%build
%{__libtoolize} --automake
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-example	\
	--disable-silent-rules	\
	--disable-static	\
	--enable-lib		\
	--enable-util
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkgconfigdir},%{_sysconfdir}}

for DIR in include lib util; do
%{__make} -C $DIR install \
	DESTDIR=$RPM_BUILD_ROOT
done

install fuse.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

%{__rm} -r $RPM_BUILD_ROOT/etc/{init.d,udev}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 102 fuse

%postun
if [ "$1" = "0" ] ; then
	%groupremove fuse
fi

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README NEWS ChangeLog AUTHORS doc/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fuse.conf

%attr(4754,root,fuse) %{_bindir}/fusermount
%attr(4754,root,fuse) %{_bindir}/ulockmgr_server
%attr(755,root,root) %{_sbindir}/mount.fuse

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libfuse.so.?
%attr(755,root,root) %ghost %{_libdir}/libulockmgr.so.?
%attr(755,root,root) %{_libdir}/libfuse.so.*.*.*
%attr(755,root,root) %{_libdir}/libulockmgr.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfuse.so
%attr(755,root,root) %{_libdir}/libulockmgr.so
%{_libdir}/libfuse.la
%{_libdir}/libulockmgr.la
%{_includedir}/fuse
%{_includedir}/*.h
%{_pkgconfigdir}/fuse.pc

