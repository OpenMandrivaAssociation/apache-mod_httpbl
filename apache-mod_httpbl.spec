#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_httpbl
%define mod_conf A99_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_httpbl is a DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0
Release:	%mkrel 1
Group:		System/Servers
License:	Apache License
URL:		http://sourceforge.net/projects/httpbl/
Source0:	mod_httpbl_for_apache_2.0.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The mod_httpbl Apache module is ideal for leveraging the Project Honey pot
http:BL services within the context of an Apache web server. Built on the
Apache APIs, the mod enables web admins to block comment spammers, harvesters,
and other malicious IPs.

%prep

%setup -q -n mod_httpbl_for_apache_2.0

cp mod_httpbl_source/mod_httpbl.c .
chmod 644 mod_httpbl_source/install.txt mod_httpbl_manual/mod_httpbl.xml

cp %{SOURCE1} %{mod_conf}

%build

%{_sbindir}/apxs -DDEFAULT_SERVER_ROOT_DIRECTORY=\\\"%{_sysconfdir}/httpd/\\\" -c mod_httpbl.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc mod_httpbl_source/install.txt mod_httpbl_manual/mod_httpbl.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
