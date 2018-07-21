import pytest

class Backend:
    def __init__(self, srcfile):
        self.srcfile = srcfile
    def set_source(self, src):
        self.srcfile.write_text("# -*- coding: utf-8 -*-\n" + src, encoding='utf-8')
    def spec(self):
        return self.srcfile.purebasename
    def location(self):
        return self.srcfile.dirname

@pytest.fixture
def backend(tmpdir):
    return Backend(tmpdir / 'Backend.py')
