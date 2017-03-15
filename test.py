import os
import shutil
import subprocess
import time

from cases import Case

TEST_ROOT = './testfiles'
TEST_OUTPUT = './testoutput/'
TEST_SUCC = 'TEST PASSED'
TEST_FAIL_AT = 'TEST FAILED AT'


def prRed(prt): print("\033[91m {}\033[00m".format(prt))


def prGreen(prt): print("\033[92m {}\033[00m".format(prt))


def prYellow(prt): print("\033[93m {}\033[00m".format(prt))


def prLightPurple(prt): print("\033[94m {}\033[00m".format(prt))


def prPurple(prt): print("\033[95m {}\033[00m".format(prt))


def prCyan(prt): print("\033[96m {}\033[00m".format(prt))


def prLightGray(prt): print("\033[97m {}\033[00m".format(prt))


def prBlack(prt): print("\033[98m {}\033[00m".format(prt))


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
    Case('Test Big file to small encode', './testfiles', 'sample5.debug.txt', 'sample5.txt'),
    Case('Test EOF character', './testfiles', 'sample6.debug.txt', 'sample6.txt'),
    Case('Test Totally Uncompressable', './testfiles', '', 'sample7.txt')
])

make()

passed = True
for test in tests:
    prCyan('RUNNING TEST: {0}'.format(test.get_name()));
    outputRle = test.get_input_file().split('/')[-1]
    outputRlePath = TEST_OUTPUT + outputRle + '.rle'
    outputDecodePath = TEST_OUTPUT + outputRle + '.txt'

    if not (test.get_debug_str() is None):
        debug_info = subprocess.check_output(['./rlencode', test.get_input_file()], universal_newlines=True)
        if debug_info != test.get_debug_str():
            prRed('TEST FAILED AT {0} expect: {1} got: {2}'.format('ENCODE-DEBUG', test.get_debug_str(), debug_info))
            passed = False
            break

    encode_start = time.time()

    output = subprocess.check_output(['./rlencode', test.get_input_file(), outputRlePath], universal_newlines=True)
    if output != "":
        prRed('TEST FAILED AT {0} expect: {1} got: {2}'.format('ENCODE-FILE', '', output))
        passed = False
        break

    encode_time_consumed = time.time() - encode_start

    if not (test.get_debug_str() is None):
        debug_info = subprocess.check_output(['./rldecode', outputRlePath], universal_newlines=True)

        if debug_info != test.get_debug_str():
            prRed('TEST FAILED AT {0} expect: {1} got: {2}'.format('DECODE-DEBUG', test.get_debug_str(), debug_info))
            passed = False
            break

    decode_start = time.time()
    output = subprocess.check_output(['./rldecode', outputRlePath, outputDecodePath], universal_newlines=True)

    if output != "":
        prRed('TEST FAILED AT {0} expect: {1} got: {2}'.format('DECODE-FILE', '', output))
        passed = False
        break

    decode_time_consumed = time.time() - decode_start

    # compare result by diff
    try:
        subprocess.check_output(['diff', outputDecodePath, test.get_input_file()], universal_newlines=True)
    except subprocess.CalledProcessError:
        prRed('TEST FAILED {0} COMPARISON FAILURE'.format('DECODE-FILE'))
        passed = False
        break

    prGreen('\'{0}\' PASSED Encode Time: {1:.2f}s, Decode Time {2:.2f}s'.format(test.get_name(), encode_time_consumed,
                                                                            decode_time_consumed))

if passed:
    prGreen('ALL TESTS PASSED')

remove_folder()