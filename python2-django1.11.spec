%global         pkgname Django


Name:           python2-django1.11

Version:        1.11.5
Release:        2%{?dist}
Summary:        Version 1.11 LTS of Django, a high-level Python Web framework

Group:          Development/Languages
License:        BSD
URL:            http://www.djangoproject.com/
Source0:        https://files.pythonhosted.org/packages/source/D/Django/Django-%{version}.tar.gz


BuildArch:      noarch


BuildRequires:  python2-devel
BuildRequires:  python2-bcrypt

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
BuildRequires:  python-memcached
Requires:       python2-pytz

Obsoletes:      python-django < 2
Obsoletes:      python2-django < 2

Provides: bundled(jquery) = 2.2.3
Provides: bundled(xregexp) = 2.0.0

Requires:       %{name}-bash-completion = %{version}-%{release}


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

BuildRequires:  python-sphinx

%description doc
This package contains the documentation for the Django high-level
Python Web framework, version 1.11 LTS.



%package bash-completion
Summary:        bash completion files for Django, version 1.11 LTS
BuildRequires:  bash-completion


%description bash-completion
This package contains the bash completion files form Django high-level
Python Web framework, version 1.11 LTS.

%prep
%autosetup -n %{pkgname}-%{version}



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
cp -ar docs ..

# install bash completion script
bashcompdir=$(pkg-config --variable=completionsdir bash-completion)
mkdir -p %{buildroot}$bashcompdir
install -m 0644 -p extras/django_bash_completion \
  %{buildroot}$bashcompdir/django-admin-1.11

# Fix admin script in %%{_bindir}
mv %{buildroot}%{_bindir}/django-admin %{buildroot}%{_bindir}/django-admin-1.11
rm %{buildroot}%{_bindir}/django-admin.py
# Man page for django-admin-1.11 is not packaged -- the dot & number don't
# play well with man

# remove .po files
find $RPM_BUILD_ROOT -name "*.po" | xargs rm -f


%check
export PYTHONPATH=$(pwd)
export LANG=en_US.utf8
cd tests
%{__python} ./runtests.py --settings=test_sqlite --verbosity=2 --parallel 1


