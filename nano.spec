%bcond_with tiny

Name:		nano
Version:	2.3.1
Release:	%mkrel 1
Summary:	Tiny console text editor that aims to emulate Pico
License:	GPLv3
Group:		Editors
URL:		http://www.nano-editor.org/
Source0:	http://www.nano-editor.org/dist/v2.3/%{name}-%{version}.tar.gz
Patch0:		nano-2.3.0-warnings.patch
# http://lists.gnu.org/archive/html/nano-devel/2010-08/msg00004.html
Patch1:		0001-check-stat-s-result-and-avoid-calling-stat-on-a-NULL.patch
# http://lists.gnu.org/archive/html/nano-devel/2010-08/msg00005.html
Patch2:		0002-use-futimens-if-available-instead-of-utime.patch
%if %{mdvver} < 201200
Requires(post):		info-install
Requires(preun):	info-install
%endif
BuildRequires:	ncurses-devel
BuildRequires:	ncursesw-devel

%description
nano (Nano's ANOther editor) is the editor formerly known as 
TIP (TIP Isn't Pico). It aims to emulate Pico as closely as 
possible while also offering a few enhancements.

Build Options:
--with tiny     builds a minimal editor without extra functionality

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure2_5x \
%if %with tiny
        --enable-tiny
%else
        --enable-all
%endif
%make

%install
%__rm -rf %{buildroot}
%makeinstall_std

#config file
%__install -Dpm644 doc/nanorc.sample %{buildroot}%{_sysconfdir}/nanorc

#disable line wrapping by default
%__sed -i -e 's/# set nowrap/set nowrap/' %{buildroot}%{_sysconfdir}/nanorc

%find_lang %{name} --with-man --all-name

%if %{mdvver} < 201200
%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info
%endif

%clean
%__rm -rf %{buildroot}

%files -f %{name}.lang
%doc AUTHORS BUGS ChangeLog NEWS README THANKS TODO UPGRADE
%doc doc/faq.html doc/nanorc.sample
%{_bindir}/nano
%{_bindir}/rnano
%{_datadir}/nano
%{_infodir}/nano.info*
%{_mandir}/man1/nano.1*
%{_mandir}/man1/rnano.1*
%{_mandir}/man5/nanorc.5*
%config(noreplace) %{_sysconfdir}/nanorc

