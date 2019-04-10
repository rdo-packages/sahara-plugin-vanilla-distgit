# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
# Globals Declaration


%global pname sahara-plugin-vanilla
%global module sahara_plugin_vanilla

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1
# guard for packages OSP does not ship
%global rhosp 0

%if 0%{?rhel} && 0%{?rhel} <= 7
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}}
%endif

%global common_desc \
The Vanilla plugin for Sahara allows Sahara to provision and \
manage Vanilla clusters on OpenStack.

Name:          python-sahara-plugin-vanilla
Version:       1.0.0
Release:       1%{?dist}
Summary:       Apache Hadoop cluster management on OpenStack
License:       ASL 2.0
URL:           https://launchpad.net/sahara
Source0:       https://tarballs.openstack.org/%{pname}/%{pname}-%{upstream_version}.tar.gz
#

BuildArch:     noarch

BuildRequires:    git
BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr >= 2.0.0
BuildRequires:    openstack-macros

# test requirements
BuildRequires:    python%{pyver}-stestr >= 1.0.0
BuildRequires:    python%{pyver}-testscenarios
BuildRequires:    python%{pyver}-oslotest
BuildRequires:    python%{pyver}-hacking
BuildRequires:    python%{pyver}-oslo-i18n >= 3.15.3
BuildRequires:    python%{pyver}-oslo-log >= 3.36.0
BuildRequires:    python%{pyver}-oslo-serialization >= 2.18.0
BuildRequires:    python%{pyver}-oslo-utils >= 3.33.0
BuildRequires:    python%{pyver}-sahara >= 10.0.0


%description
%{common_desc}


%package -n python%{pyver}-%{pname}
Summary:          Vanilla plugin for Sahara
%{?python_provide:%python_provide python%{pyver}-%{pname}}

Requires:         python%{pyver}-babel >= 2.3.4
Requires:         python%{pyver}-eventlet >= 0.18.2
Requires:         python%{pyver}-oslo-i18n >= 3.15.3
Requires:         python%{pyver}-oslo-log >= 3.36.0
Requires:         python%{pyver}-oslo-serialization >= 2.18.0
Requires:         python%{pyver}-oslo-utils >= 3.33.0
Requires:         python%{pyver}-pbr >= 2.0.0
Requires:         python%{pyver}-requests >= 2.14.2
Requires:         python%{pyver}-sahara >= 10.0.0
Requires:         python%{pyver}-six >= 1.10.0

# Extend the Sahara api and engine packages
%if 0%{?fedora} || 0%{?rhel} > 7
Supplements:      openstack-sahara-api
Supplements:      openstack-sahara-engine
%endif

%description -n python%{pyver}-%{pname}
%{common_desc}


%package -n python%{pyver}-%{pname}-tests-unit
Summary:        Tests of the Vanilla plugin for Sahara
%{?python_provide:%python_provide python%{pyver}-%{pname}-tests-unit}
Requires:       python%{pyver}-%{pname} = %{version}-%{release}

%description -n python%{pyver}-%{pname}-tests-unit
%{common_desc}

This package contains the test files of the Vanilla plugin for Sahara.


%if 0%{?with_doc}

%package -n python-%{pname}-doc
Group:         Documentation
Summary:       Usage documentation for the Vanilla plugin for Sahara
Requires:      python%{pyver}-%{pname} = %{version}-%{release}
BuildRequires:    python%{pyver}-reno
BuildRequires:    python%{pyver}-sphinx >= 1.6.2
BuildRequires:    python%{pyver}-openstackdocstheme >= 1.18.1

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-sphinxcontrib-httpdomain
%else
BuildRequires:    python%{pyver}-sphinxcontrib-httpdomain
%endif

%description -n python-%{pname}-doc
%{common_desc}

This documentation provides details about the Vanilla plugin for Sahara.

%endif


%prep
%autosetup -n %{pname}-%{upstream_version} -S git

# let RPM handle deps
%py_req_cleanup

# set executable on these files to suppress rpmlint warnings, they are used as
# templates to create shell scripts.
chmod a+x sahara_plugin_vanilla/plugins/vanilla/hadoop2/resources/post_conf.template
chmod a+x sahara_plugin_vanilla/plugins/vanilla/hadoop2/resources/tmp-cleanup.sh.template


%build
%{pyver_build}


%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}
sphinx-build-%{pyver} -W -b man doc/source doc/build/man
%endif


%install
%{pyver_install}


%if 0%{?with_doc}
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif


# TODO: re-enable when the split version of sahara.git is packaged
#%check
#export PATH=$PATH:%{buildroot}/usr/bin
#export PYTHONPATH=$PWD
#stestr-%{pyver} run


%files -n python%{pyver}-%{pname}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-%{upstream_version}-py?.?.egg-info
%exclude %{pyver_sitelib}/%{module}/tests

%files -n python%{pyver}-%{pname}-tests-unit
%license LICENSE
%{pyver_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html
%{_mandir}/man1/%{pname}.1.gz
%endif


%changelog
* Wed Apr 10 2019 RDO <dev@lists.rdoproject.org> 1.0.0-1
- Update to 1.0.0

* Wed Mar 27 2019 Luigi Toscano <ltoscano@redhat.com> 1.0.0-0.1.0rc1
- Update to 1.0.0.0rc1
