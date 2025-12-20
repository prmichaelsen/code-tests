"""
Test suite for inventory reconciliation script.
"""

import pytest
import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

# Add parent directory to path to import reconcile module
sys.path.insert(0, str(Path(__file__).parent.parent))

from reconcile import (
    InventoryItem,
    InventoryReconciler,
    InventoryChange,
    DataQualityIssue,
    ReconciliationReport
)


class TestInventoryItem:
    """Test InventoryItem dataclass."""
    
    def test_normalize_sku_with_hyphen(self):
        """Test SKU normalization when hyphen is present."""
        item = InventoryItem('SKU-001', 'Test', 100, 'Warehouse A', '2024-01-01')
        assert item.normalize_sku() == 'SKU-001'
    
    def test_normalize_sku_without_hyphen(self):
        """Test SKU normalization when hyphen is missing."""
        item = InventoryItem('SKU001', 'Test', 100, 'Warehouse A', '2024-01-01')
        assert item.normalize_sku() == 'SKU-001'
    
    def test_normalize_sku_lowercase(self):
        """Test SKU normalization with lowercase."""
        item = InventoryItem('sku-001', 'Test', 100, 'Warehouse A', '2024-01-01')
        assert item.normalize_sku() == 'SKU-001'
    
    def test_normalize_sku_with_whitespace(self):
        """Test SKU normalization with whitespace."""
        item = InventoryItem(' SKU-001 ', 'Test', 100, 'Warehouse A', '2024-01-01')
        assert item.normalize_sku() == 'SKU-001'


