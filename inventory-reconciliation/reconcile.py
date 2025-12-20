#!/usr/bin/env python3
"""
Inventory Reconciliation Script

Compares two inventory snapshots to identify changes, discrepancies,
and data quality issues.
"""

import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime


@dataclass
class InventoryItem:
    """Represents a single inventory item."""
    sku: str
    name: str
    quantity: float
    location: str
    date: str
    
    def normalize_sku(self) -> str:
        """Normalize SKU format to uppercase with hyphen."""
        sku = self.sku.strip().upper()
        # Add hyphen if missing (e.g., SKU005 -> SKU-005)
        if sku.startswith('SKU') and len(sku) > 3 and sku[3] != '-':
            sku = f"SKU-{sku[3:]}"
        return sku


@dataclass
class DataQualityIssue:
    """Represents a data quality issue found during reconciliation."""
    issue_type: str
    sku: str
    description: str
    severity: str  # 'high', 'medium', 'low'


@dataclass
class InventoryChange:
    """Represents a change between two inventory snapshots."""
    sku: str
    name: str
    change_type: str  # 'added', 'removed', 'modified', 'unchanged'
    old_quantity: Optional[float]
    new_quantity: Optional[float]
    quantity_difference: Optional[float]
    old_location: Optional[str]
    new_location: Optional[str]


@dataclass
class ReconciliationReport:
    """Complete reconciliation report."""
    summary: Dict
    changes: List[InventoryChange]
    data_quality_issues: List[DataQualityIssue]