%files -f django.lang
%doc AUTHORS README.rst
%license LICENSE
%{_bindir}/django-admin-1.11
%attr(0755,root,root) %{python2_sitelib}/django/bin/django-admin.py*
# Include everything but the locale data ...
%dir %{python2_sitelib}/django
%dir %{python2_sitelib}/django/bin
%{python2_sitelib}/django/apps
%{python2_sitelib}/django/db/
%{python2_sitelib}/django/*.py*
%{python2_sitelib}/django/utils/
%{python2_sitelib}/django/dispatch/
%{python2_sitelib}/django/template/
%{python2_sitelib}/django/views/
%{python2_sitelib}/django/urls/
%dir %{python2_sitelib}/django/conf/
%dir %{python2_sitelib}/django/conf/locale/
%dir %{python2_sitelib}/django/conf/locale/??/
%dir %{python2_sitelib}/django/conf/locale/??_*/
%dir %{python2_sitelib}/django/conf/locale/*/LC_MESSAGES
%dir %{python2_sitelib}/django/contrib/
%{python2_sitelib}/django/contrib/*.py*
%dir %{python2_sitelib}/django/contrib/admin/
%dir %{python2_sitelib}/django/contrib/admin/locale
%dir %{python2_sitelib}/django/contrib/admin/locale/??/
%dir %{python2_sitelib}/django/contrib/admin/locale/??_*/
%dir %{python2_sitelib}/django/contrib/admin/locale/*/LC_MESSAGES
%{python2_sitelib}/django/contrib/admin/*.py*
%{python2_sitelib}/django/contrib/admin/migrations
%{python2_sitelib}/django/contrib/admin/views/
%{python2_sitelib}/django/contrib/admin/static/
%{python2_sitelib}/django/contrib/admin/templatetags/
%{python2_sitelib}/django/contrib/admin/templates/
%dir %{python2_sitelib}/django/contrib/admindocs/
%dir %{python2_sitelib}/django/contrib/admindocs/locale/
%dir %{python2_sitelib}/django/contrib/admindocs/locale/??/
%dir %{python2_sitelib}/django/contrib/admindocs/locale/??_*/
%dir %{python2_sitelib}/django/contrib/admindocs/locale/*/LC_MESSAGES
%{python2_sitelib}/django/contrib/admindocs/*.py*
%{python2_sitelib}/django/contrib/admindocs/templates/
%dir %{python2_sitelib}/django/contrib/auth/
%dir %{python2_sitelib}/django/contrib/auth/locale/
%dir %{python2_sitelib}/django/contrib/auth/locale/??/
%dir %{python2_sitelib}/django/contrib/auth/locale/??_*/
%dir %{python2_sitelib}/django/contrib/auth/locale/*/LC_MESSAGES
%{python2_sitelib}/django/contrib/auth/*.py*
%{python2_sitelib}/django/contrib/auth/common-passwords.txt.gz
%{python2_sitelib}/django/contrib/auth/handlers/
%{python2_sitelib}/django/contrib/auth/management/
%{python2_sitelib}/django/contrib/auth/migrations/
%{python2_sitelib}/django/contrib/auth/templates/
%{python2_sitelib}/django/contrib/auth/tests/
%dir %{python2_sitelib}/django/contrib/contenttypes/
%dir %{python2_sitelib}/django/contrib/contenttypes/locale
%dir %{python2_sitelib}/django/contrib/contenttypes/locale/??/
%dir %{python2_sitelib}/django/contrib/contenttypes/locale/??_*/
%dir %{python2_sitelib}/django/contrib/contenttypes/locale/*/LC_MESSAGES
%{python2_sitelib}/django/contrib/contenttypes/management
%{python2_sitelib}/django/contrib/contenttypes/migrations
%{python2_sitelib}/django/contrib/contenttypes/*.py*
%dir %{python2_sitelib}/django/contrib/flatpages/
%dir %{python2_sitelib}/django/contrib/flatpages/locale/
%dir %{python2_sitelib}/django/contrib/flatpages/locale/??/
%dir %{python2_sitelib}/django/contrib/flatpages/locale/??_*/
%dir %{python2_sitelib}/django/contrib/flatpages/locale/*/LC_MESSAGES
%{python2_sitelib}/django/contrib/flatpages/*.py*
%{python2_sitelib}/django/contrib/flatpages/migrations/
%{python2_sitelib}/django/contrib/flatpages/templatetags
%dir %{python2_sitelib}/django/contrib/gis/
%dir %{python2_sitelib}/django/contrib/gis/locale/
%dir %{python2_sitelib}/django/contrib/gis/locale/??/
%dir %{python2_sitelib}/django/contrib/gis/locale/??_*/
%dir %{python2_sitelib}/django/contrib/gis/locale/*/LC_MESSAGES
%{python2_sitelib}/django/contrib/gis/*.py*
%{python2_sitelib}/django/contrib/gis/geoip/
%{python2_sitelib}/django/contrib/gis/geoip2/
%{python2_sitelib}/django/contrib/gis/serializers/
%{python2_sitelib}/django/contrib/gis/static
%dir %{python2_sitelib}/django/contrib/humanize/
%dir %{python2_sitelib}/django/contrib/humanize/locale/
%dir %{python2_sitelib}/django/contrib/humanize/locale/??/
%dir %{python2_sitelib}/django/contrib/humanize/locale/??_*/
%dir %{python2_sitelib}/django/contrib/humanize/locale/*/LC_MESSAGES
%{python2_sitelib}/django/contrib/humanize/templatetags/
%{python2_sitelib}/django/contrib/humanize/*.py*
%{python2_sitelib}/django/contrib/messages/*.py*
%dir %{python2_sitelib}/django/contrib/postgres/
%{python2_sitelib}/django/contrib/postgres/*.py*
%{python2_sitelib}/django/contrib/postgres/aggregates
%{python2_sitelib}/django/contrib/postgres/jinja2
%{python2_sitelib}/django/contrib/postgres/fields
%{python2_sitelib}/django/contrib/postgres/forms
%{python2_sitelib}/django/contrib/postgres/templates
%dir %{python2_sitelib}/django/contrib/redirects
%dir %{python2_sitelib}/django/contrib/redirects/locale
%dir %{python2_sitelib}/django/contrib/redirects/locale/??/
%dir %{python2_sitelib}/django/contrib/redirects/locale/??_*/
%dir %{python2_sitelib}/django/contrib/redirects/locale/*/LC_MESSAGES
%{python2_sitelib}/django/contrib/redirects/*.py*
%{python2_sitelib}/django/contrib/redirects/migrations
%dir %{python2_sitelib}/django/contrib/sessions/
%dir %{python2_sitelib}/django/contrib/sessions/locale/
%dir %{python2_sitelib}/django/contrib/sessions/locale/??/
%dir %{python2_sitelib}/django/contrib/sessions/locale/??_*/
%dir %{python2_sitelib}/django/contrib/sessions/locale/*/LC_MESSAGES
%{python2_sitelib}/django/contrib/sessions/management/
%{python2_sitelib}/django/contrib/sessions/migrations/
%{python2_sitelib}/django/contrib/sessions/*.py*
%{python2_sitelib}/django/contrib/sitemaps/
%dir %{python2_sitelib}/django/contrib/sites/
%dir %{python2_sitelib}/django/contrib/sites/locale/
%dir %{python2_sitelib}/django/contrib/sites/locale/??/
%dir %{python2_sitelib}/django/contrib/sites/locale/??_*/
%dir %{python2_sitelib}/django/contrib/sites/locale/*/LC_MESSAGES
%{python2_sitelib}/django/contrib/sites/*.py*
%{python2_sitelib}/django/contrib/sites/migrations
%{python2_sitelib}/django/contrib/staticfiles/
%{python2_sitelib}/django/contrib/syndication/
%{python2_sitelib}/django/contrib/gis/admin/
%{python2_sitelib}/django/contrib/gis/db/
%{python2_sitelib}/django/contrib/gis/forms/
%{python2_sitelib}/django/contrib/gis/gdal/
%{python2_sitelib}/django/contrib/gis/geometry/
%{python2_sitelib}/django/contrib/gis/geos/
%{python2_sitelib}/django/contrib/gis/management/
%{python2_sitelib}/django/contrib/gis/sitemaps/
%{python2_sitelib}/django/contrib/gis/templates/
%{python2_sitelib}/django/contrib/gis/utils/
%{python2_sitelib}/django/contrib/messages/storage/
%{python2_sitelib}/django/contrib/sessions/backends/
%{python2_sitelib}/django/forms/
%{python2_sitelib}/django/templatetags/
%{python2_sitelib}/django/core/
%{python2_sitelib}/django/http/
%{python2_sitelib}/django/middleware/
%{python2_sitelib}/django/test/
%{python2_sitelib}/django/conf/*.py*
%{python2_sitelib}/django/conf/project_template/
%{python2_sitelib}/django/conf/app_template/
%{python2_sitelib}/django/conf/urls/
%{python2_sitelib}/django/conf/locale/*/*.py*
%{python2_sitelib}/django/conf/locale/*.py*

%{python2_sitelib}/*.egg-info

%files doc
%doc docs/_build/html/*

%files bash-completion
%{_datadir}/bash-completion


%changelog
* Wed Dec 13 2017 Petr Viktorin <pviktori@redhat.com> - 1.11.5-2
- Initial compat package
- Based on Fedora's python-django 1.11.5-1
