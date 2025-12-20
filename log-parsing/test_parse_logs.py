"""
Test suite for log parsing script.
"""

import pytest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

# Add current directory to path to import parse_logs module
sys.path.insert(0, str(Path(__file__).parent))

from parse_logs import (
    LogEntry,
    TxtLogParser,
    XmlLogParser,
    CsvLogParser,
    LogAnalyzer
)


class TestLogEntry:
    """Test LogEntry dataclass."""
    
    def test_extract_hour_iso_format(self):
        """Test hour extraction from ISO format timestamp."""
        timestamp = "2023-08-18T14:30:25"
        hour = LogEntry.extract_hour(timestamp)
        assert hour == 14
    
    def test_extract_hour_bracketed_format(self):
        """Test hour extraction from bracketed format timestamp."""
        timestamp = "[2023-08-18 14:30:25]"
        hour = LogEntry.extract_hour(timestamp)
        assert hour == 14
    
    def test_extract_hour_space_separated(self):
        """Test hour extraction from space-separated timestamp."""
        timestamp = "2023-08-18 14:30:25"
        hour = LogEntry.extract_hour(timestamp)
        assert hour == 14
    
    def test_from_dict(self):
        """Test creating LogEntry from dictionary."""
        data = {
            'timestamp': '2023-08-18 14:30:25',
            'severity': 'ERROR',
            'message': 'Test error message'
        }
        entry = LogEntry.from_dict(data)
        assert entry.timestamp == '2023-08-18 14:30:25'
        assert entry.severity == 'ERROR'
        assert entry.message == 'Test error message'
        assert entry.hour == 14


class TestTxtLogParser:
    """Test TXT log parser."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        with TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def create_txt_log(self, path: Path, lines: list):
        """Helper to create TXT log files for testing."""
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def test_parse_valid_entries(self, temp_dir):
        """Test parsing valid TXT log entries."""
        log_file = temp_dir / 'test.txt'
        self.create_txt_log(log_file, [
            '[2023-08-18 12:00:01] [INFO] User logged in.',
            '[2023-08-18 12:10:23] [WARN] CPU usage high.',
            '[2023-08-18 12:15:45] [ERROR] Database connection failed.'
        ])
        
        parser = TxtLogParser()
        entries = parser.parse(log_file)
        
        assert len(entries) == 3
        assert entries[0].severity == 'INFO'
        assert entries[1].severity == 'WARN'
        assert entries[2].severity == 'ERROR'
        assert entries[2].message == 'Database connection failed.'
    
    def test_parse_empty_file(self, temp_dir):
        """Test parsing empty TXT file."""
        log_file = temp_dir / 'empty.txt'
        self.create_txt_log(log_file, [])
        
        parser = TxtLogParser()
        entries = parser.parse(log_file)
        
        assert len(entries) == 0
    
    def test_parse_malformed_entries(self, temp_dir):
        """Test parsing TXT file with malformed entries."""
        log_file = temp_dir / 'malformed.txt'
        self.create_txt_log(log_file, [
            '[2023-08-18 12:00:01] [INFO] Valid entry.',
            'This is not a valid log entry',
            '[2023-08-18 12:10:23] [WARN] Another valid entry.'
        ])
        
        parser = TxtLogParser()
        entries = parser.parse(log_file)
        
        # Should parse only valid entries
        assert len(entries) == 2
        assert entries[0].severity == 'INFO'
        assert entries[1].severity == 'WARN'


class TestXmlLogParser:
    """Test XML log parser."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        with TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def create_xml_log(self, path: Path, content: str):
        """Helper to create XML log files for testing."""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def test_parse_valid_entries(self, temp_dir):
        """Test parsing valid XML log entries."""
        log_file = temp_dir / 'test.xml'
        xml_content = '''<logs>
  <log><timestamp>2023-08-18T12:00:01</timestamp><severity>INFO</severity><message>User logged in.</message></log>
  <log><timestamp>2023-08-18T12:15:15</timestamp><severity>WARN</severity><message>Memory usage high.</message></log>
  <log><timestamp>2023-08-18T12:30:30</timestamp><severity>ERROR</severity><message>Disk write failed.</message></log>
</logs>'''
        self.create_xml_log(log_file, xml_content)
        
        parser = XmlLogParser()
        entries = parser.parse(log_file)
        
        assert len(entries) == 3
        assert entries[0].severity == 'INFO'
        assert entries[1].severity == 'WARN'
        assert entries[2].severity == 'ERROR'
        assert entries[2].message == 'Disk write failed.'
    
    def test_parse_empty_logs(self, temp_dir):
        """Test parsing XML file with empty logs element."""
        log_file = temp_dir / 'empty.xml'
        self.create_xml_log(log_file, '<logs></logs>')
        
        parser = XmlLogParser()
        entries = parser.parse(log_file)
        
        assert len(entries) == 0
    
    def test_parse_incomplete_entries(self, temp_dir):
        """Test parsing XML with incomplete log entries."""
        log_file = temp_dir / 'incomplete.xml'
        xml_content = '''<logs>
  <log><timestamp>2023-08-18T12:00:01</timestamp><severity>INFO</severity><message>Complete entry.</message></log>
  <log><timestamp>2023-08-18T12:15:15</timestamp><severity>WARN</severity></log>
  <log><timestamp>2023-08-18T12:30:30</timestamp><severity>ERROR</severity><message>Another complete entry.</message></log>
</logs>'''
        self.create_xml_log(log_file, xml_content)
        
        parser = XmlLogParser()
        entries = parser.parse(log_file)
        
        # Should parse only complete entries
        assert len(entries) == 2
        assert entries[0].message == 'Complete entry.'
        assert entries[1].message == 'Another complete entry.'


