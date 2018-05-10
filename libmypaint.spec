%bcond_with	doc
Summary:	Library for making brush strokes
Name:		libmypaint
Version:	1.3.0
Release:	2
License:	ISC
Group:		Libraries
URL:		https://github.com/mypaint/libmypaint
Source0:	https://github.com/mypaint/libmypaint/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	2e7200c7873514dfca26eea9e3d273f5
Patch0:		%{name}-gegl.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	babl-devel
BuildRequires:	gcc
BuildRequires:	gegl-devel >= 0.4.0
BuildRequires:	glib2-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	intltool
BuildRequires:	json-c-devel
%if %{with doc}
BuildRequires:	doxygen
BuildRequires:	python-breathe
BuildRequires:	sphinx-pdg
%endif
Conflicts:	mypaint < 1.3.0

%description
This is a self-contained library containing the MyPaint brush engine.

%package devel
Summary:	Development files for libmypaint
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package contains files needed for development with libmypaint.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{?with_doc:--enable-docs} \
	--enable-introspection=yes \
	--enable-gegl \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -name '*.la' -delete -print

rm -r $RPM_BUILD_ROOT%{_localedir}/{es_ES,nn_NO}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %ghost %{_libdir}/libmypaint-1.3.so.0
%attr(755,root,root) %{_libdir}/libmypaint-1.3.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libmypaint-gegl.so.0
%attr(755,root,root) %{_libdir}/libmypaint-gegl.so.*.*
%{_libdir}/girepository-1.0/MyPaint-*.typelib
%{_libdir}/girepository-1.0/MyPaintGegl-*.typelib

%files devel
%defattr(644,root,root,755)
%{?with_doc:%doc doc/build/*}
%attr(755,root,root) %{_libdir}/libmypaint.so
%attr(755,root,root) %{_libdir}/libmypaint-gegl.so
%{_includedir}/%{name}
%{_includedir}/%{name}-gegl
%{_pkgconfigdir}/libmypaint.pc
%{_pkgconfigdir}/libmypaint-gegl.pc
%{_datadir}/gir-1.0/MyPaint-*.gir
%{_datadir}/gir-1.0/MyPaintGegl-*.gir
