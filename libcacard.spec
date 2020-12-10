#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	CAC (Common Access Card) library
Summary(pl.UTF-8):	Biblioteka CAC (Common Access Library) - ogólny dostęp do kart procesorowych
Name:		libcacard
Version:	2.8.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://www.spice-space.org/download/libcacard/%{name}-%{version}.tar.xz
# Source0-md5:	71ac03db1786bdd891d8185a2524909f
URL:		https://www.spice-space.org/
BuildRequires:	glib2-devel >= 1:2.32
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	nss-devel >= 1:3.12.8
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.32
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
Requires:	glib2-devel >= 1:2.32
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

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	-Ddisable_tests=true \
	-Dpcsc=enabled

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README.md
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
