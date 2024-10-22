import argparse
import sys

from testicles.loader import TestLoader
from testicles.test_runner import TestRunner

loader = TestLoader()

suites = loader.load("sandbox", load_suites=["unit", "integration"], top_level_dir=".") 

for suite in suites:
    TestRunner(suite).run()

# cli_parser = argparse.ArgumentParser(description='CLI for test runs')

# # Setup arguments for CLI
# cli_parser.add_argument(
#     "-sd",
#     "--start-dir",
#     type=str,
#     help="path to directory with tests relative to the current working directory, e.g. \"tests\", defaults to \"tests\"",
#     default="tests")
# cli_parser.add_argument(
#     "-td",
#     "--top-level-dir",
#     type=str,
#     help="path to the project root directory, e.g. \".\", defaults to \".\"",
#     default=".")
# cli_parser.add_argument(
#     "-t", "--type", type=str, help="\"unit\" or \"integration\"")
# cli_parser.add_argument(
#     "-f",
#     "--file",
#     type=str,
#     help="path to file relative to the current working directory, e.g. \".\\tests\\path\\to\\file.py\"")
# cli_parser.add_argument(
#     "-r", "--run", type=str, help="regular expression that matches a test function, e.g. \"^test_incorrect_token\"")

# # Parse CLI arguments
# args = cli_parser.parse_args()