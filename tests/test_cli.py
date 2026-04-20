import pytest
from unittest.mock import patch, Mock
from cli import main

@pytest.fixture
def mock_argparse():
    with patch('cli.create_parser') as mock_parser:
        mock_instance = Mock()
        mock_parser.return_value = mock_instance
        yield mock_instance

def test_cli_main_success(mock_argparse):
    # Мокируем зависимости
    with patch('cli.read_all_files') as mock_read, \
         patch('cli.ClickbaitReporter') as mock_reporter, \
         patch('cli.display_report') as mock_display:

        # Настраиваем моки
        mock_read.return_value = []
        mock_reporter_instance = Mock()
        mock_reporter.return_value = mock_reporter_instance
        mock_reporter_instance.generate.return_value = Mock(videos=[])

        # Имитируем аргументы командной строки
        mock_argparse.parse_args.return_value = Mock(
            files=['stats1.csv'],
            report='clickbait'
        )

        # Запускаем main()
        main()

        # Проверяем, что функции были вызваны
        mock_read.assert_called_once()
        mock_reporter.assert_called_once()
        mock_display.assert_called_once()

def test_cli_with_multiple_files(mock_argparse):
    with patch('cli.read_all_files') as mock_read:
        mock_read.return_value = []

        mock_argparse.parse_args.return_value = Mock(
            files=['file1.csv', 'file2.csv'],
            report='clickbait'
        )

        main()
        assert mock_read.call_count == 1

def test_cli_with_invalid_report_type(capsys):
    with patch('sys.argv', ['main.py', '--files', 'stats1.csv', '--report', 'invalid']):
        with patch('readers.read_all_files', return_value=[]):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 2  # Меняем на 2

    captured = capsys.readouterr()
    assert "invalid choice: 'invalid'" in captured.err


def test_cli_without_files_argument(capsys):
    """Тест отсутствия аргумента --files."""
    with patch('sys.argv', ['main.py']):
        with pytest.raises(SystemExit):
            main()

    captured = capsys.readouterr()
    assert "ожидался хотя бы один аргумент" in captured.err or "the following arguments are required: --files" in captured.err

