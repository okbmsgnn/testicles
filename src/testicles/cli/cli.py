import argparse
import os
import re
from multiprocessing import Process
from typing import List

from testicles.loader import TestLoader
from testicles.test_runner import (ParallelTextTestRunner, TestRunner,
                                   TextTestRunner)
from testicles.test_suite import TestSuite


# Run tests (synchronously or in parallel)
def run_suite(runner: type[TestRunner], suite: TestSuite, run: str | None):
    # Filter tests by regex
    if run:
        match = re.compile(run).match

        for test in suite.tests:
            if not match(test._fn.__name__):
                suite.unregister_test(test)

    runner(suite).run()

def main():
    cli_parser = argparse.ArgumentParser(description='CLI for test runs')

    # Define arguments for CLI
    cli_parser.add_argument(
        "-sd",
        "--start-dir",
        type=str,
        help="path to directory with tests relative to the current working directory, e.g. \"tests\", defaults to \"tests\"",
        default="tests")
    cli_parser.add_argument(
        "-td",
        "--top-level-dir",
        type=str,
        help="path to the project root directory, e.g. \".\", defaults to \".\"",
        default=".")
    cli_parser.add_argument(
        "-p",
        "--pattern",
        type=str,
        help="glob search pattern for test files, e.g. \"^\"",
        default=r"*/test_*.py")
    cli_parser.add_argument(
        "-s", "--suite",
        type=str,
        help="suite names to run (comma separated values), e.g. \"suite1,suite2\"")
    cli_parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="path to file relative to the current working directory, e.g. \".\\tests\\path\\to\\file.py\"")
    cli_parser.add_argument(
        "-r", "--run", type=str, help="regular expression that matches a test function name, e.g. \"^test_incorrect_token\"")
    cli_parser.add_argument(
        "--parallel",
        type=bool,
        help="run tests in parallel, defaults to \"False\"",
        default=False
    )

    # Parse CLI arguments
    args = cli_parser.parse_args()

    load_suites = args.suite.split(",") if args.suite else None
    file = os.path.abspath(args.file) if args.file else None
    pattern = file or args.pattern

    # Load suites
    loader = TestLoader()
    suites = loader.load("sandbox", pattern, load_suites=load_suites, top_level_dir=".") 

    if args.parallel:
        processes: List[Process] = []
        
        for suite in suites:
            process = Process(target=run_suite, args=[ParallelTextTestRunner, suite, args.run])
            processes.append(process)
            process.start()
            
        for process in processes:
            process.join()
    else:
        for suite in suites:
            run_suite(TextTestRunner, suite, args.run)