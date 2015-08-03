#
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	The C++ Network Library Project
Name:		cpp-netlib
Version:	0.11.1
Release:	1
License:	Boost Software License
Group:		Libraries
Source0:	https://github.com/cpp-netlib/cpp-netlib/archive/%{name}-%{version}-final.tar.gz
# Source0-md5:	72f3653254935038876b867417de8c74
URL:		http://cpp-netlib.org/
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Unresolved symbols boost::system::system_category(), boost::system::generic_category()
%define		skip_post_check_so	libcppnetlib-client-connections.so.0.11.0

%description
The project aims to build upon the latest C++ standard (currently
C++11) to provide easy to use libraries for network programming. We
use the latest compiler versions and features with an eye on pushing
the boundaries on leveraging what's available in C++.

Currently the library contains an HTTP client and server
implementation, a stand-alone URI library, a network message
framework, and some concurrency tools.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -qc
mv cpp-netlib-cpp-netlib-%{version}-final/* .

%build
install -d build
cd build
%cmake \
	-DINSTALL_CMAKE_DIR=%{_datadir}/cmake/Modules \
	..
%{__make}
%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.rst RATIONALE.txt LICENSE_1_0.txt
%attr(755,root,root) %{_libdir}/libcppnetlib-client-connections.so.*.*.*
%ghost %{_libdir}/libcppnetlib-client-connections.so.0
%attr(755,root,root) %{_libdir}/libcppnetlib-server-parsers.so.*.*.*
%ghost %{_libdir}/libcppnetlib-server-parsers.so.0
%attr(755,root,root) %{_libdir}/libcppnetlib-uri.so.*.*.*
%ghost %{_libdir}/libcppnetlib-uri.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcppnetlib-client-connections.so
%{_libdir}/libcppnetlib-server-parsers.so
%{_libdir}/libcppnetlib-uri.so
%{_includedir}/boost/*.hpp
%{_includedir}/boost/network
%{_datadir}/cmake/Modules/cppnetlibConfig.cmake
%{_datadir}/cmake/Modules/cppnetlibConfigVersion.cmake
%{_datadir}/cmake/Modules/cppnetlibTargets-pld.cmake
%{_datadir}/cmake/Modules/cppnetlibTargets.cmake
