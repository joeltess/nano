%define directory_down %(echo %version|perl -n -e  '/^(\d+\.\d+).*$/; print \$1 ')

%bcond_with tiny

Summary:        Nano is a tiny console text editor that aims to emulate Pico 
Name:           nano
Version:        2.0.3
Release:        %mkrel 1
License:        GPL
Group:          Editors
URL:            http://www.nano-editor.org/
Source0:        http://www.nano-editor.org/dist/v2.0/nano-%{version}.tar.gz
Source1:        http://www.nano-editor.org/dist/v2.0/nano-%{version}.tar.gz.asc
Source2:        http://www.nano-editor.org/dist/v2.0/nano-%{version}.tar.gz.md5
Requires(post): rpm-helper
Requires(postun): rpm-helper
BuildRequires:  ncurses-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
nano (Nano's ANOther editor) is the editor formerly known as 
TIP (TIP Isn't Pico). It aims to emulate Pico as closely as 
possible while also offering a few enhancements.

Build Options:
--with tiny      builds a minimal editor without extra functionality

%prep
%setup -q

%build
%{configure2_5x} \
%if %with tiny
        --enable-tiny
%else
        --enable-all
%endif
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

%{__mkdir_p} %{buildroot}%{_sysconfdir}
%{__cp} -a doc/nanorc.sample %{buildroot}%{_sysconfdir}/nanorc

%find_lang %{name}

%post
%_install_info %{name}.info

%postun
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


