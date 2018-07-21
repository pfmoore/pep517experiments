import pep517
import sys
import os

def test_backend(backend):
    assert backend.spec() == 'Backend'

def test_import_backend(backend, monkeypatch):
    backend.set_source("example = 12")
    monkeypatch.setattr(sys, 'path', [backend.location()])
    b = __import__(backend.spec())
    assert b.example == 12

def test_call_backend(backend, monkeypatch):
    backend.set_source("def h(): return 12")
    monkeypatch.setitem(os.environ, 'PYTHONPATH', backend.location())
    b = pep517.Backend(backend.spec())
    assert b.call_hook('h') == 12
