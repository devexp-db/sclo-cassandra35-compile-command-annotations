%{?scl:%scl_package compile-command-annotations}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}compile-command-annotations
Version:	1.2.0
Release:	4%{?dist}
Summary:	Hotspot compile command annotations
License:	ASL 2.0
URL:		https://github.com/nicoulaj/%{pkg_name}
Source0:	https://github.com/nicoulaj/%{pkg_name}/archive/%{version}.tar.gz

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}maven-plugin-build-helper
BuildRequires:	%{?scl_prefix_maven}exec-maven-plugin
BuildRequires:	%{?scl_prefix}guava
BuildRequires:	%{?scl_prefix_java_common}apache-commons-io
BuildRequires:	%{?scl_prefix_maven}testng
BuildRequires:	%{?scl_prefix}assertj-core
BuildRequires:	%{?scl_prefix_maven}mockito
BuildRequires:	%{?scl_prefix}cglib
# For IT suite
#BuildRequires:	mvn(org.codehaus.groovy:groovy)
%{?scl:Requires: %scl_runtime}

BuildArch:	noarch

%description
Annotation based configuration file generator for the
Hotspot JVM JIT compiler.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{pkg_name}-%{version}

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# net.ju-n:net-ju-n-parent:32
%pom_remove_parent

# Prevent IT failures
#find ./src/it/tests -name "pom.xml" -exec sed -i "s/@project.build.sourceEncoding@/UTF-8/g" {} +
#find ./src/it/tests -name "pom.xml" -exec sed -i "s/@exec-maven-plugin.version@/1.4.0/g" {} +
#find ./src/it/tests -name "pom.xml" -exec sed -i "s/@maven-compiler-plugin.version@/3.3/g" {} +
# Fails on koji only
%pom_remove_plugin :maven-invoker-plugin

# TestNG support requires version 4.7 or above
%pom_change_dep :testng ::6.8.21

# org.easytesting:fest-assert-core:2.0M10
# https://github.com/nicoulaj/compile-command-annotations/issues/8
%pom_xpath_remove pom:fest-assert.version
%pom_xpath_inject pom:properties "<assertj-core.version>2.2.0</assertj-core.version>"
%pom_change_dep :fest-assert-core org.assertj:assertj-core:'${assertj-core.version}'
find ./ -name "*.java" -exec sed -i "s/org.fest.assertions/org.assertj.core/g" {} +

%mvn_file net.ju-n.%{pkg_name}:%{pkg_name} %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc README.md
%license COPYING

%files javadoc -f .mfiles-javadoc
%license COPYING

%changelog
* Wed Mar 29 2017 Tomas Repik <trepik@redhat.com> - 1.2.0-4
- use newly added assertj-core and run tests

* Tue Oct 11 2016 Tomas Repik <trepik@redhat.com> - 1.2.0-3
- use standard SCL macros

* Wed Aug 03 2016 Tomas Repik <trepik@redhat.com> - 1.2.0-2
- scl conversion

* Mon Jul 20 2015 gil cattaneo <puntogil@libero.it> 1.2.0-1
- initial rpm
