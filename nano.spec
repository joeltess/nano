%bcond_with tiny

Name:           nano
Version:        2.2.3
Release:        %mkrel 1
Summary:        Tiny console text editor that aims to emulate Pico 
License:        GPLv3
Group:          Editors
URL:            http://www.nano-editor.org/
Source0:        http://www.nano-editor.org/dist/v2.2/nano-%{version}.tar.gz
Requires(post): info-install
Requires(preun): info-install
BuildRequires:	ncurses-devel
BuildRequires:  ncursesw-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
nano (Nano's ANOther editor) is the editor formerly known as 
TIP (TIP Isn't Pico). It aims to emulate Pico as closely as 
possible while also offering a few enhancements.

Build Options:
--with tiny     builds a minimal editor without extra functionality

%prep
%setup -q

%build
%configure2_5x \
%if %with tiny
        --enable-tiny
%else
        --enable-all
%endif
%make

%install
%{__rm} -rf %{buildroot}
%makeinstall_std

%{__mkdir_p} %{buildroot}%{_sysconfdir}
%{__cp} -a doc/nanorc.sample %{buildroot}%{_sysconfdir}/nanorc

%find_lang %{name}

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%clean
%{__rm} -rf %{buildroot} 

%files -f %{name}.lang
%defattr(0644,root,root,0755)
%doc ABOUT-NLS AUTHORS BUGS COPYING ChangeLog INSTALL NEWS README THANKS TODO UPGRADE nano.spec doc/faq.html
%attr(0755,root,root) %{_bindir}/nano
%attr(0755,root,root) %{_bindir}/rnano
%{_datadir}/nano
%{_infodir}/nano.info*
%{_mandir}/man1/nano.1*
%{_mandir}/man1/rnano.1*
%{_mandir}/man5/nanorc.5*
%lang(fr) %{_mandir}/fr/man1/nano.1*
%lang(fr) %{_mandir}/fr/man1/rnano.1*
%lang(fr) %{_mandir}/fr/man5/nanorc.5*
%config(noreplace) %{_sysconfdir}/nanorc
