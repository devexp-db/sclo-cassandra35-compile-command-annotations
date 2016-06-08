Name:          compile-command-annotations
Version:       1.2.0
Release:       1%{?dist}
Summary:       Hotspot compile command annotations
License:       ASL 2.0
URL:           https://github.com/nicoulaj/compile-command-annotations
Source0:       https://github.com/nicoulaj/compile-command-annotations/archive/%{version}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(commons-io:commons-io)
#BuildRequires: mvn(org.apache.maven.plugins:maven-invoker-plugin)
BuildRequires: mvn(org.assertj:assertj-core)
BuildRequires: mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires: mvn(org.codehaus.mojo:exec-maven-plugin)
BuildRequires: mvn(org.testng:testng)
# For IT suite
#BuildRequires: mvn(org.codehaus.groovy:groovy)

BuildArch:     noarch

%description
Annotation based configuration file generator for the
Hotspot JVM JIT compiler.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}

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

%mvn_file net.ju-n.compile-command-annotations:%{name} %{name}

%build

%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license COPYING

%files javadoc -f .mfiles-javadoc
%license COPYING

%changelog
* Mon Jul 20 2015 gil cattaneo <puntogil@libero.it> 1.2.0-1
- initial rpm
