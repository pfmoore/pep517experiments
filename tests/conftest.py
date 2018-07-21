import pytest
import sys

class Backend:
    def __init__(self, srcfile):
        self.srcfile = srcfile
    def set_source(self, src):
        coding = u"# -*- coding: utf-8 -*-\n" 
        # This is a bit of a hack in Python 2. If src is a non-unicode
        # string, we concatenate it with a Unicode string, which
        # may give a decoding error if we get an encoding mismatch.
        # But I'm not sure I want to worry about making it any more
        # robust.
        self.srcfile.write_text(coding + src, encoding='utf-8')
    def spec(self):
        return self.srcfile.purebasename
    def location(self):
        return self.srcfile.dirname

@pytest.fixture
def backend(tmpdir):
    return Backend(tmpdir / 'Backend.py')
