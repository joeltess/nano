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



%changelog
* Fri Mar 23 2012 Andrey Bondrov <abondrov@mandriva.org> 2.3.1-1
+ Revision: 786455
- New version 2.3.1, sync patches with Mageia/Fedora, add conditions for info-install stuff

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.4-2mdv2011.0
+ Revision: 612998
- the mass rebuild of 2010.1 packages

* Fri Apr 16 2010 Frederik Himpe <fhimpe@mandriva.org> 2.2.4-1mdv2010.1
+ Revision: 535554
- Update to new version 2.2.4 (fixes CVE-2010-1160, CVE-2010-1161)

* Thu Feb 11 2010 Frederik Himpe <fhimpe@mandriva.org> 2.2.3-1mdv2010.1
+ Revision: 504291
- update to new version 2.2.3

* Mon Jan 18 2010 Frederik Himpe <fhimpe@mandriva.org> 2.2.2-1mdv2010.1
+ Revision: 493435
- update to new version 2.2.2

* Sat Dec 26 2009 Ahmad Samir <ahmadsamir@mandriva.org> 2.2.1-1mdv2010.1
+ Revision: 482456
- new version 2.2.1

* Wed Dec 02 2009 Funda Wang <fwang@mandriva.org> 2.2.0-1mdv2010.1
+ Revision: 472471
- new version 2.2.0

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 2.0.9-2mdv2010.0
+ Revision: 430153
- rebuild

* Sun Sep 07 2008 Frederik Himpe <fhimpe@mandriva.org> 2.0.9-1mdv2009.0
+ Revision: 282241
- update to new version 2.0.9

* Mon Aug 25 2008 Funda Wang <fwang@mandriva.org> 2.0.8-1mdv2009.0
+ Revision: 275644
- New version 2.0.8

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.7-2mdv2009.0
+ Revision: 232976
- fix build

* Mon Dec 24 2007 David Walluck <walluck@mandriva.org> 2.0.7-1mdv2008.1
+ Revision: 137392
- 2.0.7

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 2.0.6-2mdv2008.0
+ Revision: 70374
- info file must be unregistered before being uninstalled

* Fri Apr 27 2007 David Walluck <walluck@mandriva.org> 2.0.6-1mdv2008.0
+ Revision: 18551
- 2.0.6

* Sun Apr 22 2007 David Walluck <walluck@mandriva.org> 2.0.5-1mdv2008.0
+ Revision: 17058
- 2.0.5
  require info-install not rpm-helper


* Mon Jan 29 2007 David Walluck <walluck@mandriva.org> 2.0.3-1mdv2007.1
+ Revision: 115169
- 2.0.3
  requires rpm-helper not info-install

* Thu Dec 21 2006 David Walluck <walluck@mandriva.org> 2.0.2-1mdv2007.1
+ Revision: 100915
- 2.0.2

* Mon Nov 20 2006 David Walluck <walluck@mandriva.org> 2.0.1-1mdv2007.1
+ Revision: 85688
- 2.0.1

  + Lenny Cartier <lenny@mandriva.com>
    - Import nano

* Fri Jun 16 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.3.11-3mdv2007.0
- fix the saving of crontabs with the backup mode active (P1 from debian)
- fix zero-length single-line regexes, which were making nano segfault (P2 from
  debian, should fix #19235)
- allow overriding regexes in the global nanorc with regexes in the personal
  nanorc without error messages (P3 from debian)
- fix nano wrapping some lines containing tabs too early. (P4 from debian)

* Sun Apr 16 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.3.11-2mdk
- 64-bit fixes

* Fri Mar 31 2006 Lenny Cartier <lenny@mandriva.com> 1.3.11-1mdk
- 1.3.11

* Tue Dec 27 2005 Michael Scherer <misc@mandriva.org> 1.3.10-1mdk
- 1.3.10
- fix some construct that trigger a loop in rpmbuildupdate

* Wed Oct 26 2005 Michael Scherer <misc@mandriva.org> 1.3.9-1mdk
- 1.3.9
- rpmbuildupdatable
- mkrel
- fix prereq

* Sat Jul 02 2005 Lenny Cartier <lenny@mandrakesoft.com> 1.3.8-1mdk
- 1.3.8

* Fri Apr 15 2005 Lenny Cartier <lenny@mandrakesoft.com> 1.3.7-1mdk
- 1.3.7

* Mon Feb 21 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.3.5-2mdk
- fix compile (P0, from gentoo)

* Thu Dec 02 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.3.5-1mdk
- 1.3.5

* Thu Aug 19 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.3.4-1mdk
- 1.3.4

* Wed Jun 30 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.3.3-1mdk
- 1.3.3

* Sat Apr 17 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.3.2-1mdk
- 1.3.2

