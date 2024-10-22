import fnmatch
import os
import re
import sys
from typing import List

from .test_suite import TestSuite

VALID_MODULE_NAME = re.compile(r'[_a-z]\w*\.py$', re.IGNORECASE)

class TestLoader:
    _start_dir: str
    _top_level_dir: str

    def __init__(self) -> None:
        pass

    def load(self, start_dir: str, pattern: str, /, *, load_suites: List[str] | None = None, top_level_dir: str | None = None):
        self._start_dir = start_dir = os.path.abspath(start_dir or "tests")
        self._top_level_dir = top_level_dir = os.path.abspath(top_level_dir or ".")

        if not top_level_dir in sys.path:
            sys.path.insert(0, top_level_dir)

        is_importable = True
        if os.path.isdir(start_dir):
            if start_dir != top_level_dir:
                is_importable = os.path.isfile(os.path.join(start_dir, "__init__.py"))
        else:
            raise Exception("Import from dotted module names is not implemented.")
        
        if not is_importable:
            raise ImportError(f"Start directory is not importable: {start_dir}")

        suites = set(self._find_suites(start_dir, pattern, load_suites=load_suites))

        return suites

    def _find_suites(self, start_dir: str, pattern: str, /, *, load_suites: List[str] | None = None):
        paths = sorted(os.listdir(start_dir))

        for path in paths:
            full_path = os.path.join(start_dir, path)
            basename = os.path.basename(full_path)
            if os.path.isfile(full_path):
                # filter out modules with invalid names
                if not VALID_MODULE_NAME.match(basename):
                    continue

                # filter our files that do not match
                if not fnmatch.fnmatch(full_path, pattern):
                    continue

                yield from self._load_suites_from_path(full_path, load_suites=load_suites)
            elif os.path.isdir(full_path):
                if not os.path.isfile(os.path.join(full_path, '__init__.py')):
                    continue

                yield from self._load_suites_from_path(full_path, load_suites=load_suites)
                
                # recursively find suites
                yield from self._find_suites(full_path, pattern, load_suites=load_suites)

    def _get_name_from_path(self, path: str):
        if path == self._top_level_dir:
            return '.'
        
        path = os.path.splitext(os.path.normpath(path))[0]
        relpath = os.path.relpath(path, self._top_level_dir)
        assert not os.path.isabs(relpath), "Path must be within the project"
        assert not relpath.startswith('..'), "Path must be within the project"

        return relpath.replace(os.path.sep, '.')
    
    def _get_module_from_name(self, name: str):
        __import__(name)
        return sys.modules[name]

    def _load_suites_from_path(self, path: str, /, *, load_suites: List[str] | None = None):
        name = self._get_name_from_path(path)
        module = self._get_module_from_name(name)
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, TestSuite) and (load_suites is None or obj._name in load_suites):
                yield obj