%global commit c1bf10da1873bc212caa857653bef0b1e899703a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global timestamp 1415738661

Summary: NSS library for SecurePass
Name: libnss_sp2
Version: 0.2
Release: 2%{?dist}
Source0: https://github.com/garlsecurity/nss_securepass/archive/%{commit}/nss_securepass-%{timestamp}.%{shortcommit}.tar.gz
URL: https://github.com/garlsecurity/nss_securepass
Group: System Environment/Base
License: GPL-2.0+
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: libcurl-devel

%description
NSS (Name Service Switch) module for SecurePass

SecurePass provides identity management and web single sign-on.

%prep
%setup -qn nss_securepass-%{timestamp}.%{shortcommit}


%build
%configure
make 

%install
[ "%{buildroot}" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/{etc,lib}
mkdir -p %{buildroot}/%{_libdir}

/usr/bin/install -c libnss_sp.so.2 %{buildroot}/%{_libdir}/libnss_sp.so.2
ln -sf libnss_sp.so.2 %{buildroot}/%{_libdir}/libnss_sp.so

install -m 644 securepass.conf.template %{buildroot}/etc/securepass.conf

chmod 755 %{buildroot}/usr/%{_lib}/*.so*

%clean
[ "%{buildroot}" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/*.so*
%attr(0600,root,root) %config(noreplace) /etc/securepass.conf
%doc README.md
%doc securepass.conf.template

%if 0%{?rhel} <= 6
   %doc LICENSE LICENSE_APACHE2 LICENSE_GNUGPL LICENSE_MIT
%else 
   %license LICENSE LICENSE_APACHE2 LICENSE_GNUGPL LICENSE_MIT
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

