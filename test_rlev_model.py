import os
import unittest

from click.testing import CliRunner

from rlev_model import cli


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def compare_rows(r1, r2):
    for f1, f2 in zip(r1, r2):
        assert isclose(f1, f2)


def parse_output(output):
    return [
        list(map(float, row.split()))
        for row in output.split('\n')
    ]


class TestCli(unittest.TestCase):
    def test_cli(self):
        runner = CliRunner()
        sample_filename = os.path.join('data', 'sample-data.txt')
        result = runner.invoke(cli, [sample_filename])
        assert result.exit_code == 0

        output_filename = os.path.join('data', 'sample-output.txt')
        with open(output_filename) as fp:
            expected_output = parse_output(fp.read())
        result_output = parse_output(result.output)
        for result_row, expected_row in zip(result_output, expected_output):
            compare_rows(result_row, expected_row)


if __name__ == '__main__':
    unittest.main()
