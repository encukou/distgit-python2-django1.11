%global         pkgname Django


Name:           python2-django1.11

Version:        1.11.9
Release:        1%{?dist}
Summary:        Version 1.11 LTS of Django, a high-level Python Web framework

Group:          Development/Languages
License:        BSD
URL:            http://www.djangoproject.com/
Source0:        https://files.pythonhosted.org/packages/source/D/Django/Django-%{version}.tar.gz


BuildArch:      noarch


BuildRequires:  python2-devel
BuildRequires:  python2-bcrypt
BuildRequires:  %{_bindir}/pathfix.py

# test requirements
BuildRequires:  python2-docutils
BuildRequires:  python2-jinja2
BuildRequires:  python2-mock
BuildRequires:  python2-numpy
BuildRequires:  python2-pillow
BuildRequires:  python2-pyyaml
BuildRequires:  python2-pytz
BuildRequires:  python2-selenium
BuildRequires:  python2-sqlparse
BuildRequires:  python2-memcached

Requires:       python2-pytz
Obsoletes:      python-django < 2
Obsoletes:      python2-django < 2

Provides: bundled(jquery) = 2.2.3
Provides: bundled(xregexp) = 2.0.0


%description
This package provides Django in version 1.11 LTS, the last release
to support Python 2.

Django is a high-level Python Web framework that encourages rapid
development and a clean, pragmatic design. It focuses on automating as
much as possible and adhering to the DRY (Don't Repeat Yourself)
principle.


%package doc
Summary:        Documentation for Django, version 1.11 LTS
Requires:       %{name} = %{version}-%{release}

BuildRequires:  python2-sphinx

%description doc
This package contains the documentation for the Django high-level
Python Web framework, version 1.11 LTS.


%prep
%autosetup -n %{pkgname}-%{version}

# Remove stray executable bit
chmod -v -x django/contrib/admin/static/admin/js/vendor/xregexp/xregexp.js


%build
%py2_build


%install

%py2_install

%find_lang django
%find_lang djangojs
# append djangojs.lang to django.lang
cat djangojs.lang >> django.lang

# build documentation
(cd docs && mkdir djangohtml && mkdir -p _build/{doctrees,html} && make html)

# Fix admin script in %%{_bindir}
mv %{buildroot}%{_bindir}/django-admin %{buildroot}%{_bindir}/django-admin-1.11
rm %{buildroot}%{_bindir}/django-admin.py

# Man page for django-admin-1.11 is not packaged -- the dot & number don't
# play well with man

# remove .po files
find %{buildroot} -name "*.po" | xargs rm -f

# Fix shebang in internal script
pathfix.py -i %{__python2} -p %{buildroot}%{python2_sitelib}/django/bin/*

# Remove stray backup file
rm -f %{buildroot}%{python2_sitelib}/django/bin/*~


%check
export PYTHONPATH=$(pwd)
export LANG=en_US.utf8
cd tests
%{__python2} ./runtests.py --settings=test_sqlite --verbosity=2 --parallel 1


%files -f django.lang
%doc AUTHORS README.rst
%license LICENSE
%{_bindir}/django-admin-1.11

%{python2_sitelib}/django/
# Note: this duplicates files in %%find_lang
# The macro is meant to make it easy for packages to own .mo files in:
#    %%{_datadir}/locale/??/LC_MESSAGES/*.mo
# ... but not the LC_MESSAGES directory itself.
# But Django's lang files are in site-packages/django, and we own all of that.
# This does cause harmless build warnings about duplicate files.

%{python2_sitelib}/*.egg-info


%files doc
%doc docs/_build/html/*


%changelog
* Wed Dec 13 2017 Petr Viktorin <pviktori@redhat.com> - 1.11.9-1
- Initial compat package
- Based on Fedora's python-django 1.11.5-1; updated to 1.11.9
