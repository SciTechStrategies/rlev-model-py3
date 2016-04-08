import os
import unittest

from click.testing import CliRunner

from rlev_model import cli


class TestCli(unittest.TestCase):
    def test_cli(self):
        runner = CliRunner()
        sample_filename = os.path.join('data', 'sample-data.txt')
        result = runner.invoke(cli, [sample_filename])
        assert result.exit_code == 0

        output_filename = os.path.join('data', 'sample-output.txt')
        with open(output_filename) as fp:
            expected_output = fp.read()
        assert result.output == expected_output


if __name__ == '__main__':
    unittest.main()
