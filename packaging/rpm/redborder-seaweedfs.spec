%define debug_package %{nil}
# SeaweedFS release built from source (Source1, checked by sha256 in %%prep)
%global weed_version 4.55
%global weed_sha256 725282228d39edc4327bbba4e4a31867660cafbec6adb5f43005ba3e3960d25c

Name: redborder-seaweedfs
Version: %{__version}
Release: %{__release}%{?dist}
ExclusiveArch: x86_64
Summary: SeaweedFS %{weed_version} (S3 object storage) for redborder environments

# weed is Apache 2.0, the redborder units and scripts are AGPL 3.0
License: ASL 2.0 and AGPL 3.0
URL: https://github.com/redBorder/redborder-seaweedfs
Source0: %{name}-%{version}.tar.gz
Source1: https://github.com/seaweedfs/seaweedfs/archive/refs/tags/%{weed_version}.tar.gz#/seaweedfs-%{weed_version}.tar.gz

BuildRequires: golang >= 1.26.6
BuildRequires: systemd
BuildRequires: git

Requires(pre): shadow-utils
Requires: bash

Provides: seaweedfs = %{weed_version}

%description
SeaweedFS %{weed_version} built from source, with the systemd units used by redborder:
seaweedfs-master, seaweedfs-volume and seaweedfs-filer (filer with the S3 gateway).
The cookbook seaweedfs writes the options of each unit in /etc/default/seaweedfs-*
and the configuration files in /etc/seaweedfs.

%prep
echo "%{weed_sha256}  %{SOURCE1}" | sha256sum -c -
%setup -qn %{name}-%{version}
%setup -qn %{name}-%{version} -T -D -a 1

%build
cd seaweedfs-%{weed_version}/weed
# The go modules are downloaded during the build and checked against go.sum
export GOFLAGS="-mod=readonly -trimpath"
export GOPATH=$(pwd)/../../.gopath
export GOCACHE=$(pwd)/../../.gocache
export CGO_ENABLED=0
go build -ldflags "-s -w -X github.com/seaweedfs/seaweedfs/weed/util/version.COMMIT=redborder-%{version}-%{release}" -o weed .
./weed version

%install
install -D -m 0755 seaweedfs-%{weed_version}/weed/weed %{buildroot}%{_bindir}/weed
install -D -m 0644 resources/systemd/seaweedfs-master.service %{buildroot}%{_unitdir}/seaweedfs-master.service
install -D -m 0644 resources/systemd/seaweedfs-volume.service %{buildroot}%{_unitdir}/seaweedfs-volume.service
install -D -m 0644 resources/systemd/seaweedfs-filer.service %{buildroot}%{_unitdir}/seaweedfs-filer.service
mkdir -p %{buildroot}/etc/seaweedfs
mkdir -p %{buildroot}/var/lib/seaweedfs/master
mkdir -p %{buildroot}/var/lib/seaweedfs/volume
mkdir -p %{buildroot}/var/lib/seaweedfs/filer
install -D -m 0644 seaweedfs-%{weed_version}/LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE.seaweedfs

%pre
getent group seaweedfs >/dev/null || groupadd -r seaweedfs
getent passwd seaweedfs >/dev/null || \
    useradd -r -g seaweedfs -d /var/lib/seaweedfs -s /sbin/nologin \
    -c "User for SeaweedFS" seaweedfs
exit 0

%post
%systemd_post seaweedfs-master.service seaweedfs-volume.service seaweedfs-filer.service

%preun
%systemd_preun seaweedfs-master.service seaweedfs-volume.service seaweedfs-filer.service

%postun
%systemd_postun_with_restart seaweedfs-master.service seaweedfs-volume.service seaweedfs-filer.service

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/weed
%{_unitdir}/seaweedfs-master.service
%{_unitdir}/seaweedfs-volume.service
%{_unitdir}/seaweedfs-filer.service
%license %{_datadir}/licenses/%{name}/LICENSE.seaweedfs
%dir %attr(0750,root,seaweedfs) /etc/seaweedfs
%dir %attr(0750,seaweedfs,seaweedfs) /var/lib/seaweedfs
%dir %attr(0750,seaweedfs,seaweedfs) /var/lib/seaweedfs/master
%dir %attr(0750,seaweedfs,seaweedfs) /var/lib/seaweedfs/volume
%dir %attr(0750,seaweedfs,seaweedfs) /var/lib/seaweedfs/filer

%changelog
* Thu Nov 26 2026 Miguel Negrón <manegron@redborder.com> 1.0.0
- First version: SeaweedFS 4.55 built from source with the master, volume and filer (S3) units
