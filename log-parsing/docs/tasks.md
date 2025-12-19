# Log Parsing Tasks

## Overview
This directory contains a log analysis system that parses server logs from multiple formats (TXT, XML, CSV) and generates comprehensive summary reports in JSON format.

## Core Requirements

### 1. Multi-Format Log Parsing
- [ ] Parse [`log.txt`](../log.txt) - Plain text format
- [ ] Parse [`log2.xml`](../log2.xml) - XML format
- [ ] Parse [`log3.csv`](../log3.csv) - CSV format
- [ ] Extract from each entry:
  - Timestamp
  - Severity level (ERROR, WARN, INFO, DEBUG, etc.)
  - Message content
- [ ] Handle malformed log entries gracefully
- [ ] Normalize data from different formats into unified structure

### 2. Log Analysis Script
- [ ] Create main analysis script (language of choice)
- [ ] Implement parsers for each format:
  - Text parser for `.txt` files
  - XML parser for `.xml` files
  - CSV parser for `.csv` files
- [ ] Combine parsed data from all sources
- [ ] Validate and clean log entries
- [ ] Handle parsing errors without crashing

### 3. Summary Report Generation
- [ ] Generate JSON format output
- [ ] Calculate total number of log entries
- [ ] Break down entries by severity level:
  - ERROR count
  - WARN count
  - INFO count
  - DEBUG count
  - Other levels (if present)
- [ ] Identify three most frequent error messages
- [ ] Count occurrences for each frequent error
- [ ] Break down error messages by hour of day (0-23)
- [ ] Format output as valid, well-structured JSON

### 4. Error Handling & Robustness
- [ ] Handle missing files gracefully
- [ ] Skip malformed log entries with warning
- [ ] Handle incomplete timestamp data
- [ ] Deal with missing severity levels
- [ ] Handle empty or corrupted log files
- [ ] Validate XML structure
- [ ] Handle CSV parsing errors
- [ ] Log parsing issues to stderr or log file

## Implementation Tasks

### Parser Development
- [ ] Create base parser interface/class
- [ ] Implement text log parser
  - Regular expression for pattern matching
  - Timestamp extraction and parsing
  - Severity level extraction
  - Message extraction
- [ ] Implement XML log parser
  - XML tree parsing
  - Element extraction
  - Attribute handling
- [ ] Implement CSV log parser
  - CSV reading with proper delimiter handling
  - Column mapping
  - Header validation

### Data Processing
- [ ] Create unified log entry data structure
- [ ] Normalize timestamps to consistent format
- [ ] Standardize severity levels (case-insensitive)
- [ ] Clean and trim message content
- [ ] Extract hour from timestamp for hourly breakdown
- [ ] Group errors by message content
- [ ] Sort errors by frequency

### Report Generation
- [ ] Create JSON report structure
- [ ] Format summary statistics
- [ ] Format severity breakdown
- [ ] Format top 3 error messages with counts
- [ ] Format hourly error breakdown
- [ ] Pretty-print JSON output
- [ ] Save report to file

## Files to Create

### Main Implementation
- `analyze_logs.py` (or `.js`, `.rb`, etc.) - Main analysis script
- `parsers/` - Directory for parser modules
  - `text_parser.py` - Text log parser
  - `xml_parser.py` - XML log parser
  - `csv_parser.py` - CSV log parser
- `models/` - Data models
  - `log_entry.py` - Log entry data structure
- `utils/` - Utility functions
  - `time_utils.py` - Timestamp parsing utilities
  - `report_generator.py` - JSON report generation

### Output
- `output/summary_report.json` - Generated analysis report
- `output/parsing_errors.log` - Log of parsing issues (optional)

### Documentation
- `README.md` - Usage instructions and examples
- `DESIGN.md` - Architecture and design decisions (optional)

## Expected JSON Output Structure

