%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
# Globals Declaration


%global pname sahara-plugin-vanilla
%global module sahara_plugin_vanilla

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate pylint whereto
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global with_doc 1
# guard for packages OSP does not ship
%global rhosp 0

%global common_desc \
The Vanilla plugin for Sahara allows Sahara to provision and \
manage Vanilla clusters on OpenStack.

Name:          python-sahara-plugin-vanilla
Version:       XXX
Release:       XXX
Summary:       Apache Hadoop cluster management on OpenStack
License:       Apache-2.0
URL:           https://launchpad.net/sahara
Source0:       https://tarballs.openstack.org/%{pname}/%{pname}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pname}/%{pname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:     noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:    git-core
BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
BuildRequires:    openstack-macros


%description
%{common_desc}


%package -n python3-%{pname}
Summary:          Vanilla plugin for Sahara

# Extend the Sahara api and engine packages
Supplements:      openstack-sahara-api
Supplements:      openstack-sahara-engine
Supplements:      openstack-sahara-image-pack

%description -n python3-%{pname}
%{common_desc}


%package -n python3-%{pname}-tests-unit
Summary:        Tests of the Vanilla plugin for Sahara
Requires:       python3-%{pname} = %{version}-%{release}

%description -n python3-%{pname}-tests-unit
%{common_desc}

This package contains the test files of the Vanilla plugin for Sahara.


%if 0%{?with_doc}

%package -n python-%{pname}-doc
Group:         Documentation
Summary:       Usage documentation for the Vanilla plugin for Sahara
Requires:      python3-%{pname} = %{version}-%{release}
%description -n python-%{pname}-doc
%{common_desc}

This documentation provides details about the Vanilla plugin for Sahara.

%endif


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pname}-%{upstream_version} -S git


# set executable on these files to suppress rpmlint warnings, they are used as
# templates to create shell scripts.
chmod a+x sahara_plugin_vanilla/plugins/vanilla/hadoop2/resources/post_conf.template
chmod a+x sahara_plugin_vanilla/plugins/vanilla/hadoop2/resources/tmp-cleanup.sh.template


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel


%if 0%{?with_doc}
export PYTHONPATH=.
%tox -e docs
rm -rf doc/build/html/.{doctrees,buildinfo}
sphinx-build -W -b man doc/source doc/build/man
%endif


%install
%pyproject_install


%if 0%{?with_doc}
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif


# TODO: re-enable when the split version of sahara.git is packaged
#%check
#export PATH=$PATH:%{buildroot}/usr/bin
#export PYTHONPATH=$PWD
#stestr run


%files -n python3-%{pname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-%{upstream_version}.dist-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{pname}-tests-unit
%license LICENSE
%{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html
%{_mandir}/man1/%{pname}.1.gz
%endif


%changelog
