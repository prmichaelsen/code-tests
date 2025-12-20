# Inventory Reconciliation - Implementation Notes

## Overview
This document summarizes the key decisions, assumptions, data quality issues, and approach taken for the inventory reconciliation project.

## Approach

### 1. Data Loading Strategy
- Used Python's built-in `csv` module for parsing (lightweight, no external dependencies beyond pytest)
- Implemented flexible column name handling to accommodate different naming conventions between snapshots
- Added comprehensive error handling for malformed data

### 2. SKU Normalization
- Normalized all SKUs to uppercase with hyphen format (e.g., `SKU-001`)
- This handles inconsistencies like `SKU005`, `sku-008`, `SKU018`
- Ensures accurate matching between snapshots despite format variations

### 3. Reconciliation Logic
- Categorized changes into 4 types: `added`, `removed`, `modified`, `unchanged`
- Calculated quantity differences for all items
- Flagged unusual changes (>1000% quantity change) as potential data quality issues

### 4. Data Quality Checks
Implemented multi-level severity system:
- **High Severity**: Negative quantities, duplicate SKUs, parse errors
- **Medium Severity**: SKU format inconsistencies, unusual quantity changes
- **Low Severity**: Whitespace issues in names

## Key Decisions

### Column Name Flexibility
**Decision**: Support multiple column name variations (`name`/`product_name`, `quantity`/`qty`, etc.)

**Rationale**: Real-world systems often have inconsistent naming conventions. This makes the tool more robust and reusable.

### Whitespace Handling
**Decision**: Detect whitespace issues but store cleaned data

**Rationale**: Whitespace issues are common data quality problems that should be flagged, but shouldn't prevent reconciliation. We detect them before cleaning to maintain data quality visibility.

### Decimal Quantity Support
**Decision**: Use `float` for quantities instead of `int`

**Rationale**: Some items may have fractional quantities (e.g., partial units, weight-based items). The data contained decimal values like `70.0` and `80.00`.

### Output Formats
**Decision**: Generate CSV, JSON, and human-readable text outputs

**Rationale**: 
- CSV for spreadsheet analysis
- JSON for programmatic consumption
- Text for quick human review

## Data Quality Issues Found

### High Severity (2 issues)
1. **Negative Quantity**: SKU-045 has quantity of -5 in snapshot 2
   - This is clearly erroneous and needs investigation
   
2. **Duplicate SKU**: SKU-045 appears twice in snapshot 2
   - First occurrence: "Multimeter Professional" with 23 units
   - Second occurrence: "Multimeter Pro" with -5 units
   - Likely a data entry error or system bug

### Medium Severity (3 issues)
1. **SKU Format Inconsistencies**: 
   - `SKU005` → `SKU-005`
   - `sku-008` → `SKU-008`
   - `SKU018` → `SKU-018`
   - Indicates inconsistent data entry practices

### Low Severity (5 issues)
1. **Whitespace in Names**:
   - Leading/trailing spaces in 5 product names
   - Examples: ` Widget B`, `Cable Ties 100pk `, ` HDMI Cable 3ft `
   - Suggests copy-paste errors or inconsistent data entry

## Reconciliation Results

### Summary Statistics
- **Snapshot 1**: 75 items
- **Snapshot 2**: 78 items
- **Net Change**: +3 items

### Changes Breakdown
- **Added**: 5 items (SKU-076 through SKU-080)
  - New streaming/capture equipment added to inventory
- **Removed**: 2 items (SKU-025, SKU-026)
  - VGA and DVI cables removed (likely obsolete technology)
- **Modified**: 71 items
  - Most items had quantity changes (typical for active inventory)
- **Unchanged**: 2 items
  - SKU-006 and SKU-007 maintained same quantities

### Notable Patterns
1. **Quantity Decreases**: Most items showed small decreases (5-25 units)
   - Consistent with normal sales/usage over one week
2. **Large Decreases**: Some items like thermal paste (-150 units) and cable ties (-80 units)
   - High-volume consumables showing expected usage patterns
3. **Technology Shift**: Removal of legacy video cables (VGA, DVI), addition of modern streaming equipment
   - Indicates inventory modernization

## Testing Strategy

### Test Coverage
Implemented 20 comprehensive tests covering:
- SKU normalization (4 tests)
- Data loading and parsing (2 tests)
- Data quality detection (5 tests)
- Reconciliation logic (4 tests)
- Export functionality (3 tests)
- Edge cases (2 tests)

### Test Philosophy
- Used pytest for clean, readable tests
- Created temporary files for isolation
- Tested both happy paths and error conditions
- Achieved 100% test pass rate

## Potential Improvements

### Short Term
1. Add command-line arguments for custom file paths
2. Support additional output formats (Excel, HTML report)
3. Add email notification for high-severity issues
4. Implement configurable thresholds for unusual changes

### Long Term
1. Database integration for historical tracking
2. Web dashboard for visualization
3. Automated reconciliation scheduling
4. Machine learning for anomaly detection
5. Integration with warehouse management systems

## Technical Decisions

### Why Python 3.10+?
- Modern type hints for better code clarity
- Dataclasses for clean data modeling
- Pathlib for cross-platform file handling
- Strong CSV/JSON support in standard library

### Why No Pandas?
- Kept dependencies minimal (only pytest)
- Built-in csv module sufficient for this data size
- Easier deployment without heavy dependencies
- Demonstrates core Python proficiency

### Error Handling Philosophy
- Fail gracefully with informative messages
- Continue processing despite individual row errors
- Collect all issues for comprehensive reporting
- Never silently ignore problems

## Conclusion

The reconciliation tool successfully identified all changes between snapshots and flagged 10 data quality issues across 3 severity levels. The most critical finding is the duplicate SKU-045 with negative quantity, which requires immediate attention. The tool is production-ready with comprehensive test coverage and clear, actionable output.