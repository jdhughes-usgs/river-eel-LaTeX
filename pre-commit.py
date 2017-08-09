#!/usr/bin/python

from __future__ import print_function
import subprocess
import os
import sys
import datetime

pak = 'MODFLOW 6'
fpth = 'VERSION_FILE'
vpth = 'version.tex'
def get_version_str(v0, v1, v2, v3):
    version_type = ('{}'.format(v0), 
                    '{}'.format(v1), 
                    '{}'.format(v2), 
                    '{}'.format(v3))
    version = '.'.join(version_type)
    return version 

    
def get_tag(v0, v1, v2):
    tag_type = ('{}'.format(v0), 
                '{}'.format(v1), 
                '{}'.format(v2))
    tag = '.'.join(tag_type)
    return tag
     

def update_version():
    try:
        pth = os.path.join(fpth)
        
        vmajor = 0
        vminor = 0
        vmicro = 0
        vbuild = 0
        lines = [line.rstrip('\n') for line in open(pth, 'r')]
        for line in lines:
            if len(line) < 1 or line[0] == '#':
                continue
            t = line.split()
            if 'major =' in line:
                vmajor = int(t[2])
            elif 'minor =' in line:
                vminor = int(t[2])
            elif 'micro =' in line:
                vmicro = int(t[2])
            elif 'build =' in line:
                vbuild = int(t[2])
        
        v0 = get_version_str(vmajor, vminor, vmicro, vbuild)
        
        # get latest build number
        tag = get_version_str(vmajor, vminor, vmicro, 0)
        print('determining version build from {}'.format(tag))
        try:
            b = subprocess.Popen(("git", "describe", "--match", tag),
                                 stdout=subprocess.PIPE).communicate()[0]
            vbuild = int(b.decode().strip().split('-')[1]) + 1
        # assume if tag does not exist that it has not been added
        except:
            vbuild = 0
    
        v1 = get_version_str(vmajor, vminor, vmicro, vbuild)
    
        # get current build number
        b = subprocess.Popen(("git", "describe", "--match", "0.0.0.0"),
                             stdout=subprocess.PIPE).communicate()[0]
        vcommit = int(b.decode().strip().split('-')[1]) + 2
    
        cdatetime = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        t = cdatetime.split()
        cdate = t[0]
        ctime = t[1]
        cdv = '{:d}.{:d}.{:d}.{:d}'.format(vmajor, vminor, vmicro, vbuild)
        
        print('Updating version:')
        print('  ', v0, '->', v1)
    
        # write new version file
        f = open(pth, 'w')
        f.write('# {} version file automatically '.format(pak) +
                'created using...{0}\n'.format(os.path.basename(__file__)))
        f.write('# created on...{} at {}\n'.format(cdate, ctime))
        f.write('#\n')
        f.write('# major = major release number\n')
        f.write('# minor = minor release number\n')
        f.write('# micro = maintenance release number (bug fixes only)\n')
        f.write('# build = build number from initial maintenance release\n')
        f.write('\n')
        f.write('major = {}\n'.format(vmajor))
        f.write('minor = {}\n'.format(vminor))
        f.write('micro = {}\n'.format(vmicro))
        f.write('build = {}\n'.format(vbuild))
        f.write('commit = {}\n'.format(vcommit))
        f.write('version = {:d}.{:d}.{:d}\n'.format(vmajor, vminor, vmicro))
        f.write('develop_version = {}\n'.format(cdv))
        f.write('commit_date = {}\n'.format(cdate))
        f.close()
        print('Succesfully updated {}'.format(fpth))
        
        pth = os.path.join(vpth)
        f = open(pth, 'w')
        c = r'\newcommand{\version}{Version '
        c += '{}---{} {}'.format(cdv, cdate, ctime)
        c += '}\n'
        f.write(c)
        f.close()
        print('Succesfully updated {}'.format(vpth))
        
    except:
        print('There was a problem updating the {}'.format(fpth))
        sys.exit(1)

def add_updated_version():
    try:
        # add modified version file
        msg = 'Adding updated {}'.format(fpth)
        msg += ' and {}'.format(vpth)
        msg += ' to repo.'
        print(msg)
        args = ("git", "add", "{}".format(fpth), "{}".format(vpth))
        b = subprocess.Popen(args,
                             stdout=subprocess.PIPE).communicate()[0]
    except:
        print('Could not add updated version of {}'.format(fpth))
        sys.exit(1) 

if __name__ == "__main__":
    update_version()
    add_updated_version()
    
