This project is a test script for the 1st assignemt COMP9319 Web Data Compression
and Search.

## Test cases
- currently we have 5 test cases in folder testfiles writen by tutor
HaoJie. I provided the debug cli output from my program named sampleX.debug.txt, 
please feel free to check correctness.

## Structure
```
/
├── test.py (the test script)
├── cases.py (the class to construct test case)
├── testfiles
│   │      
│   ├── testfile.tar.gz (test contents)

```
## How to use
- make sure you have python3
- copy `test.py`, `cases.py`,  `testfiles/` into your assignment direcotry
- uncompress `testfiles/testfile.tar.gz`
- run `python3 test.py`

## Contributing

Please feel free to contribute more test cases via pull request and improve this test script by adding memory and time 
measurements. 