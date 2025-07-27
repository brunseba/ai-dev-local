import pytest
from click.testing import CliRunner
from ai_dev_local.cli import cli


def test_cli_start():
    """Test the start command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['start'])
    assert result.exit_code == 0
    assert "Starting AI Dev Local..." in result.output


def test_cli_help():
    """Test CLI help functionality."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "Usage:" in result.output
