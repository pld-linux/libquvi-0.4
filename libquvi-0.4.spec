#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	A cross-platform library for parsing flash media stream
Summary(pl.UTF-8):	Wieloplatformowa biblioteka do analizy flashowych strumieni multimedialnych
Name:		libquvi-0.4
Version:	0.4.1
Release:	1
License:	AGPL v3+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/quvi/libquvi-%{version}.tar.xz
# Source0-md5:	acc5a5da25a7f89c6ff5338d00eaaf58
Patch0:		%{name}-automake-1.12.patch
URL:		http://quvi.sourceforge.net/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	curl-devel >= 7.18.2
BuildRequires:	libquvi-scripts-0.4 >= 0.4.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	lua51-devel >= 5.1
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	curl-libs >= 7.18.2
Requires:	libquvi-scripts-0.4 >= 0.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libquvi is a cross-platform library for parsing flash media stream.

%description -l pl.UTF-8
libquvi to wieloplatformowa biblioteka do analizy flashowych strumieni
multimedialnych.

%package devel
Summary:	Header files for libquvi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libquvi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	lua51-devel

%description devel
Header files for libquvi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libquvi.

%package static
Summary:	Static libquvi library
Summary(pl.UTF-8):	Statyczna biblioteka libquvi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libquvi library.

%description static -l pl.UTF-8
Statyczna biblioteka libquvi.

%prep
%setup -q -n libquvi-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# libquiv 0.9 version is packaged in libquvi.spec
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/libquvi.3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libquvi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libquvi.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libquvi.so
%{_includedir}/quvi
%{_pkgconfigdir}/libquvi.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libquvi.a
%endif
