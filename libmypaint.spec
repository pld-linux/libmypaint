#
# Conditional build:
%bcond_without	apidocs	# API documentation
%bcond_without	openmp	# OpenMP support

Summary:	Library for making brush strokes
Summary(pl.UTF-8):	Biblioteka do wykonywania dotknięć pędzla
Name:		libmypaint
Version:	1.6.1
Release:	2
License:	ISC
Group:		Libraries
#Source0Download: https://github.com/mypaint/libmypaint/releases
Source0:	https://github.com/mypaint/libmypaint/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	7f1dab2d30ce8a3f494354c7c77a2977
URL:		http://mypaint.org/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gegl-devel >= 0.4.14
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gobject-introspection-devel >= 1.32.0
BuildRequires:	intltool
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	libtool >= 2:2.2
BuildRequires:	json-c-devel
BuildRequires:	pkgconfig >= 1:0.16
BuildRequires:	rpm-build >= 4.6
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with apidocs}
BuildRequires:	doxygen
%endif
Requires:	gegl >= 0.4.14
Conflicts:	mypaint < 1.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a self-contained library containing the MyPaint brush engine.

%description -l pl.UTF-8
Ten pakiet zawiera samodzielną bibliotekę silnika pędzli MyPaint.

%package devel
Summary:	Development files for libmypaint
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libmypaint
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gegl-devel >= 0.4.14
Requires:	glib2-devel >= 2.0
Requires:	json-c-devel
%{?with_openmp:Requires:	libgomp-devel}

%description devel
This package contains files needed for development with libmypaint.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki niezbędne do tworzenia oprogramowania
wykorzystujących bibliotekę libmypaint.

%package apidocs
Summary:	API documentation for libmypaint library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libmypaint
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libmypaint library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmypaint.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-docs} \
	--enable-gegl \
	--enable-introspection \
	%{?with_openmp:--enable-openmp}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmypaint*.la

# unify name
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{nn_NO,nn}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc COPYING README.md TODO
%attr(755,root,root) %{_libdir}/libmypaint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmypaint.so.0
%attr(755,root,root) %{_libdir}/libmypaint-gegl.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libmypaint-gegl.so.0
%{_libdir}/girepository-1.0/MyPaint-1.6.typelib
%{_libdir}/girepository-1.0/MyPaintGegl-1.6.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmypaint.so
%attr(755,root,root) %{_libdir}/libmypaint-gegl.so
%{_includedir}/libmypaint
%{_includedir}/libmypaint-gegl
%{_pkgconfigdir}/libmypaint.pc
%{_pkgconfigdir}/libmypaint-gegl.pc
%{_datadir}/gir-1.0/MyPaint-1.6.gir
%{_datadir}/gir-1.0/MyPaintGegl-1.6.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/{search,*.css,*.html,*.js,*.png}
%endif
