import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from ai_dev_local.cli import cli


def test_cli_help():
    """Test CLI help functionality."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "AI Dev Local - Manage your AI development environment" in result.output


@patch('ai_dev_local.cli.subprocess.run')
def test_cli_start_success(mock_run):
    """Test successful start command."""
    mock_run.return_value = MagicMock(returncode=0)
    
    runner = CliRunner()
    result = runner.invoke(cli, ['start'])
    
    assert result.exit_code == 0
    assert "🚀 Starting AI Dev Local services..." in result.output
    assert "✅ Services started successfully!" in result.output
    mock_run.assert_called_once()


@patch('ai_dev_local.cli.subprocess.run')
def test_cli_start_with_ollama(mock_run):
    """Test start command with Ollama flag."""
    mock_run.return_value = MagicMock(returncode=0)
    
    runner = CliRunner()
    result = runner.invoke(cli, ['start', '--ollama'])
    
    assert result.exit_code == 0
    assert "🚀 Starting AI Dev Local services..." in result.output
    mock_run.assert_called_once()
    
    # Check that --profile ollama was included in the command
    call_args = mock_run.call_args[0][0]
    assert '--profile' in call_args
    assert 'ollama' in call_args


@patch('ai_dev_local.cli.subprocess.run')
def test_cli_stop_success(mock_run):
    """Test successful stop command."""
    mock_run.return_value = MagicMock(returncode=0)
    
    runner = CliRunner()
    result = runner.invoke(cli, ['stop'])
    
    assert result.exit_code == 0
    assert "🛑 Stopping AI Dev Local services..." in result.output
    assert "✅ Services stopped successfully!" in result.output
    mock_run.assert_called_once_with(['docker-compose', 'down'], check=True, capture_output=True)


@patch('ai_dev_local.cli.subprocess.run')
def test_cli_status(mock_run):
    """Test status command."""
    mock_run.return_value = MagicMock(returncode=0, stdout="Service status output")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['status'])
    
    assert result.exit_code == 0
    assert "📊 Service Status:" in result.output
    assert "Service status output" in result.output
    mock_run.assert_called_once_with(['docker-compose', 'ps'], check=True, capture_output=True, text=True)


@patch('ai_dev_local.cli.subprocess.run')
def test_cli_logs_all(mock_run):
    """Test logs command for all services."""
    mock_run.return_value = MagicMock(returncode=0)
    
    runner = CliRunner()
    result = runner.invoke(cli, ['logs'])
    
    assert result.exit_code == 0
    assert "📋 Logs for all services:" in result.output
    mock_run.assert_called_once_with(['docker-compose', 'logs'], check=True)


@patch('ai_dev_local.cli.subprocess.run')
def test_cli_logs_specific_service(mock_run):
    """Test logs command for specific service."""
    mock_run.return_value = MagicMock(returncode=0)
    
    runner = CliRunner()
    result = runner.invoke(cli, ['logs', 'langfuse'])
    
    assert result.exit_code == 0
    assert "📋 Logs for langfuse:" in result.output
    mock_run.assert_called_once_with(['docker-compose', 'logs', 'langfuse'], check=True)


@patch('ai_dev_local.cli.webbrowser.open')
def test_cli_docs(mock_open):
    """Test docs command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['docs'])
    
    assert result.exit_code == 0
    assert "📚 Opening documentation..." in result.output
    mock_open.assert_called_once_with('http://localhost:8000')


@patch('ai_dev_local.cli.webbrowser.open')
def test_cli_dashboard(mock_open):
    """Test dashboard command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['dashboard'])
    
    assert result.exit_code == 0
    assert "🎛️ Opening dashboard..." in result.output
    mock_open.assert_called_once_with('http://localhost:3002')
