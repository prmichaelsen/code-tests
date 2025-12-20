#!/usr/bin/env python3
"""
Log Analysis Script

Parses log files in multiple formats (TXT, XML, CSV) and generates
a comprehensive JSON summary report with error analysis.
"""

import csv
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from collections import Counter, defaultdict


@dataclass
class LogEntry:
    """Represents a single log entry."""
    timestamp: str
    severity: str
    message: str
    hour: int
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LogEntry':
        """Create LogEntry from dictionary."""
        timestamp = data['timestamp']
        # Extract hour from timestamp
        hour = cls.extract_hour(timestamp)
        return cls(
            timestamp=timestamp,
            severity=data['severity'],
            message=data['message'],
            hour=hour
        )
    
    @staticmethod
    def extract_hour(timestamp: str) -> int:
        """Extract hour from timestamp string."""
        # Handle multiple timestamp formats
        patterns = [
            r'(\d{4}-\d{2}-\d{2})[T\s](\d{2}):',  # ISO format or space-separated
            r'\[(\d{4}-\d{2}-\d{2})\s+(\d{2}):',  # Bracketed format
        ]
        
        for pattern in patterns:
            match = re.search(pattern, timestamp)
            if match:
                return int(match.group(2))
        
        return 0  # Default if parsing fails


class LogParser:
    """Base class for log parsers."""
    
    def parse(self, filepath: Path) -> List[LogEntry]:
        """Parse log file and return list of LogEntry objects."""
        raise NotImplementedError


class TxtLogParser(LogParser):
    """Parser for text format logs."""
    
    def parse(self, filepath: Path) -> List[LogEntry]:
        """Parse TXT log file."""
        entries = []
        pattern = r'\[([^\]]+)\]\s+\[([^\]]+)\]\s+(.+)'
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                
                match = re.match(pattern, line)
                if match:
                    timestamp, severity, message = match.groups()
                    try:
                        entry = LogEntry.from_dict({
                            'timestamp': timestamp,
                            'severity': severity.strip(),
                            'message': message.strip()
                        })
                        entries.append(entry)
                    except Exception as e:
                        print(f"Warning: Failed to parse line {line_num} in {filepath}: {e}")
                else:
                    print(f"Warning: Malformed entry at line {line_num} in {filepath}: {line}")
        
        return entries


class XmlLogParser(LogParser):
    """Parser for XML format logs."""
    
    def parse(self, filepath: Path) -> List[LogEntry]:
        """Parse XML log file."""
        entries = []
        
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            for log_elem in root.findall('log'):
                try:
                    timestamp_elem = log_elem.find('timestamp')
                    severity_elem = log_elem.find('severity')
                    message_elem = log_elem.find('message')
                    
                    if timestamp_elem is not None and severity_elem is not None and message_elem is not None:
                        entry = LogEntry.from_dict({
                            'timestamp': timestamp_elem.text or '',
                            'severity': severity_elem.text or '',
                            'message': message_elem.text or ''
                        })
                        entries.append(entry)
                    else:
                        print(f"Warning: Incomplete log entry in {filepath}")
                except Exception as e:
                    print(f"Warning: Failed to parse XML log entry in {filepath}: {e}")
        
        except ET.ParseError as e:
            print(f"Error: Failed to parse XML file {filepath}: {e}")
        
        return entries


class CsvLogParser(LogParser):
    """Parser for CSV format logs."""
    
    def parse(self, filepath: Path) -> List[LogEntry]:
        """Parse CSV log file."""
        entries = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is line 1)
                try:
                    if 'timestamp' in row and 'severity' in row and 'message' in row:
                        entry = LogEntry.from_dict({
                            'timestamp': row['timestamp'].strip(),
                            'severity': row['severity'].strip(),
                            'message': row['message'].strip()
                        })
                        entries.append(entry)
                    else:
                        print(f"Warning: Missing required fields at row {row_num} in {filepath}")
                except Exception as e:
                    print(f"Warning: Failed to parse row {row_num} in {filepath}: {e}")
        
        return entries


