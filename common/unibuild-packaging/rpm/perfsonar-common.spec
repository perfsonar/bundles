%define perfsonar_auto_version 5.0.1
%define perfsonar_auto_relnum 0.a1.0

Version:        %{perfsonar_auto_version}
Name:           perfsonar-common
Summary:        Package common to all perfSONAR tools
Release:        %{perfsonar_auto_relnum}%{?dist}
License:        ASL 2.0
Group:          Applications/Communications
URL:            http://www.perfsonar.net/
BuildArch:      noarch
Requires:       coreutils
Requires(pre):  coreutils
Requires(post): coreutils
Obsoletes:      perfSONAR-Bundles-common
Provides:       perfSONAR-Bundles-common

%description
Package common to all perfsonar tools. Creates users, groups, logging directories, etc.

%pre
/usr/sbin/groupadd -r perfsonar 2> /dev/null || :
/usr/sbin/useradd -g perfsonar -r -s /sbin/nologin -c "perfSONAR User" -d /tmp perfsonar 2> /dev/null || :

%post
mkdir -p /var/log/perfsonar
chown perfsonar:perfsonar /var/log/perfsonar
mkdir -p /var/lib/perfsonar/bundles

%files
%defattr(0644,perfsonar,perfsonar,0755)

%changelog
* Fri Oct 15 2021 daniel.neto@rnp.br
- Add logstash configuration
* Mon Jul 14 2015 andy@es.net
- common bundle
* Mon Jul 06 2015 adelvaux@man.poznan.pl
- Tools bundle
* Wed Mar 25 2015 sowmya@es.net
- Core bundle
* Tue Mar 24 2015 sowmya@es.net
- Testpoint and CentralManagement bundle
