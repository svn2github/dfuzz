#!/usr/bin/python
""" 
FileP File Fuzzer.
    Mutates source files and feeds them to a target application for testing.

September 2006, Written by Jesse Burns (jesse@isecpartners.com) 
and modified by Tim Newsham (tim@isecpartners.com).

Copyright (C) 2006, Information Security Partners, LLC.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import os, random, sys, time
from optparse import OptionParser
import squnch

def die(msg) :
    print msg
    raise SystemExit(1)

def isDirEmpty(dn) :
    """Test if a directory is empty."""
    return os.listdir(dn) == []

def emptyDir(dn) :
    """Remove all files in a directory."""
    for fn in os.listdir(dn) :
        os.remove(os.path.join(dn, fn))

def readFile(fn) :
    f = open(fn, 'rb')
    d = f.read()
    f.close()
    return d

def writeFile(fn, d) :
    f = open(fn, 'wb')
    f.write(d)
    f.close()

def splitFilename(fn) :
    """Split filename into dir, base and extension (base+ext = filename)."""
    dir,base = os.path.dirname(fn), os.path.basename(fn)
    if '.' in base :
        base,_ext = base.rsplit('.', 1)
        ext = '.' + _ext
    else :
        ext = ''
    return dir,base,ext

def noResults(src, targ, res) :
    """For -d: Don't show results."""
    pass

def showResults(src, targ, res) :
    """For -d: Show results."""
    print res

def showQuoted(src, targ, res) :
    """For -d: Show results quoted."""
    print repr(res)

def loadFunction(fn) :
    """Load a function, potentially from another module."""
    if '.' in fn :
        mn,fn = fn.rsplit('.', 1)
        try :
            mod = __import__(mn)
            return getattr(mod, fn)
        except ImportError :
            die("Can't load %s (for %s)." % (mn, fn))
        except AttributeError :
            die("Can't find %s in %s." % (fn, mn))
        return getattr(mod, fn)
    try :
        return globals()[fn]
    except KeyError :
        die("Can't find %s." % fn)

def runCmd(cmd, src, targ, proc) :
    """Invoke the command and process the results."""
    # XXX run in a debugger and catch exceptions.
    cmd = cmd.replace('%targ', targ)
    res = os.popen(cmd).read()
    return proc(src, targ, res)

def getOptions():
    """Perform option processing"""
    parser = OptionParser(usage='%prog [options] srcfiles ...', 
        version='%prog version 0.2')

    parser.add_option('-b', dest='batch', action='store',
        help='Number of files in a batch.', default=100, type=int)
    parser.add_option('-c', dest='cmd', action='store',
        help='Command to execute.  %dest is replaced with destination dir.')
    parser.add_option('-d', dest='detector', action='store',
        help='Detector function to call to process output.',
        default='noResults')
    parser.add_option('-l', dest='loop', action='store_false',
        help='Dont loop and run forever.', default=True)
    parser.add_option('-m', dest='maxFiles', action='store',
        help='Maximum files to generate for each src file.',
        default=10000, type=int)
    parser.add_option('-o', dest='outDir', action='store',
        help='directory to write the fuzz files to', default='files')
    parser.add_option('-s', dest='seed', action='store',
        help='Random number generator seed', default=0, type=int)
    parser.add_option('-t', dest='maxTime', action='store',
        help='Maximum time to spend on each src file.',
        default=5, type=int)

    ops,args = parser.parse_args()
    ops.srcFiles = args
    if ops.cmd is None :
        parser.error("Must specify a command.")
    if len(ops.srcFiles) == 0 :
        parser.error("Must specify at least one source file.")
    return ops

def main():
    ops = getOptions()
    if ops.detector is not None :
        ops.detector = loadFunction(ops.detector)

    if not isDirEmpty(ops.outDir) :
        die('Output directory has files.  Use an empty directory')
    print 'Src files: %s' % ', '.join(ops.srcFiles)
    print 'Command: %s' % ops.cmd
    print 'Files per batch run: %d' % ops.batch
    print 'Output dir: %s' % ops.outDir

    ops.seed -= 1
    while 1 :   # forever (if ops.loop)
        ops.seed += 1
        for fn in ops.srcFiles :   # cycle through all files...
            dir,base,ext = splitFilename(fn)
            d = readFile(fn)
            sq = squnch.Squncher(random.Random(ops.seed))
            fuzzer = sq.mutate(d)
            print "%s: %d bytes" % (fn, len(d))

            emptyDir(ops.outDir)
            startTime = time.time()
            nfiles,dt = 0, 0
            while dt < 60*ops.maxTime and nfiles < ops.maxFiles :
                # empty dir not needed after each run because we write
                # over the same filenames.
                for x in xrange(ops.batch) :
                    outfn = os.path.join(ops.outDir, '%s-%d%s' % (base, x, ext))
                    writeFile(outfn, fuzzer.next())
                if runCmd(ops.cmd, (dir,base,ext), ops.outDir, ops.detector) :
                    print 'something dropped!'
                    die('something dropped!')
                nfiles += ops.batch

                dt = time.time() - startTime + 0.000001
                print "\tseed %d run %d, Files/sec: %.1f" % (ops.seed, nfiles, nfiles / dt)
            # end while more time and files
        # end for all src files
        if not ops.loop :
            break
    # end forever
    print 'done.'
  
if __name__ == '__main__':
    main()