class TestCsvLogParser:
    """Test CSV log parser."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        with TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def create_csv_log(self, path: Path, rows: list):
        """Helper to create CSV log files for testing."""
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(rows))
    
    def test_parse_valid_entries(self, temp_dir):
        """Test parsing valid CSV log entries."""
        log_file = temp_dir / 'test.csv'
        self.create_csv_log(log_file, [
            'timestamp,severity,message',
            '"2023-08-18 12:00:01","INFO","User logged in."',
            '"2023-08-18 12:15:15","WARN","Disk space low."',
            '"2023-08-18 12:30:30","ERROR","File write failed."'
        ])
        
        parser = CsvLogParser()
        entries = parser.parse(log_file)
        
        assert len(entries) == 3
        assert entries[0].severity == 'INFO'
        assert entries[1].severity == 'WARN'
        assert entries[2].severity == 'ERROR'
        assert entries[2].message == 'File write failed.'
    
    def test_parse_empty_file(self, temp_dir):
        """Test parsing CSV file with only headers."""
        log_file = temp_dir / 'empty.csv'
        self.create_csv_log(log_file, ['timestamp,severity,message'])
        
        parser = CsvLogParser()
        entries = parser.parse(log_file)
        
        assert len(entries) == 0


class TestLogAnalyzer:
    """Test LogAnalyzer class."""
    
    def create_sample_entries(self) -> list:
        """Create sample log entries for testing."""
        return [
            LogEntry('2023-08-18 12:00:01', 'INFO', 'User logged in.', 12),
            LogEntry('2023-08-18 12:15:15', 'WARN', 'Memory high.', 12),
            LogEntry('2023-08-18 12:30:30', 'ERROR', 'Database error.', 12),
            LogEntry('2023-08-18 13:00:00', 'ERROR', 'Database error.', 13),
            LogEntry('2023-08-18 13:15:15', 'ERROR', 'Disk error.', 13),
            LogEntry('2023-08-18 14:00:00', 'INFO', 'Backup complete.', 14),
            LogEntry('2023-08-18 14:15:15', 'ERROR', 'Database error.', 14),
            LogEntry('2023-08-18 15:00:00', 'WARN', 'CPU high.', 15),
        ]
    
    def test_add_entries(self):
        """Test adding entries to analyzer."""
        analyzer = LogAnalyzer()
        entries = self.create_sample_entries()
        
        analyzer.add_entries(entries)
        
        assert len(analyzer.entries) == 8
    
    def test_generate_summary_total_entries(self):
        """Test summary generation - total entries."""
        analyzer = LogAnalyzer()
        analyzer.add_entries(self.create_sample_entries())
        
        summary = analyzer.generate_summary()
        
        assert summary['total_entries'] == 8
    
    def test_generate_summary_by_severity(self):
        """Test summary generation - entries by severity."""
        analyzer = LogAnalyzer()
        analyzer.add_entries(self.create_sample_entries())
        
        summary = analyzer.generate_summary()
        
        assert summary['entries_by_severity']['ERROR'] == 4
        assert summary['entries_by_severity']['WARN'] == 2
        assert summary['entries_by_severity']['INFO'] == 2
    
    def test_generate_summary_top_errors(self):
        """Test summary generation - top 3 error messages."""
        analyzer = LogAnalyzer()
        analyzer.add_entries(self.create_sample_entries())
        
        summary = analyzer.generate_summary()
        top_errors = summary['top_3_error_messages']
        
        assert len(top_errors) <= 3
        assert top_errors[0]['message'] == 'Database error.'
        assert top_errors[0]['count'] == 3
        assert top_errors[1]['message'] == 'Disk error.'
        assert top_errors[1]['count'] == 1
    
    def test_generate_summary_errors_by_hour(self):
        """Test summary generation - errors by hour."""
        analyzer = LogAnalyzer()
        analyzer.add_entries(self.create_sample_entries())
        
        summary = analyzer.generate_summary()
        errors_by_hour = {item['hour']: item['count'] for item in summary['errors_by_hour']}
        
        assert errors_by_hour[12] == 1
        assert errors_by_hour[13] == 2
        assert errors_by_hour[14] == 1
        assert 15 not in errors_by_hour  # No errors at hour 15
    
    def test_export_json(self, tmp_path):
        """Test JSON export functionality."""
        analyzer = LogAnalyzer()
        analyzer.add_entries(self.create_sample_entries())
        
        output_file = tmp_path / 'test_summary.json'
        analyzer.export_json(output_file)
        
        assert output_file.exists()
        
        with open(output_file, 'r') as f:
            data = json.load(f)
            assert 'total_entries' in data
            assert 'entries_by_severity' in data
            assert 'top_3_error_messages' in data
            assert 'errors_by_hour' in data
            assert data['total_entries'] == 8
    
    def test_empty_analyzer(self):
        """Test analyzer with no entries."""
        analyzer = LogAnalyzer()
        summary = analyzer.generate_summary()
        
        assert summary['total_entries'] == 0
        assert len(summary['entries_by_severity']) == 0
        assert len(summary['top_3_error_messages']) == 0
        assert len(summary['errors_by_hour']) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])