Summary:	Virtual Smart Card Emulator library
Summary(pl.UTF-8):	Biblioteka emulator wirtualnych kart procesorowych
Name:		libcacard
Version:	0.1.2
Release:	1
License:	GPL v3
Group:		Libraries
Source0:	http://spice-space.org/download/libcacard/%{name}-%{version}.tar.gz
# Source0-md5:	d06480131936ea45a60e98c87b2bb4d9
Patch0:		%{name}-sh.patch
Patch1:		%{name}-pcsc.patch
URL:		http://spice-space.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	nss-devel
BuildRequires:	pcsc-lite-devel >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This emulator is designed to provide emulation of actual smart cards
to a virtual card reader running in a guest virtual machine. The
emulated smart cards can be representations of real smart cards, where
the necessary functions such as signing, card removal/insertion, etc.
are mapped to real, physical cards which are shared with the client
machine the emulator is running on, or the cards could be pure
software constructs.

%description -l pl.UTF-8
Ten pakiet ma na celu zapewnienie emulacji kart procesorowych w
wirtualnym czytniku kart działającym na wirtualnej maszynie-gościu.
Emulowane karty procesorowe mogą reprezentować prawdziwe karty
procesorowe, których potrzebne funkcje, takie jak podpisywanie,
wyjęcie/włożenie karty itp. są odwzorowywane na prawdziwe karty
współdzielone z maszyną kliencką, na której działa emulator, lub
karty czysto programowe.

%package devel
Summary:	Header files for cacard library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki cacard
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	nss-devel
Requires:	pcsc-lite-devel >= 1.6

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
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-passthru
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
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/vscclient
%attr(755,root,root) %{_libdir}/libcacard.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcacard.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcacard.so
%{_includedir}/cacard
%{_pkgconfigdir}/libcacard.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcacard.a
