#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	CAC (Common Access Card) library
Summary(pl.UTF-8):	Biblioteka CAC (Common Access Library) - ogólny dostęp do kart procesorowych
Name:		libcacard
Version:	2.5.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.spice-space.org/download/libcacard/%{name}-%{version}.tar.xz
# Source0-md5:	8b6fb1b0fef660b6e5d7a1fe42f5349b
URL:		http://www.spice-space.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	autoconf-archive >= 2015.09.25
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.22
BuildRequires:	libtool >= 2:2
BuildRequires:	nss-devel >= 1:3.12.8
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.22
Requires:	nss >= 1:3.12.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library provides emulation of smart cards to a virtual card
reader running in a guest virtual machine.

It implements DoD CAC standard with separate PKI containers
(compatible coolkey), using certificates read from NSS.

%description -l pl.UTF-8
Ta biblioteka zapewnia emulację kart procesorowych dla wirtualnego
czytnika kart działającego na maszynie wirtualnej gościa.

Implementuje standard CAC DoD z osobnymi kontenerami PKI (zgodny
coolkey) przy użyciu certyfikatów odczytywanych z NSS.

%package devel
Summary:	Header files for cacard library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki cacard
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.22
Requires:	nss-devel >= 1:3.12.8

%description devel
Header files for cacard library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki cacard.

%package static
Summary:	Static cacard library
Summary(pl.UTF-8):	Statyczna biblioteka cacard
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static cacard library.

%description static -l pl.UTF-8
Statyczna biblioteka cacard.

%prep
%setup -q

# take version from .tarball-version instead of using missing git-related script
%{__sed} -i -e '1s,build-aux/git-version-gen,tr -d "\\n" <,' configure.ac

# force new version from autoconf-archive (original one uses non-POSIX ${V:N} syntax)
%{__rm} m4/ax_compiler_flags_cflags.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcacard.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README.md
%attr(755,root,root) %{_bindir}/vscclient
%attr(755,root,root) %{_libdir}/libcacard.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcacard.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcacard.so
%{_includedir}/cacard
%{_pkgconfigdir}/libcacard.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcacard.a
%endif
