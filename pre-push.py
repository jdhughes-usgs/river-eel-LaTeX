#!/usr/bin/python

from __future__ import print_function
import subprocess
import os
import sys
import datetime

pak = 'MODFLOW 6'
fpth = 'VERSION_FILE'


def get_version():
    tag = ''
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

        tag = '{:d}.{:d}.{:d}.{:d}'.format(vmajor, vminor, vmicro, vbuild)
        print('tag to add: {}'.format(tag))
    except:
        print('There was a problem parsing {}'.format(fpth))
        sys.exit(1)

    return tag


def add_tag(tag):
    """
    tag the git repo with the new version
    """
    try:
        # tagit = subprocess.check_output('git tag {}'.format(tag))
        cmd = 'git tag -f current_build -m "current build"'
        tagit = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        msg = 'tagging not successful: ' + \
              '{} {}'.format(e.output, e.returncode)
        raise Exception(msg)


if __name__ == "__main__":
    dryrun = False
    for arg in sys.argv:
        if arg == '-dr' or arg == '--dryrun':
            dryrun = True
            print('dryrun - will not add tag to repo')

    tag = get_version()
    if not dryrun:
        add_tag(tag)