class LogAnalyzer:
    """Analyzes parsed log entries and generates summary report."""
    
    def __init__(self):
        self.entries: List[LogEntry] = []
    
    def add_entries(self, entries: List[LogEntry]) -> None:
        """Add log entries to the analyzer."""
        self.entries.extend(entries)
    
    def generate_summary(self) -> Dict:
        """Generate comprehensive summary report."""
        total_entries = len(self.entries)
        
        # Count by severity
        severity_counts = Counter(entry.severity for entry in self.entries)
        
        # Get error entries only
        error_entries = [entry for entry in self.entries if entry.severity == 'ERROR']
        
        # Count error messages
        error_message_counts = Counter(entry.message for entry in error_entries)
        top_3_errors = [
            {'message': msg, 'count': count}
            for msg, count in error_message_counts.most_common(3)
        ]
        
        # Count errors by hour
        errors_by_hour = defaultdict(int)
        for entry in error_entries:
            errors_by_hour[entry.hour] += 1
        
        # Convert to sorted list of dicts for JSON output
        errors_by_hour_list = [
            {'hour': hour, 'count': count}
            for hour, count in sorted(errors_by_hour.items())
        ]
        
        summary = {
            'total_entries': total_entries,
            'entries_by_severity': dict(severity_counts),
            'top_3_error_messages': top_3_errors,
            'errors_by_hour': errors_by_hour_list,
            'analysis_metadata': {
                'total_error_count': len(error_entries),
                'total_warn_count': severity_counts.get('WARN', 0),
                'total_info_count': severity_counts.get('INFO', 0),
                'unique_error_messages': len(error_message_counts),
                'hours_with_errors': len(errors_by_hour)
            }
        }
        
        return summary
    
    def export_json(self, output_path: Path) -> None:
        """Export summary report to JSON file."""
        summary = self.generate_summary()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
    
    def print_summary(self) -> None:
        """Print human-readable summary to console."""
        summary = self.generate_summary()
        
        print("\n" + "=" * 70)
        print("LOG ANALYSIS SUMMARY")
        print("=" * 70 + "\n")
        
        print(f"Total Log Entries: {summary['total_entries']}")
        print("\nEntries by Severity:")
        for severity, count in sorted(summary['entries_by_severity'].items()):
            print(f"  {severity:6s}: {count:4d}")
        
        print("\nTop 3 Error Messages:")
        for i, error in enumerate(summary['top_3_error_messages'], 1):
            print(f"  {i}. {error['message']} ({error['count']} occurrences)")
        
        print(f"\nErrors by Hour of Day ({len(summary['errors_by_hour'])} hours with errors):")
        for hour_data in summary['errors_by_hour']:
            hour = hour_data['hour']
            count = hour_data['count']
            bar = '█' * (count // 2)  # Visual bar chart
            print(f"  {hour:02d}:00 - {count:3d} errors {bar}")
        
        print("\n" + "=" * 70 + "\n")


def main():
    """Main entry point."""
    # Setup paths
    base_dir = Path(__file__).parent
    output_dir = base_dir / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Initialize analyzer
    analyzer = LogAnalyzer()
    
    print("\n" + "=" * 70)
    print("LOG PARSING AND ANALYSIS")
    print("=" * 70 + "\n")
    
    # Parse log.txt
    txt_file = base_dir / 'log.txt'
    if txt_file.exists():
        print(f"Parsing {txt_file.name}...")
        parser = TxtLogParser()
        entries = parser.parse(txt_file)
        analyzer.add_entries(entries)
        print(f"  ✓ Parsed {len(entries)} entries from TXT format")
    
    # Parse log2.xml
    xml_file = base_dir / 'log2.xml'
    if xml_file.exists():
        print(f"Parsing {xml_file.name}...")
        parser = XmlLogParser()
        entries = parser.parse(xml_file)
        analyzer.add_entries(entries)
        print(f"  ✓ Parsed {len(entries)} entries from XML format")
    
    # Parse log3.csv
    csv_file = base_dir / 'log3.csv'
    if csv_file.exists():
        print(f"Parsing {csv_file.name}...")
        parser = CsvLogParser()
        entries = parser.parse(csv_file)
        analyzer.add_entries(entries)
        print(f"  ✓ Parsed {len(entries)} entries from CSV format")
    
    # Generate and export summary
    output_file = output_dir / 'log_summary.json'
    print(f"\nGenerating summary report...")
    analyzer.export_json(output_file)
    print(f"  ✓ Summary exported to {output_file}")
    
    # Print summary to console
    analyzer.print_summary()


if __name__ == '__main__':
    main()