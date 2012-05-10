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
import glob
cwd = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(cwd,"../../client/controller/"))
sys.path.append(os.path.join(cwd,"../../client/core/"))
import action
import core_processor
import cleaner

def die(msg) :
    print msg
    raise SystemExit(1)

def isDirEmpty(dn) :
    """Test if a directory is empty."""
    return not glob.glob(os.path.join(dn, '*'))

def emptyDir(dn) :
    """Remove all files in a directory."""
    for fn in glob.glob(os.path.join(dn, '*')):
        fn = os.path.split(fn)[1]
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

def runCmd(cmd, src, targ, ctrl, time=None) :
    """Invoke the command and process the results."""
    target_file = os.path.abspath(os.path.join(src,targ))
    cmd = cmd.replace('%targ', target_file)
    if time:
        ctrl.run_timed(cmd, time)
    else:
        ctrl.run(cmd)
    

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
    parser.add_option('-w', dest='wait', action='store',
        help='Wait for X number of seconds', default=None, type=int)
    parser.add_option('-t', dest='maxTime', action='store',
        help='Maximum time to spend on each src file.',
        default=5, type=int)
    parser.add_option('-i', dest='inputDir', action='store',
        help='Input direcotry for filep where sample files are located', default=None)

    ops,args = parser.parse_args()
    if ops.cmd is None :
        parser.error("Must specify a command.")
    if not ops.inputDir:
        parser.error("Must specify an input directory.")
    return ops

def main():
    ctrl = action.Action()
    core_p = core_processer.ProcessCores()
    _cleaner = cleaner.Clean()
    
    ops = getOptions()
    if ops.detector is not None :
        ops.detector = loadFunction(ops.detector)
 
    if not isDirEmpty(ops.outDir):
        emptyDir(ops.outDir)
        #die('Output directory has files.  Use an empty directory')
    
    print 'Input Directory: %s' % ', '.join(ops.inputDir)
    print 'Command: %s' % ops.cmd
    print 'Files per batch run: %d' % ops.batch
    print 'Output dir: %s' % ops.outDir

    ops.seed -= 1
    while 1 :   # forever (if ops.loop)
        ops.seed += 1
        for fn in glob.glob(os.path.join(ops.inputDir, '*')):   # cycle through all files...
            fn = os.path.split(fn)[1]
            fn = os.path.abspath(os.path.join(ops.inputDir, fn))
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
                file_listing = []
                for ofile in glob.glob(os.path.join(ops.outDir, '*')):
                    file_listing.append(os.path.split(ofile)[1])
                
                for file in file_listing:
                    try:
                        runCmd(ops.cmd, ops.outDir, file, ctrl, ops.wait)
                    except:
                        print 'Failed to execute command'
                        pass
                nfiles += ops.batch
                dt = time.time() - startTime + 0.000001
                #process all crashes/core files and their respective mutated files
                core_p.process_cores()
                _cleaner.remove_cores(cwd)
                print "\tseed %d run %d, Files/sec: %.1f" % (ops.seed, nfiles, nfiles / dt)
            
        if not ops.loop :
            break
    print 'done.'
  
if __name__ == '__main__':
    main()

