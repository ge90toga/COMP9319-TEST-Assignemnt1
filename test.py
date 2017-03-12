import os
import shutil
import subprocess
from cases import Case

TEST_ROOT = './testfiles'
TEST_OUTPUT = './testoutput/'
TEST_SUCC = 'TEST PASSED'
TEST_FAIL_AT = 'TEST FAILED AT'


def remove_folder(path='./testoutput'):
    if os.path.exists(path):
        shutil.rmtree(path)


def create_folder(path='./testoutput'):
    if not os.path.exists(path):
        os.makedirs(path)


def make():
    with open(os.devnull, 'w') as shutup:
        return_code = subprocess.check_call(['make', 'clean'], stdout=shutup, stderr=shutup)

    with open(os.devnull, 'w') as shutup:
        return_code = subprocess.check_call(['make'], stdout=shutup, stderr=shutup)


create_folder()

tests = []

## add your test case here
tests.extend([
    Case('sample1', './testfiles', 'sample1.debug.txt', 'sample1.txt'),
    Case('sample2', './testfiles', 'sample2.debug.txt', 'sample2.txt'),
    Case('sample3', './testfiles', 'sample3.debug.txt', 'sample3.txt'),
    Case('sample4', './testfiles', 'sample4.debug.txt', 'sample4.txt'),
    Case('sample5', './testfiles', 'sample5.debug.txt', 'sample5.txt'),
])

make()

passed = True
for test in tests:

    print('RUNNING TEST: {0}'.format(test.get_name()))
    outputRle = test.get_input_file().split('/')[-1]
    outputRlePath = TEST_OUTPUT + outputRle + '.rle'
    outputDecodePath = TEST_OUTPUT + outputRle + '.txt'

    debug_info = subprocess.check_output(['./rlencode', test.get_input_file()], universal_newlines=True)
    # remove the last new line char
    if debug_info != test.get_debug_str():
        print('TEST FAILED AT {0} expect: {1} got: {2}'.format('ENCODE-DEBUG', test.get_debug_str(), debug_info))
        passed = False
        break

    output = subprocess.check_output(['./rlencode', test.get_input_file(), outputRlePath], universal_newlines=True)
    if output != "":
        print('TEST FAILED AT {0} expect: {1} got: {2}'.format('ENCODE-FILE', '', output))
        passed = False
        break

    debug_info = subprocess.check_output(['./rldecode', outputRlePath], universal_newlines=True)

    if debug_info != test.get_debug_str():
        print('TEST FAILED AT {0} expect: {1} got: {2}'.format('DECODE-DEBUG', test.get_debug_str(), debug_info))
        passed = False
        break

    output = subprocess.check_output(['./rldecode', outputRlePath, outputDecodePath], universal_newlines=True)

    if output != "":
        print('TEST FAILED AT {0} expect: {1} got: {2}'.format('DECODE-FILE', '', output))
        passed = False
        break

    # compare result by diff
    try:
        subprocess.check_output(['diff', outputDecodePath, test.get_input_file()], universal_newlines=True)
    except subprocess.CalledProcessError:
        print('TEST FAILED {0} COMPARISON FAILURE'.format('DECODE-FILE'))
        passed = False
        break

    print('{0} PASSED'.format(test.get_name()))

if passed:
    print('TEST ALL PASSED')

remove_folder()