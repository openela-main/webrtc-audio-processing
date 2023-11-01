Name:           webrtc-audio-processing
Version:        0.3
Release:        10%{?dist}
Summary:        Library for echo cancellation

License:        BSD and MIT
URL:            http://www.freedesktop.org/software/pulseaudio/webrtc-audio-processing/
Source0:        http://freedesktop.org/software/pulseaudio/webrtc-audio-processing/%{name}-%{version}.tar.xz

## upstream patches (lookaside cache for now, not willing to bloat git this much yet)
Patch1: 0001-Add-missing-windows-specific-headers.patch
Patch2: 0002-build-Add-cerbero-gnustl-support-for-Android.patch
Patch3: 0003-build-Don-t-blindly-link-to-pthread.patch
Patch4: 0004-build-Add-required-define-for-Windows.patch
Patch5: 0005-build-Properly-select-the-right-system-wrappers.patch
Patch6: 0006-build-Define-MSVC-_WIN32-so-we-can-build-on-mingw.patch
Patch7: 0007-Add-missing-windows-conditions-variable.patch
Patch8: 0008-build-Protect-against-unsupported-CPU-types.patch
Patch9: 0009-osx-Fix-type-OS_FLAGS-instead-of-OS_CFLAGS.patch
Patch10: 0010-build-Sync-defines-and-libs-with-build.gn.patch
Patch11: 0011-build-Use-no-undefined-to-support-both-clang-and-gcc.patch
Patch12: 0012-build-Re-add-pthread-linking-on-linux.patch
Patch13: 0013-build-Add-ARM-64bit-support.patch
Patch14: 0014-build-fix-architecture-detection.patch
Patch15: 0015-doc-file-invalid-reference-to-pulseaudio-mailing-lis.patch
Patch16: 0016-build-Fix-configure-option-with-ns-mode.patch

Patch100:         webrtc-fix-typedefs-on-other-arches.patch
# bz#1336466, https://bugs.freedesktop.org/show_bug.cgi?id=95738
Patch104:         webrtc-audio-processing-0.2-big-endian.patch

BuildRequires: autoconf automake libtool
BuildRequires: gcc gcc-c++

%description
%{name} is a library derived from Google WebRTC project that 
provides echo cancellation functionality. This library is used by for example
PulseAudio to provide echo cancellation.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header
files for developing applications that use %{name}.

%prep
%autosetup -p1

%build
# for patch1
autoreconf -vif

%configure \
%ifarch %{arm} aarch64
  --enable-neon=no \
%endif
  --disable-silent-rules \
  --disable-static

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

# remove libtool archives
find %{buildroot} -type f -name "*.la" -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc NEWS AUTHORS README.md
%license COPYING
%{_libdir}/libwebrtc_audio_processing.so.1*

%files devel
%{_libdir}/libwebrtc_audio_processing.so
%{_libdir}/pkgconfig/webrtc-audio-processing.pc
%{_includedir}/webrtc_audio_processing/


%changelog
* Tue Jan 11 2021 Tomas Popela <tpopela@redhat.com> 0.3-10
- Include devel package in CRB
- Resolves: #2036956

* Mon Jun 01 2020 Debarshi Ray <rishi@fedoraproject.org> 0.3-9
- Rebuild to address Annobin coverage issues
Resolves: #1704148

* Mon Jul 23 2018 Debarshi Ray <rishi@fedoraproject.org> 0.3-8
- Update License

* Sat Mar  3 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.3-7
- Add gcc/gcc-c++ build requires
- Add aarch64 to NEON exception

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.3-5
- pull in upstream fixes, use %%autosetup

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jul 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.3-1
- 0.3

* Fri May 27 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.2-7
- better/upstreamable x86_msse2.patch

* Fri May 27 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.2-6
- simpler/upstreamable no_undefined.patch (fdo#96244)

* Wed May 25 2016 Than Ngo <than@redhat.com> - 0.2-5
- add url to upstream bug report

* Tue May 24 2016 Than Ngo <than@redhat.com> - 0.2-4
- add support big endian

* Mon May 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.2-3
- ExclusiveArch primary archs, FTBFS on big endian arches (#1336466)

* Mon May 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.2-2
- link w/ --no-undefined
- fix x86 sse2 runtime detection

* Thu May 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.2-1
- webrtc-audio-processing-0.2 (#1335536)
- %%files: track ABI/API closer

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.1-9
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 28 2014 Kyle McMartin <kyle@fedoraproject.org> - 0.1-6
- webrtc-fix-typedefs-on-other-arches.patch: fix ftbfs on non-x86/arm due to
  a build #error in typedefs.h, however, the defines are not used anywhere in
  the code. Fixes build on ppc{,64}, s390x, and aarch64.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Debarshi Ray <rishi@fedoraproject.org> 0.1-4
- Rebuilt to fix broken binary possibly caused by broken toolchain

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 9 2012 Dan Horák <dan[at]danny.cz> 0.1-2
- set ExclusiveArch x86 and ARM for now

* Fri Oct 5 2012 Christian Schaller <christian.schaller@gmail.com> 0.1-1
- Initial Fedora spec.
