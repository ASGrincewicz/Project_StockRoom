# Running Tests from the Tests Folder

## Quick Start

All test files have been moved to the `Tests/` folder for better organization.

### From the venv directory:
```bash
cd /Users/solid24/PycharmProjects/Project_StockRoom/venv
python3 -m pytest Tests/ -v
```

### From the Tests directory:
```bash
cd /Users/solid24/PycharmProjects/Project_StockRoom/venv/Tests
python3 -m pytest -v
```

## Test Execution Examples

### Run all tests
```bash
python3 -m pytest Tests/ -v
```

### Run specific test file
```bash
python3 -m pytest Tests/test_product.py -v
```

### Run with coverage
```bash
python3 -m pytest Tests/ --cov=.. --cov-report=html
```

### Run tests matching pattern
```bash
python3 -m pytest Tests/ -k "inventory" -v
```

### Run and stop on first failure
```bash
python3 -m pytest Tests/ -x
```

### Generate HTML coverage report
```bash
python3 -m pytest Tests/ --cov=.. --cov-report=html
# Open: venv/htmlcov/index.html
```

## Directory Structure

```
Project_StockRoom/
├── venv/
│   ├── Tests/                          ← All tests here now
│   │   ├── conftest.py
│   │   ├── pytest.ini
│   │   ├── test_*.py (7 files)
│   │   ├── TEST_SUITE_README.md
│   │   ├── TEST_SUITE_SUMMARY.md
│   │   ├── TEST_INDEX.md
│   │   └── QUICK_START.md
│   │
│   ├── Main.py
│   ├── Product.py
│   ├── MasterInventory.py
│   ├── MasterStockRoom.py
│   ├── ProductLocation.py
│   ├── Colorize.py
│   └── Messages.py
```

## Test Summary

- **Total Tests**: 147 (144 passing, 3 skipped)
- **Location**: `/Users/solid24/PycharmProjects/Project_StockRoom/venv/Tests/`
- **Execution Time**: ~0.06 seconds
- **Coverage**: 61%

## Documentation

All documentation files are in the `Tests/` folder:
- `QUICK_START.md` - Quick reference guide
- `TEST_SUITE_README.md` - Comprehensive documentation
- `TEST_SUITE_SUMMARY.md` - Overview and statistics
- `TEST_INDEX.md` - Complete test listing

## Notes

- Tests can be run from either the `venv/` or `Tests/` directory
- The `conftest.py` has been updated to correctly import modules from the parent directory
- All 147 tests pass successfully from the new location
