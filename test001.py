import os
import subprocess

def test_clean():
    ierr = 0
    try:
        os.remove('main.pdf')
    except:
        ierr = 1
    assert ierr == 0, 'could not remove main.pdf'
    
    return

def test_build():
    cmd = 'pdflatex main.tex'
    ierr = 0
    try:
        os.system(cmd)
    except:
        ierr = 1
    assert ierr == 0, 'could not build main.pdf'

    cmd = 'bibtex main.aux'
    ierr = 0
    try:
        os.system(cmd)
    except:
        ierr = 1
    assert ierr == 0, 'could not build main.aux'

    cmd = 'pdflatex main.tex'
    ierr = 0
    try:
        os.system(cmd)
    except:
        ierr = 1
    assert ierr == 0, 'could not build main.pdf'
    
    return
    
def test_pdf():
    assert os.path.isfile('main.pdf'), 'main.pdf does not exist'


def test_clean2():
    ierr = 0
    try:
        os.remove('main.pdf')
    except:
        ierr = 1
    assert ierr == 0, 'could not remove main.pdf'

    ierr = 0
    try:
        os.remove('main.aux')
    except:
        ierr = 1
    assert ierr == 0, 'could not remove main.aux'
    
    return


def test_build2():
    pth = './'
    
    # build pdf
    argv = ['pdflatex', 'main.tex']
    ierr = run_command(argv, pth)
    assert ierr == 0, 'Error on first call to pdflatex ({})'.format(ierr)

    argv = ['bibtex', 'main.aux']
    ierr = run_command(argv, pth)
    assert ierr == 0, 'Error on bibtex call ({})'.format(ierr)

    argv = ['pdflatex', 'main.tex']
    ierr = run_command(argv, pth)
    assert ierr == 0, 'Error on second call to pdflatex ({})'.format(ierr)

    argv = ['pdflatex', 'main.tex']
    ierr = run_command(argv, pth)
    assert ierr == 0, 'Error on third call to pdflatex ({})'.format(ierr)

    
def test_pdf():
    assert os.path.isfile('main.pdf'), 'main.pdf does not exist'
   
    return



def run_command(argv, pth):
    try:
        # run the model with Popen
        proc = subprocess.Popen(argv,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                cwd=pth)
        while True:
            line = proc.stdout.readline()
            c = line.decode('utf-8')
            if c != '':
                c = c.rstrip('\r\n')
                print('{}'.format(c))
            else:
                break
        ierr = 0
        if proc.returncode is not None:
            ierr = proc.returncode
        return ierr
    except:
        sys.stdout.write('could not run:')
        for arg in argv:
            sys.stdout.write(' {}'.format(arg))
        sys.stdout.write('\n')
        return 100


if __name__ == "__main__":
    print('standalone run of {}'.format(os.path.basename(__file__)))

    # run main routine
    test_clean()
    test_build()
    test_pdf()
