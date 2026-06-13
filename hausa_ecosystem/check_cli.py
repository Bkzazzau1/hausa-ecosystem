import sys

from hausa_ecosystem.code_checker import run_check_command


def main():
    return run_check_command(sys.argv[1:])
