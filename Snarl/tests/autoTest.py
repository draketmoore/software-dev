#
# autoTest.py
# authors: Michael Curley & Drake Moore
#

from json import loads
from os import listdir, path, remove
from pprint import pprint
from subprocess import PIPE, Popen, run
from sys import argv
testNum = 1
testDir = (argv[1] + ('' if argv[1].endswith('/') else '/')) if len(argv) > 1 else ''
testFile = list(filter(lambda f: path.isfile(f) and f.startswith('test') and '.' not in f, listdir('.')))[0]
while 1:
    try:
        actOutFile = '{0}{1}-out-actual.json'.format(testDir, testNum)
        expOutFile = '{0}{1}-out.json'.format(testDir, testNum)
        if not path.exists(expOutFile):
            raise FileNotFoundError
        with open('{0}{1}-in.json'.format(testDir, testNum), 'r') as f:
            jsonIn = f.read()
        p = Popen(['./' + testFile], stdout = PIPE, stdin = PIPE)
        p.stdin.write(jsonIn.encode('utf-8'))
        p.stdin.flush()
        p.stdin.close()
        p.wait()
        with open(actOutFile, 'w') as f:
            f.write(p.stdout.read().decode('utf-8'))
        cmd = ['jq', '-S', '.']
        p = Popen(cmd + [expOutFile], stdout = PIPE)
        p.wait()
        expJq = p.stdout.read().decode('utf-8')
        p = Popen(cmd + [actOutFile], stdout = PIPE)
        p.wait()
        actJq = p.stdout.read().decode('utf-8')
        passed = expJq == actJq
        print('Test #{0}: {1}'.format(testNum, 'passed' if passed else 'failed'))
        if not passed:
            print('Expected')
            pprint(loads(expJq))
            print('Actual')
            pprint(loads(actJq))
            print()
    except FileNotFoundError:
        break
    except Exception as e:
        print('Error in {0}: {1}'.format(testNum, e))
    finally:
        if path.exists(actOutFile):
            remove(actOutFile)
        testNum += 1
