Fuzzbox 0.3
(C)2007 Information Security Partners Inc.

Fuzzbox creates corrupt but structurally valid sound files, and
optionally launches them off in a player, gathering backtraces and
register information. Also included is a standalone tool to reset
the CRCs of Ogg-contained files after manual corruption.

NOTICE: One of the fuzzing tests tries to insert an HTTP URL to check
for programs attempting to make web requests when processing files.
This goes to labs.isecpartners.com by default. Please change this
if you have privacy concerns.

The spawning/killing of the player will only work on UNIX/OSX or
possibly cygwin, as there's unfortunately no simple cross-platform way
to do it. It shouldn't be hard to modify for Windows, though.

For the vorbis comment header, py-vorbis is required. You will have to
increase the max tag buffer size (tag_buff) in pyvorbisinfo.c before
install for this to work right.

For AIFFs, WAVs, MP3s and MP4s, the included Makefile should auto-fetch
and patch the appropriate files. It will need to be edited to know about
your system layout and file transfer program of choice.

You should verify that the mutagen distfile matches this SHA256:

SHA256 (./mutagen-1.11.tar.gz) = 
f22d0570a0d7d1b3d7a54bc70471fe212bd84aaabe5ab1d0c685f2b92a85b11a

If you find bugs with this software, I'd love to hear about it. I also
ask that these bugs be disclosed responsibly.

david@isecpartners.com
