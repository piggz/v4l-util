Name:           v4l-utils
Version:        1.16.3
Release:        1%{?dist}
Summary:        Utilities for video4linux and DVB devices
Group:          Applications/System
# libdvbv5, dvbv5 utils, ir-keytable and v4l2-sysfs-path are GPLv2 only
License:        GPLv2+ and GPLv2
URL:            http://www.linuxtv.org/downloads/v4l-utils/
Source0:        http://linuxtv.org/downloads/v4l-utils/v4l-utils-%{version}.tar.bz2
BuildRequires:  libjpeg-devel kernel-headers desktop-file-utils
BuildRequires:  alsa-lib-devel doxygen gettext
# For /lib/udev/rules.d ownership
Requires:       udev
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description
v4l-utils is a collection of various video4linux (V4L) and DVB utilities. The
main v4l-utils package contains cx18-ctl, ir-keytable, ivtv-ctl, v4l2-ctl and
v4l2-sysfs-path.


%package        devel-tools
Summary:        Utilities for v4l2 / DVB driver development and debugging
# decode_tm6000 is GPLv2 only
License:        GPLv2+ and GPLv2
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description    devel-tools
Utilities for v4l2 / DVB driver authors: decode_tm6000, v4l2-compliance and
v4l2-dbg.


%package -n     qv4l2
Summary:        QT v4l2 test control and streaming test application
License:        GPLv2+
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description -n qv4l2
QT v4l2 test control and streaming test application.


%package -n     libv4l
Summary:        Collection of video4linux support libraries 
Group:          System Environment/Libraries
# Some of the decompression helpers are GPLv2, the rest is LGPLv2+
License:        LGPLv2+ and GPLv2
URL:            http://hansdegoede.livejournal.com/3636.html

%description -n libv4l
libv4l is a collection of libraries which adds a thin abstraction layer on
top of video4linux2 devices. The purpose of this (thin) layer is to make it
easy for application writers to support a wide variety of devices without
having to write separate code for different devices in the same class. libv4l
consists of 3 different libraries: libv4lconvert, libv4l1 and libv4l2.

libv4lconvert offers functions to convert from any (known) pixel-format
to V4l2_PIX_FMT_BGR24 or V4l2_PIX_FMT_YUV420.

libv4l1 offers the (deprecated) v4l1 API on top of v4l2 devices, independent
of the drivers for those devices supporting v4l1 compatibility (which many
v4l2 drivers do not).

libv4l2 offers the v4l2 API on top of v4l2 devices, while adding for the
application transparent libv4lconvert conversion where necessary.


%package -n     libdvbv5
Summary:        Libraries to control, scan and zap on Digital TV channels
Group:          Development/Libraries
License:        GPLv2

%description -n libdvbv5
Libraries to control, scan and zap on Digital TV channels

%package -n     libv4l-devel
Summary:        Development files for libv4l
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://hansdegoede.livejournal.com/3636.html
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description -n libv4l-devel
The libv4l-devel package contains libraries and header files for
developing applications that use libv4l.


%package -n     libdvbv5-devel
Summary:        Development files for libdvbv5
Group:          Development/Libraries
License:        GPLv2
Requires:       libdvbv5%{?_isa} = %{version}-%{release}

%description -n libdvbv5-devel
The libdvbv5-devel package contains libraries and header
files for developing applications that use libdvbv5.


%prep
%setup -q -n v4l-utils/v4l-utils


%build
./bootstrap.sh
%configure --disable-static --enable-libdvbv5 --disable-doxygen-doc --disable-doxygen-man
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm $RPM_BUILD_ROOT%{_libdir}/{v4l1compat.so,v4l2convert.so}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3/
#cp -arv %{_builddir}/%{name}-%{version}/doxygen-doc/man/man3 $RPM_BUILD_ROOT%{_mandir}/
#rm $RPM_BUILD_ROOT%{_mandir}/man3/_*3
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qv4l2.desktop
%find_lang %{name}
%find_lang libdvbv5


%post -n libv4l -p /sbin/ldconfig

%postun -n libv4l -p /sbin/ldconfig

%post -n libdvbv5 -p /sbin/ldconfig

%postun -n libdvbv5 -p /sbin/ldconfig

%post -n qv4l2
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n qv4l2
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n qv4l2
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang -f libdvbv5.lang
%doc README
%dir %{_sysconfdir}/rc_keymaps
%config(noreplace) %{_sysconfdir}/rc_maps.cfg
/lib/udev/rc_keymaps
%{_udevrulesdir}/70-infrared.rules
%{_bindir}/cx18-ctl
%{_bindir}/dvb*
%{_bindir}/ir-keytable
%{_bindir}/ivtv-ctl
%{_bindir}/media-ctl
%{_bindir}/rds-ctl
%{_bindir}/v4l2-ctl
%{_bindir}/v4l2-sysfs-path
%{_bindir}/cec-compliance
%{_bindir}/cec-ctl
%{_bindir}/cec-follower
%{_bindir}/ir-ctl

%{_mandir}/man1/*.1*
%exclude %{_mandir}/man1/qv4l2.1*
%exclude %{_mandir}/man1/v4l2-compliance.1*

%files devel-tools
%doc README
%{_bindir}/decode_tm6000
%{_bindir}/v4l2-compliance
%{_mandir}/man1/v4l2-compliance.1*
%{_sbindir}/v4l2-dbg

%files -n qv4l2
%doc README
%{_bindir}/qv4l2
%{_datadir}/applications/qv4l2.desktop
%{_datadir}/icons/hicolor/*/apps/qv4l2.*
%{_mandir}/man1/qv4l2.1*

%files -n libv4l
%doc COPYING.libv4l COPYING ChangeLog README.libv4l TODO
%{_libdir}/libv4l
%{_libdir}/libv4l*.so.*

%files -n libv4l-devel
%doc README.lib-multi-threading
%{_includedir}/libv4l*.h
%{_libdir}/libv4l*.so
%{_libdir}/pkgconfig/libv4l*.pc

%files -n libdvbv5
%doc COPYING ChangeLog lib/libdvbv5/README
%{_libdir}/libdvbv5*.so.*

%files -n libdvbv5-devel
%{_includedir}/libdvbv5/*.h
%{_libdir}/libdvbv5*.so
%{_libdir}/pkgconfig/libdvbv5*.pc
