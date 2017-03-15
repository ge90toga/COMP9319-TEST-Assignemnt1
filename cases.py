# The test case class
'''
Suppose your testfiles sits under ./testfiles direcotry, your debug output file is ./testfiles/sample1.debug.txt
your sample file is ./testfiles/sample1.txt
Create your test case by doing:
Case('sample1', './testfiles', 'sample1.debug.txt', 'sample1.txt') case,
'''
class Case():
    def __init__(self, name, test_root, debug_file, input_file):
        self.name = name
        self.test_root = test_root
        self.debug_file = debug_file
        self.input_file = self.test_root + '/'+ input_file
        self.read_debug_file()

    def get_name(self):
        return self.name;

    def read_debug_file(self):
        if self.debug_file == "":
            self.debug_str = None
        else:
            with open(self.test_root + '/' + self.debug_file , 'r') as f:
                self.debug_str = f.read()

    def get_debug_str(self):
        return self.debug_str

    def get_input_file(self):
        return self.input_file

    def __str__(self):
        return "TEST NAME {0}, TEST FILE PATH: {1}, TEST DEBUG:{2} ".format(self.name,self.input_file,self.debug_str)