class TestInventoryReconciler:
    """Test InventoryReconciler class."""
    
    @pytest.fixture
    def reconciler(self):
        """Create a fresh reconciler instance."""
        return InventoryReconciler()
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        with TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def create_csv_file(self, path: Path, headers: list, rows: list):
        """Helper to create CSV files for testing."""
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
    
    def test_load_snapshot_basic(self, reconciler, temp_dir):
        """Test loading a basic snapshot file."""
        csv_path = temp_dir / 'test.csv'
        self.create_csv_file(
            csv_path,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-01'],
                ['SKU-002', 'Widget B', '200', 'Warehouse B', '2024-01-01']
            ]
        )
        
        items = reconciler.load_snapshot(csv_path, 1)
        
        assert len(items) == 2
        assert 'SKU-001' in items
        assert 'SKU-002' in items
        assert items['SKU-001'].quantity == 100
        assert items['SKU-002'].name == 'Widget B'
    
    def test_load_snapshot_alternate_columns(self, reconciler, temp_dir):
        """Test loading snapshot with alternate column names."""
        csv_path = temp_dir / 'test.csv'
        self.create_csv_file(
            csv_path,
            ['sku', 'product_name', 'qty', 'warehouse', 'updated_at'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-01']
            ]
        )
        
        items = reconciler.load_snapshot(csv_path, 1)
        
        assert len(items) == 1
        assert items['SKU-001'].name == 'Widget A'
        assert items['SKU-001'].quantity == 100
    
    def test_detect_negative_quantity(self, reconciler, temp_dir):
        """Test detection of negative quantities."""
        csv_path = temp_dir / 'test.csv'
        self.create_csv_file(
            csv_path,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '-5', 'Warehouse A', '2024-01-01']
            ]
        )
        
        items = reconciler.load_snapshot(csv_path, 1)
        
        issues = [i for i in reconciler.data_quality_issues 
                 if i.issue_type == 'negative_quantity']
        assert len(issues) == 1
        assert issues[0].sku == 'SKU-001'
        assert issues[0].severity == 'high'
    
    def test_detect_duplicate_sku(self, reconciler, temp_dir):
        """Test detection of duplicate SKUs."""
        csv_path = temp_dir / 'test.csv'
        self.create_csv_file(
            csv_path,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-01'],
                ['SKU-001', 'Widget A Duplicate', '50', 'Warehouse B', '2024-01-01']
            ]
        )
        
        items = reconciler.load_snapshot(csv_path, 1)
        
        issues = [i for i in reconciler.data_quality_issues 
                 if i.issue_type == 'duplicate_sku']
        assert len(issues) == 1
        assert issues[0].sku == 'SKU-001'
    
    def test_detect_sku_format_inconsistency(self, reconciler, temp_dir):
        """Test detection of SKU format inconsistencies."""
        csv_path = temp_dir / 'test.csv'
        self.create_csv_file(
            csv_path,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU001', 'Widget A', '100', 'Warehouse A', '2024-01-01'],
                ['sku-002', 'Widget B', '200', 'Warehouse B', '2024-01-01']
            ]
        )
        
        items = reconciler.load_snapshot(csv_path, 1)
        
        issues = [i for i in reconciler.data_quality_issues 
                 if i.issue_type == 'sku_format_inconsistency']
        assert len(issues) == 2
    
    def test_detect_whitespace_in_name(self, reconciler, temp_dir):
        """Test detection of whitespace issues in names."""
        csv_path = temp_dir / 'test.csv'
        self.create_csv_file(
            csv_path,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', ' Widget A ', '100', 'Warehouse A', '2024-01-01']
            ]
        )
        
        items = reconciler.load_snapshot(csv_path, 1)
        
        issues = [i for i in reconciler.data_quality_issues 
                 if i.issue_type == 'whitespace_in_name']
        assert len(issues) == 1
    
    def test_reconcile_items_added(self, reconciler, temp_dir):
        """Test detection of newly added items."""
        snap1 = temp_dir / 'snap1.csv'
        snap2 = temp_dir / 'snap2.csv'
        
        self.create_csv_file(
            snap1,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-01']
            ]
        )
        
        self.create_csv_file(
            snap2,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-08'],
                ['SKU-002', 'Widget B', '200', 'Warehouse B', '2024-01-08']
            ]
        )
        
        report = reconciler.reconcile(snap1, snap2)
        
        added = [c for c in report.changes if c.change_type == 'added']
        assert len(added) == 1
        assert added[0].sku == 'SKU-002'
        assert added[0].new_quantity == 200
        assert report.summary['items_added'] == 1
    
    def test_reconcile_items_removed(self, reconciler, temp_dir):
        """Test detection of removed items."""
        snap1 = temp_dir / 'snap1.csv'
        snap2 = temp_dir / 'snap2.csv'
        
        self.create_csv_file(
            snap1,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-01'],
                ['SKU-002', 'Widget B', '200', 'Warehouse B', '2024-01-01']
            ]
        )
        
        self.create_csv_file(
            snap2,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-08']
            ]
        )
        
        report = reconciler.reconcile(snap1, snap2)
        
        removed = [c for c in report.changes if c.change_type == 'removed']
        assert len(removed) == 1
        assert removed[0].sku == 'SKU-002'
        assert removed[0].old_quantity == 200
        assert report.summary['items_removed'] == 1
    
    def test_reconcile_items_modified(self, reconciler, temp_dir):
        """Test detection of quantity changes."""
        snap1 = temp_dir / 'snap1.csv'
        snap2 = temp_dir / 'snap2.csv'
        
        self.create_csv_file(
            snap1,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-01']
            ]
        )
        
        self.create_csv_file(
            snap2,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '85', 'Warehouse A', '2024-01-08']
            ]
        )
        
        report = reconciler.reconcile(snap1, snap2)
        
        modified = [c for c in report.changes if c.change_type == 'modified']
        assert len(modified) == 1
        assert modified[0].sku == 'SKU-001'
        assert modified[0].old_quantity == 100
        assert modified[0].new_quantity == 85
        assert modified[0].quantity_difference == -15
        assert report.summary['items_modified'] == 1
    
    def test_reconcile_items_unchanged(self, reconciler, temp_dir):
        """Test detection of unchanged items."""
        snap1 = temp_dir / 'snap1.csv'
        snap2 = temp_dir / 'snap2.csv'
        
        self.create_csv_file(
            snap1,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-01']
            ]
        )
        
        self.create_csv_file(
            snap2,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-08']
            ]
        )
        
        report = reconciler.reconcile(snap1, snap2)
        
        unchanged = [c for c in report.changes if c.change_type == 'unchanged']
        assert len(unchanged) == 1
        assert unchanged[0].sku == 'SKU-001'
        assert unchanged[0].quantity_difference == 0
        assert report.summary['items_unchanged'] == 1
    
    def test_detect_unusual_quantity_change(self, reconciler, temp_dir):
        """Test detection of unusual quantity changes (>1000%)."""
        snap1 = temp_dir / 'snap1.csv'
        snap2 = temp_dir / 'snap2.csv'
        
        self.create_csv_file(
            snap1,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '10', 'Warehouse A', '2024-01-01']
            ]
        )
        
        self.create_csv_file(
            snap2,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '1000', 'Warehouse A', '2024-01-08']
            ]
        )
        
        report = reconciler.reconcile(snap1, snap2)
        
        issues = [i for i in report.data_quality_issues 
                 if i.issue_type == 'unusual_quantity_change']
        assert len(issues) == 1
        assert issues[0].sku == 'SKU-001'
    
    def test_export_csv(self, reconciler, temp_dir):
        """Test CSV export functionality."""
        snap1 = temp_dir / 'snap1.csv'
        snap2 = temp_dir / 'snap2.csv'
        output = temp_dir / 'output.csv'
        
        self.create_csv_file(
            snap1,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-01']
            ]
        )
        
        self.create_csv_file(
            snap2,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '85', 'Warehouse A', '2024-01-08']
            ]
        )
        
        report = reconciler.reconcile(snap1, snap2)
        reconciler.export_csv(report, output)
        
        assert output.exists()
        
        with open(output, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 1
            assert rows[0]['sku'] == 'SKU-001'
            assert rows[0]['change_type'] == 'modified'
    
    def test_export_json(self, reconciler, temp_dir):
        """Test JSON export functionality."""
        snap1 = temp_dir / 'snap1.csv'
        snap2 = temp_dir / 'snap2.csv'
        output = temp_dir / 'output.json'
        
        self.create_csv_file(
            snap1,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-01']
            ]
        )
        
        self.create_csv_file(
            snap2,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '85', 'Warehouse A', '2024-01-08']
            ]
        )
        
        report = reconciler.reconcile(snap1, snap2)
        reconciler.export_json(report, output)
        
        assert output.exists()
        
        with open(output, 'r') as f:
            data = json.load(f)
            assert 'summary' in data
            assert 'changes' in data
            assert 'data_quality_issues' in data
            assert data['summary']['items_modified'] == 1
    
    def test_export_summary(self, reconciler, temp_dir):
        """Test summary text export functionality."""
        snap1 = temp_dir / 'snap1.csv'
        snap2 = temp_dir / 'snap2.csv'
        output = temp_dir / 'summary.txt'
        
        self.create_csv_file(
            snap1,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100', 'Warehouse A', '2024-01-01']
            ]
        )
        
        self.create_csv_file(
            snap2,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '85', 'Warehouse A', '2024-01-08']
            ]
        )
        
        report = reconciler.reconcile(snap1, snap2)
        reconciler.export_summary(report, output)
        
        assert output.exists()
        
        with open(output, 'r') as f:
            content = f.read()
            assert 'INVENTORY RECONCILIATION SUMMARY' in content
            assert 'Items Modified:  1' in content
    
    def test_empty_snapshots(self, reconciler, temp_dir):
        """Test handling of empty snapshots."""
        snap1 = temp_dir / 'snap1.csv'
        snap2 = temp_dir / 'snap2.csv'
        
        self.create_csv_file(
            snap1,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            []
        )
        
        self.create_csv_file(
            snap2,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            []
        )
        
        report = reconciler.reconcile(snap1, snap2)
        
        assert report.summary['snapshot_1_total_items'] == 0
        assert report.summary['snapshot_2_total_items'] == 0
        assert len(report.changes) == 0
    
    def test_decimal_quantities(self, reconciler, temp_dir):
        """Test handling of decimal quantities."""
        csv_path = temp_dir / 'test.csv'
        self.create_csv_file(
            csv_path,
            ['sku', 'name', 'quantity', 'location', 'last_counted'],
            [
                ['SKU-001', 'Widget A', '100.5', 'Warehouse A', '2024-01-01'],
                ['SKU-002', 'Widget B', '200.00', 'Warehouse B', '2024-01-01']
            ]
        )
        
        items = reconciler.load_snapshot(csv_path, 1)
        
        assert items['SKU-001'].quantity == 100.5
        assert items['SKU-002'].quantity == 200.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])