```json
{
  "summary": {
    "total_entries": 1500,
    "parsing_errors": 5,
    "date_range": {
      "earliest": "2024-01-01T00:00:00Z",
      "latest": "2024-01-07T23:59:59Z"
    }
  },
  "severity_breakdown": {
    "ERROR": 245,
    "WARN": 380,
    "INFO": 750,
    "DEBUG": 125
  },
  "top_errors": [
    {
      "message": "Database connection timeout",
      "count": 87
    },
    {
      "message": "Failed to load configuration file",
      "count": 56
    },
    {
      "message": "Authentication failed for user",
      "count": 42
    }
  ],
  "errors_by_hour": {
    "0": 8,
    "1": 5,
    "2": 3,
    "3": 4,
    "4": 6,
    "5": 12,
    "6": 18,
    "7": 25,
    "8": 32,
    "9": 28,
    "10": 22,
    "11": 19,
    "12": 15,
    "13": 17,
    "14": 20,
    "15": 24,
    "16": 21,
    "17": 18,
    "18": 14,
    "19": 11,
    "20": 9,
    "21": 7,
    "22": 6,
    "23": 5
  }
}
```

## Language-Specific Considerations

### Python
- [ ] Use `csv` module for CSV parsing
- [ ] Use `xml.etree.ElementTree` or `lxml` for XML
- [ ] Use `re` module for text pattern matching
- [ ] Use `json` module for output generation
- [ ] Use `datetime` for timestamp handling
- [ ] Consider `pandas` for advanced analysis (optional)

### JavaScript/Node.js
- [ ] Use `fs` module for file reading
- [ ] Use `csv-parse` or similar for CSV
- [ ] Use `xml2js` or `fast-xml-parser` for XML
- [ ] Use built-in `JSON.stringify()` for output
- [ ] Use `Date` object for timestamp handling

### Ruby
- [ ] Use `CSV` class for CSV parsing
- [ ] Use `REXML` or `Nokogiri` for XML
- [ ] Use regular expressions for text parsing
- [ ] Use `JSON` module for output
- [ ] Use `Time` or `DateTime` for timestamps

## Testing Considerations

### Test Cases
- [ ] Test each parser independently
- [ ] Test with valid log entries
- [ ] Test with malformed entries
- [ ] Test with empty files
- [ ] Test with missing files
- [ ] Test timestamp parsing edge cases
- [ ] Test severity level normalization
- [ ] Test error frequency calculation
- [ ] Test hourly breakdown calculation
- [ ] Test JSON output validity

### Edge Cases
- [ ] Logs with no errors
- [ ] Logs with only errors
- [ ] Duplicate log entries
- [ ] Logs spanning multiple days
- [ ] Logs with non-standard severity levels
- [ ] Logs with multi-line messages
- [ ] Logs with special characters
- [ ] Very large log files

## Performance Considerations
- [ ] Stream large files instead of loading entirely into memory
- [ ] Use efficient data structures (dictionaries/maps for counting)
- [ ] Consider parallel processing for multiple files
- [ ] Optimize regex patterns for text parsing
- [ ] Profile code for bottlenecks

## Code Quality
- [ ] Write clear, self-documenting code
- [ ] Add comments for complex logic
- [ ] Use meaningful variable names
- [ ] Follow language-specific style guides
- [ ] Handle exceptions properly
- [ ] Add logging for debugging
- [ ] Validate input parameters

## Usage Example

```bash
# Python
python analyze_logs.py --output output/summary_report.json

# Node.js
node analyze_logs.js --output output/summary_report.json

# Ruby
ruby analyze_logs.rb --output output/summary_report.json
```

## Time Estimate
- Parser implementation: 1-1.5 hours
- Analysis logic: 30-45 minutes
- Report generation: 30 minutes
- Testing and refinement: 30-45 minutes
- **Total: 2.5-3.5 hours**

## Success Criteria
- [ ] All three log formats successfully parsed
- [ ] Malformed entries handled without crashes
- [ ] Valid JSON output generated
- [ ] All required statistics calculated correctly
- [ ] Top 3 errors identified accurately
- [ ] Hourly breakdown complete and accurate
- [ ] Code is clean and well-documented
- [ ] Edge cases handled appropriately

## Bonus Features
- [ ] Add command-line arguments for flexibility
- [ ] Support additional log formats
- [ ] Generate HTML report in addition to JSON
- [ ] Add visualization of hourly error distribution
- [ ] Implement log filtering by date range
- [ ] Add support for custom severity levels
- [ ] Create interactive dashboard for results
- [ ] Add email alerting for critical errors