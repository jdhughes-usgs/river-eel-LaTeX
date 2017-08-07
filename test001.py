import os

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
    
    return
    
def test_pdf():
    assert os.path.isfile('main.pdf'), 'main.pdf does not exist'

if __name__ == "__main__":
    print('standalone run of {}'.format(os.path.basename(__file__)))

    # run main routine
    test_clean()
    test_build()
    test_pdf()
