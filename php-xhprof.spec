%define modname xhprof
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B22_%{modname}.ini

Summary:	A Hierarchical Profiler for PHP
Name:		php-%{modname}
Version:	0.9.2
Release:	%mkrel 3
Group:		Development/PHP
License:	Apache License
URL:		http://pecl.php.net/package/xhprof/
Source0:	http://pecl.php.net/get/xhprof-%{version}.tgz
Source1:	B22_xhprof.ini
Patch0:		xhprof-0.9.2-make_it_php_aware.diff
Patch1:		xhprof-0.9.2-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
XHProf is a function-level hierarchical profiler for PHP and has a simple
HTML based navigational interface. The raw data collection component is
implemented in C (as a PHP extension). The reporting/UI layer is all in PHP.

It is capable of reporting function-level inclusive and exclusive wall times,
memory usage, CPU times and number of calls for each function. Additionally,
it supports ability to compare two runs (hierarchical DIFF reports), or
aggregate results from multiple runs.

%prep

%setup -q -n %{modname}-%{version}
%patch0 -p1
%patch1 -p0

mv extension/* .

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

install -d %{buildroot}%{_datadir}/php/xhprof
cp -rp xhprof_lib/* %{buildroot}%{_datadir}/php/xhprof/

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG CREDITS LICENSE README xhprof_html/* examples/*
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
%{_datadir}/php/xhprof

