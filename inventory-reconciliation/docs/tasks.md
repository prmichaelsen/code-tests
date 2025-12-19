# Inventory Reconciliation Tasks

## Overview
This directory contains a Python-based inventory reconciliation system that compares warehouse inventory snapshots taken a week apart to identify changes, discrepancies, and data quality issues.

## Core Requirements

### 1. Data Analysis & Comparison
- [ ] Load and parse [`data/snapshot_1.csv`](../data/snapshot_1.csv) (week-old snapshot)
- [ ] Load and parse [`data/snapshot_2.csv`](../data/snapshot_2.csv) (current snapshot)
- [ ] Identify common items between both snapshots
- [ ] Detect quantity changes for items present in both snapshots
- [ ] Find items only in snapshot 1 (removed/sold out)
- [ ] Find items only in snapshot 2 (newly added)
- [ ] Flag data quality issues (duplicates, missing values, invalid data, etc.)

### 2. Reconciliation Script (`reconcile.py`)
- [ ] Create main reconciliation script
- [ ] Implement CSV parsing with error handling
- [ ] Build comparison logic for inventory items
- [ ] Handle edge cases (missing fields, malformed data)
- [ ] Calculate quantity differences
- [ ] Categorize changes (added, removed, modified, unchanged)
- [ ] Generate structured output (CSV or JSON)

### 3. Output Generation
- [ ] Create `output/` directory structure
- [ ] Generate reconciliation report in CSV format
- [ ] Generate reconciliation report in JSON format (optional)
- [ ] Include summary statistics:
  - Total items in each snapshot
  - Items added
  - Items removed
  - Items with quantity changes
  - Data quality issues found
- [ ] Create detailed change log with:
  - Item ID
  - Item name
  - Change type (added/removed/modified)
  - Old quantity (if applicable)
  - New quantity (if applicable)
  - Quantity difference

### 4. Testing (`tests/`)
- [ ] Set up testing framework (pytest recommended)
- [ ] Create test fixtures with sample data
- [ ] Test CSV parsing functionality
- [ ] Test comparison logic for:
  - Items in both snapshots
  - Items only in snapshot 1
  - Items only in snapshot 2
  - Quantity change calculations
- [ ] Test data quality checks
- [ ] Test edge cases:
  - Empty snapshots
  - Malformed CSV data
  - Missing required fields
  - Duplicate item IDs
- [ ] Test output generation
- [ ] Achieve reasonable test coverage (>80%)

### 5. Documentation (`NOTES.md`)
- [ ] Document key decisions made
- [ ] Explain assumptions about data structure
- [ ] List data quality issues discovered
- [ ] Describe approach to problem-solving
- [ ] Document any trade-offs or limitations
- [ ] Note potential improvements or extensions
- [ ] Keep to approximately half-page length

## Data Quality Checks to Implement

### Required Validations
- [ ] Check for duplicate item IDs
- [ ] Validate required fields are present
- [ ] Check for negative quantities
- [ ] Identify missing or null values
- [ ] Detect inconsistent data types
- [ ] Flag unusual quantity changes (e.g., >1000% increase)
- [ ] Validate item ID format consistency
- [ ] Check for whitespace issues in item names

## Files to Create

### Main Implementation
- `reconcile.py` - Main reconciliation script
- `requirements.txt` - Python dependencies
- `README.md` - Setup and usage instructions (optional)

### Testing
- `tests/__init__.py` - Test package initialization
- `tests/test_reconcile.py` - Main test suite
- `tests/fixtures/` - Test data fixtures
- `tests/conftest.py` - Pytest configuration (if needed)

### Output
- `output/reconciliation_report.csv` - CSV format report
- `output/reconciliation_report.json` - JSON format report (optional)
- `output/summary.txt` - Human-readable summary

### Documentation
- `NOTES.md` - Decision log and findings

## Technical Guidelines

### Python Requirements
- [ ] Use Python 3.10 or higher
- [ ] Follow PEP 8 style guidelines
- [ ] Use type hints where appropriate
- [ ] Write clear, self-documenting code

### Recommended Libraries
- [ ] `pandas` - For CSV manipulation and analysis
- [ ] `pytest` - For testing
- [ ] `csv` (built-in) - Alternative to pandas for lightweight parsing
- [ ] `json` (built-in) - For JSON output
- [ ] `dataclasses` - For structured data models

### Code Quality
- [ ] Add docstrings to functions and classes
- [ ] Include inline comments for complex logic
- [ ] Handle exceptions gracefully
- [ ] Log important operations and errors
- [ ] Use meaningful variable and function names

## Git Workflow
- [ ] Make initial commit with project structure
- [ ] Commit after implementing CSV parsing
- [ ] Commit after implementing comparison logic
- [ ] Commit after adding tests
- [ ] Commit after generating output
- [ ] Commit after completing documentation
- [ ] Use clear, descriptive commit messages

## Example Output Structure

### CSV Report Format
```csv
item_id,item_name,change_type,old_quantity,new_quantity,quantity_difference
SKU001,Widget A,modified,100,85,-15
SKU002,Widget B,removed,50,0,-50
SKU003,Widget C,added,0,200,200
```

### JSON Report Format
```json
{
  "summary": {
    "snapshot_1_total": 150,
    "snapshot_2_total": 175,
    "items_added": 30,
    "items_removed": 5,
    "items_modified": 20,
    "data_quality_issues": 3
  },
  "changes": [...]
}
```

## Time Estimate
- Data analysis and script development: 1-1.5 hours
- Testing implementation: 30-45 minutes
- Output generation and formatting: 15-30 minutes
- Documentation: 15-30 minutes
- **Total: 1.5-3 hours** (most candidates complete in this range)

## Success Criteria
- [ ] Script successfully processes both CSV files
- [ ] All change types correctly identified
- [ ] Data quality issues properly flagged
- [ ] Tests pass with good coverage
- [ ] Output is clear and actionable
- [ ] Documentation explains approach and findings
- [ ] Code is clean, readable, and maintainable
- [ ] Git history shows incremental progress

## Submission Checklist
- [ ] All code committed to repository
- [ ] Tests are passing
- [ ] Output files generated in `output/` directory
- [ ] `NOTES.md` completed
- [ ] Code is well-documented
- [ ] Repository pushed to remote
- [ ] Interviewer notified of completion