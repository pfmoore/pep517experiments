"""Calling PEP 517 hooks.

From PEP 517, "Frontends should call each hook in a fresh subprocess", so it's
not sufficient to simply import the backend and call the hooks. This module
encapsulates the process of calling the hooks via a subprocess.

It remains the responsibility of the build frontend to set up an isolated
environment for the build. This code assumes that a subprocess call to
`sys.executable` will run in an environment where only the build requirements
are present.
"""

import base64
import json
import subprocess
import sys

# Encoding format for transferring data to and from a subprocess:
#
# Python to transfer format:
#   Python data -> json dumps -> encode(utf8) -> b64encode -> stdout(ASCII)
# Transfer format to Python:
#  Stdin(ASCII) -> b64decode -> decode(utf8) -> json loads -> Python data
#
# The intent here is to only ever transfer ASCII data over stdio, to avoid any
# complications with encodings or Unicode.
#
# One potential issue. In Python 2, strings in the input data will become
# Unicode in the output. This should not be an issue, but needs to be tested.
# PEP 517 is not explicit on whether backends need to handle Unicode.

HOOK_SHIM = """
import base64
import json
import sys

import {backend_module}
backend = {backend_object}

argdata = base64.b64decode(sys.stdin.read())
args, kw = json.loads(argdata.decode('utf-8'))

ret = backend.{hook_name}(*args, **kw)

retdata = base64.b64encode(json.dumps(ret).encode('utf-8')).decode('ASCII')
print(retdata)
"""

class Backend:
    def __init__(self, spec):
        # TODO: Handle invalid specs
        self.module, sep, self.object = spec.partition(':')
        if not sep:
            self.object = self.module

    def call_hook(self, hook_name, *args, **kw):

        # TODO: Add error handling
        argdata = base64.b64encode(json.dumps([args, kw]).encode('utf-8'))
        shim = HOOK_SHIM.format(backend_module=self.module, backend_object=self.object, hook_name=hook_name)
        hookproc = subprocess.Popen([sys.executable, '-c', shim], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = hookproc.communicate(argdata)
        print(out)
        ret = json.loads(base64.b64decode(out).decode('utf-8'))
        return ret
    
