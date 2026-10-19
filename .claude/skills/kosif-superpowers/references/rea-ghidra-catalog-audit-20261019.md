# KOSIF Evidence-led Investigation — 2026-10-19

This document summarizes bounded results, not an assertion of exhaustive
reverse engineering or copying commercial software.

- Existing static Desktop "تجربة" inventory: 2,006 files, 737 folders,
  approximately 9.57 GiB, with four unreadable files. The 1,706 files inside
  kosif-tool in that inventory were KOSIF's own source or resources, so they
  should not be counted as 1,706 newly investigated commercial-program files.
- Unpacked Adobe Lightroom Classic 14.0.1 package: 205 files, 90 subfolders
  at review time. Mostly installer package files (.pimx/.pima/.sig). These
  are not a verified running Lightroom image editor.
- REA agents version 6.7.0 and Ghidra 12.1.4 were found. Their initial
  integration failed because GHIDRA_INSTALL_DIR was absent and JAVA_HOME
  pointed at JDK 17. Using the existing JDK 21 in the *process environment*
  allowed a successful REA/Ghidra inspect of Lightroom's AdobePIM.dll.
- Read-only AdobePIM.dll inspection: 8,088 Ghidra-defined procedures and
  4,283 defined strings. Those counts are partial static evidence from an
  INSTALLER-support DLL, not extracted functionality of Lightroom.
- Blender was not discoverable as an installed command on the Windows host.
  No Blender binaries were analyzed or integrated during this pass.
- KOSIF Superpowers 4,730 unique catalog records in 52 families.
  Evidence/link audit checks every catalog entry but does not execute the
  external references. Most external/SIBLING/URL links cannot be verified
  from kosif-tool alone.
- kosif-atlas repository README explicitly says the redistributed third-party
  skill scripts were not all line-by-line audited. GPL and other copyleft
  sources have separate licensing requirements. Source must be reviewed
  before imports or execution, not copied into KOSIF indiscriminately.
- The user's Claude Auto Mode screenshot shows an external-code execution
  permission denial for a git clone compound command. This is not a proven
  Superpowers runtime failure. New offline local-first workflow avoids making
  a git clone a prerequisite for searching an installed skill.

Remaining work: inspect chosen native binaries/function flows with evidence;
audit Atlas skills and dependencies individually before import; run cross-
platform acceptance tests for KOSIF image/video output and real word alignment;
finish Blender integration if official Blender is installed; fix stale or
missing catalog links; and confirm GitHub CI after PR.