class InventoryReconciler:
    """Handles inventory reconciliation between two snapshots."""
    
    def __init__(self):
        self.snapshot1: Dict[str, InventoryItem] = {}
        self.snapshot2: Dict[str, InventoryItem] = {}
        self.data_quality_issues: List[DataQualityIssue] = []
    
    def load_snapshot(self, filepath: Path, snapshot_num: int) -> Dict[str, InventoryItem]:
        """Load and parse a CSV snapshot file."""
        items = {}
        seen_skus = set()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    # Handle different column names between snapshots
                    sku = row.get('sku', '').strip()
                    name = row.get('name') or row.get('product_name', '')
                    # Don't strip name yet - need to check for whitespace issues first
                    
                    # Parse quantity (handle decimals and empty values)
                    qty_str = row.get('quantity') or row.get('qty', '0')
                    try:
                        quantity = float(qty_str)
                    except ValueError:
                        quantity = 0.0
                        self.data_quality_issues.append(DataQualityIssue(
                            issue_type='invalid_quantity',
                            sku=sku,
                            description=f"Invalid quantity value '{qty_str}' in row {row_num}",
                            severity='high'
                        ))
                    
                    location = row.get('location') or row.get('warehouse', '')
                    location = location.strip()
                    
                    date = row.get('last_counted') or row.get('updated_at', '')
                    date = date.strip()
                    
                    # Create item (with original name for whitespace checking)
                    item = InventoryItem(sku, name, quantity, location, date)
                    normalized_sku = item.normalize_sku()
                    
                    # Check for data quality issues
                    self._check_item_quality(item, normalized_sku, row_num, seen_skus)
                    
                    # Now strip the name for storage
                    item.name = item.name.strip()
                    
                    # Store item (use normalized SKU as key)
                    if normalized_sku in items:
                        # Duplicate SKU
                        self.data_quality_issues.append(DataQualityIssue(
                            issue_type='duplicate_sku',
                            sku=normalized_sku,
                            description=f"Duplicate SKU '{normalized_sku}' found in row {row_num}",
                            severity='high'
                        ))
                    
                    items[normalized_sku] = item
                    seen_skus.add(normalized_sku)
                    
                except Exception as e:
                    self.data_quality_issues.append(DataQualityIssue(
                        issue_type='parse_error',
                        sku=sku if 'sku' in locals() else 'unknown',
                        description=f"Error parsing row {row_num}: {str(e)}",
                        severity='high'
                    ))
        
        return items
    
    def _check_item_quality(self, item: InventoryItem, normalized_sku: str, 
                           row_num: int, seen_skus: Set[str]) -> None:
        """Check for data quality issues in an item."""
        
        # Check for negative quantities
        if item.quantity < 0:
            self.data_quality_issues.append(DataQualityIssue(
                issue_type='negative_quantity',
                sku=normalized_sku,
                description=f"Negative quantity {item.quantity} for SKU '{normalized_sku}'",
                severity='high'
            ))
        
        # Check for SKU format inconsistencies
        if item.sku != normalized_sku:
            self.data_quality_issues.append(DataQualityIssue(
                issue_type='sku_format_inconsistency',
                sku=normalized_sku,
                description=f"SKU format inconsistency: '{item.sku}' normalized to '{normalized_sku}'",
                severity='medium'
            ))
        
        # Check for whitespace issues in name
        if item.name != item.name.strip():
            self.data_quality_issues.append(DataQualityIssue(
                issue_type='whitespace_in_name',
                sku=normalized_sku,
                description=f"Leading/trailing whitespace in name: '{item.name}'",
                severity='low'
            ))
        
        # Check for missing required fields
        if not item.sku:
            self.data_quality_issues.append(DataQualityIssue(
                issue_type='missing_sku',
                sku='UNKNOWN',
                description=f"Missing SKU in row {row_num}",
                severity='high'
            ))
        
        if not item.name:
            self.data_quality_issues.append(DataQualityIssue(
                issue_type='missing_name',
                sku=normalized_sku,
                description=f"Missing name for SKU '{normalized_sku}'",
                severity='medium'
            ))
    
    def reconcile(self, snapshot1_path: Path, snapshot2_path: Path) -> ReconciliationReport:
        """Perform reconciliation between two snapshots."""
        
        # Load both snapshots
        print(f"Loading {snapshot1_path}...")
        self.snapshot1 = self.load_snapshot(snapshot1_path, 1)
        
        print(f"Loading {snapshot2_path}...")
        self.snapshot2 = self.load_snapshot(snapshot2_path, 2)
        
        # Get all unique SKUs
        all_skus = set(self.snapshot1.keys()) | set(self.snapshot2.keys())
        
        changes: List[InventoryChange] = []
        
        for sku in sorted(all_skus):
            item1 = self.snapshot1.get(sku)
            item2 = self.snapshot2.get(sku)
            
            if item1 and item2:
                # Item exists in both snapshots
                qty_diff = item2.quantity - item1.quantity
                
                if qty_diff != 0:
                    change_type = 'modified'
                    
                    # Flag unusual quantity changes
                    if item1.quantity > 0:
                        pct_change = abs(qty_diff / item1.quantity) * 100
                        if pct_change > 1000:
                            self.data_quality_issues.append(DataQualityIssue(
                                issue_type='unusual_quantity_change',
                                sku=sku,
                                description=f"Unusual quantity change: {pct_change:.1f}% change for SKU '{sku}'",
                                severity='medium'
                            ))
                else:
                    change_type = 'unchanged'
                
                changes.append(InventoryChange(
                    sku=sku,
                    name=item2.name.strip(),
                    change_type=change_type,
                    old_quantity=item1.quantity,
                    new_quantity=item2.quantity,
                    quantity_difference=qty_diff,
                    old_location=item1.location,
                    new_location=item2.location
                ))
                
            elif item1 and not item2:
                # Item removed
                changes.append(InventoryChange(
                    sku=sku,
                    name=item1.name.strip(),
                    change_type='removed',
                    old_quantity=item1.quantity,
                    new_quantity=0,
                    quantity_difference=-item1.quantity,
                    old_location=item1.location,
                    new_location=None
                ))
                
            elif item2 and not item1:
                # Item added
                changes.append(InventoryChange(
                    sku=sku,
                    name=item2.name.strip(),
                    change_type='added',
                    old_quantity=0,
                    new_quantity=item2.quantity,
                    quantity_difference=item2.quantity,
                    old_location=None,
                    new_location=item2.location
                ))
        
        # Calculate summary statistics
        summary = {
            'snapshot_1_total_items': len(self.snapshot1),
            'snapshot_2_total_items': len(self.snapshot2),
            'items_added': sum(1 for c in changes if c.change_type == 'added'),
            'items_removed': sum(1 for c in changes if c.change_type == 'removed'),
            'items_modified': sum(1 for c in changes if c.change_type == 'modified'),
            'items_unchanged': sum(1 for c in changes if c.change_type == 'unchanged'),
            'data_quality_issues': len(self.data_quality_issues),
            'reconciliation_date': datetime.now().isoformat()
        }
        
        return ReconciliationReport(
            summary=summary,
            changes=changes,
            data_quality_issues=self.data_quality_issues
        )
    
    def export_csv(self, report: ReconciliationReport, output_path: Path) -> None:
        """Export reconciliation report to CSV."""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'sku', 'name', 'change_type', 'old_quantity', 
                'new_quantity', 'quantity_difference', 'old_location', 'new_location'
            ])
            
            for change in report.changes:
                writer.writerow([
                    change.sku,
                    change.name,
                    change.change_type,
                    change.old_quantity if change.old_quantity is not None else '',
                    change.new_quantity if change.new_quantity is not None else '',
                    change.quantity_difference if change.quantity_difference is not None else '',
                    change.old_location or '',
                    change.new_location or ''
                ])
    
    def export_json(self, report: ReconciliationReport, output_path: Path) -> None:
        """Export reconciliation report to JSON."""
        data = {
            'summary': report.summary,
            'changes': [asdict(c) for c in report.changes],
            'data_quality_issues': [asdict(i) for i in report.data_quality_issues]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def export_summary(self, report: ReconciliationReport, output_path: Path) -> None:
        """Export human-readable summary."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("INVENTORY RECONCILIATION SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Reconciliation Date: {report.summary['reconciliation_date']}\n\n")
            
            f.write("SNAPSHOT COMPARISON:\n")
            f.write(f"  Snapshot 1 Total Items: {report.summary['snapshot_1_total_items']}\n")
            f.write(f"  Snapshot 2 Total Items: {report.summary['snapshot_2_total_items']}\n\n")
            
            f.write("CHANGES DETECTED:\n")
            f.write(f"  Items Added:     {report.summary['items_added']}\n")
            f.write(f"  Items Removed:   {report.summary['items_removed']}\n")
            f.write(f"  Items Modified:  {report.summary['items_modified']}\n")
            f.write(f"  Items Unchanged: {report.summary['items_unchanged']}\n\n")
            
            f.write(f"DATA QUALITY ISSUES: {report.summary['data_quality_issues']}\n\n")
            
            if report.data_quality_issues:
                f.write("=" * 70 + "\n")
                f.write("DATA QUALITY ISSUES DETAIL\n")
                f.write("=" * 70 + "\n\n")
                
                # Group by severity
                high = [i for i in report.data_quality_issues if i.severity == 'high']
                medium = [i for i in report.data_quality_issues if i.severity == 'medium']
                low = [i for i in report.data_quality_issues if i.severity == 'low']
                
                if high:
                    f.write(f"HIGH SEVERITY ({len(high)}):\n")
                    for issue in high:
                        f.write(f"  - [{issue.issue_type}] {issue.description}\n")
                    f.write("\n")
                
                if medium:
                    f.write(f"MEDIUM SEVERITY ({len(medium)}):\n")
                    for issue in medium:
                        f.write(f"  - [{issue.issue_type}] {issue.description}\n")
                    f.write("\n")
                
                if low:
                    f.write(f"LOW SEVERITY ({len(low)}):\n")
                    for issue in low:
                        f.write(f"  - [{issue.issue_type}] {issue.description}\n")
                    f.write("\n")


def main():
    """Main entry point."""
    # Setup paths
    base_dir = Path(__file__).parent
    data_dir = base_dir / 'data'
    output_dir = base_dir / 'output'
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Initialize reconciler
    reconciler = InventoryReconciler()
    
    # Perform reconciliation
    print("\n" + "=" * 70)
    print("INVENTORY RECONCILIATION")
    print("=" * 70 + "\n")
    
    report = reconciler.reconcile(
        data_dir / 'snapshot_1.csv',
        data_dir / 'snapshot_2.csv'
    )
    
    # Export results
    print("\nExporting results...")
    reconciler.export_csv(report, output_dir / 'reconciliation_report.csv')
    print(f"  ✓ CSV report: {output_dir / 'reconciliation_report.csv'}")
    
    reconciler.export_json(report, output_dir / 'reconciliation_report.json')
    print(f"  ✓ JSON report: {output_dir / 'reconciliation_report.json'}")
    
    reconciler.export_summary(report, output_dir / 'summary.txt')
    print(f"  ✓ Summary: {output_dir / 'summary.txt'}")
    
    # Print summary to console
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Snapshot 1: {report.summary['snapshot_1_total_items']} items")
    print(f"  Snapshot 2: {report.summary['snapshot_2_total_items']} items")
    print(f"  Added:      {report.summary['items_added']} items")
    print(f"  Removed:    {report.summary['items_removed']} items")
    print(f"  Modified:   {report.summary['items_modified']} items")
    print(f"  Unchanged:  {report.summary['items_unchanged']} items")
    print(f"  Data Quality Issues: {report.summary['data_quality_issues']}")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()