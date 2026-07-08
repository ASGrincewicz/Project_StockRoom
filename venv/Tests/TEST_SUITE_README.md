# Project Stockroom - Test Suite Documentation

## Overview

This is a comprehensive test suite for the Project Stockroom application, an inventory management system for managing products, categories, and stockroom locations.

## Test Structure

The test suite is organized into the following test files:

### Unit Tests

1. **test_product.py** - Tests for the `Product` class
   - Product initialization and normalization
   - Data validation and error handling
   - Product information display

2. **test_colorize.py** - Tests for the `Colorize` module
   - Color application to text
   - Handling of None/invalid inputs
   - All color functions (blue, green, red, yellow, orange, cyan, magenta, gray, white, salmon)

3. **test_messages.py** - Tests for the `Messages` module
   - Message helper functions
   - Input validation and retry logic
   - Confirmation dialogs

4. **test_master_stockroom.py** - Tests for the `MasterStockRoom` module
   - Location parsing and creation
   - Next location computation
   - CSV read/write operations
   - Location index building

5. **test_master_inventory.py** - Tests for the `MasterInventory` module
   - Product number verification
   - Category management
   - Product search and sorting
   - CSV import/export
   - Product selection workflows

6. **test_product_location.py** - Tests for the `ProductLocation` module
   - Location file reading/writing
   - Product backstock tracking
   - Location validation

### Integration Tests

**test_integration.py** - End-to-end workflow tests
   - Complete inventory workflows
   - Location management workflows
   - Product management workflows
   - Error handling and recovery

### Test Configuration

**conftest.py** - Pytest fixtures and configuration
   - Temporary directory setup
   - Sample CSV file generation
   - Clean test environment initialization

## Running the Tests

### Run All Tests
```bash
cd /Users/solid24/PycharmProjects/Project_StockRoom/venv
python3 -m pytest -v
```

### Run Specific Test File
```bash
python3 -m pytest test_product.py -v
```

### Run Specific Test Class
```bash
python3 -m pytest test_product.py::TestProduct -v
```

### Run Specific Test
```bash
python3 -m pytest test_product.py::TestProduct::test_product_initialization_basic -v
```

### Run with Coverage Report
```bash
python3 -m pytest --cov=. --cov-report=html -v
```

### Run Tests Matching a Pattern
```bash
python3 -m pytest -k "inventory" -v
```

### Run Only Unit Tests (exclude integration tests)
```bash
python3 -m pytest test_product.py test_colorize.py test_messages.py test_master_stockroom.py test_master_inventory.py test_product_location.py -v
```

## Test Coverage

The test suite provides comprehensive coverage of:

- **Product Class**: 20 test cases
  - Initialization with various input types
  - Data normalization and validation
  - Edge cases (None, empty strings, invalid numbers)

- **Colorize Module**: 18 test cases
  - All color functions
  - None and empty input handling
  - Special characters handling

- **Messages Module**: 32 test cases
  - All message generators
  - All input functions with validation
  - Retry logic for invalid inputs

- **MasterStockRoom Module**: 22 test cases
  - Location parsing and validation
  - Next location computation logic
  - CSV operations
  - User input handling

- **MasterInventory Module**: 26 test cases
  - Product verification and sorting
  - Category management
  - CSV import/export
  - Product search and selection

- **ProductLocation Module**: 16 test cases
  - Location file operations
  - Data validation
  - Malformed data handling

- **Integration Tests**: 9 test cases
  - Full workflow scenarios
  - Multi-module interactions
  - Error handling and recovery

**Total: 143 test cases**

## Test Fixtures

The `conftest.py` file provides reusable fixtures:

- `temp_dir` - Creates and cleans up temporary directory
- `sample_master_inventory_csv` - Creates sample inventory CSV
- `sample_stockroom_csv` - Creates sample stockroom CSV
- `sample_location_file` - Creates sample location file
- `clean_environment` - Sets up clean test environment with all directories

## Key Testing Strategies

### 1. Input Validation
Tests verify that all user inputs are properly validated and normalized:
- String trimming and case conversion
- Numeric input parsing with zero-padding
- Range validation

### 2. Error Handling
Tests ensure graceful handling of:
- Missing files
- Corrupted CSV data
- Invalid user inputs
- Edge cases (empty, None, negative values)

### 3. Data Integrity
Tests verify:
- CSV read/write correctness
- Data sorting and organization
- Category/product relationships
- Location indexing

### 4. State Management
Tests check:
- Proper state updates across modules
- Category persistence
- Inventory consistency

## Coverage Summary

Run the coverage report:
```bash
python3 -m pytest --cov=. --cov-report=term-missing -v
```

This will show:
- Lines covered by tests
- Lines missed by tests
- Overall coverage percentage

## Dependencies

- pytest >= 7.0
- pytest-cov >= 4.0

Install with:
```bash
python3 -m pip install pytest pytest-cov
```

## Known Limitations

Some tests are marked as skipped:
- `test_backstock_product_basic` - Requires complex interactive mocking
- `test_remove_product_basic` - Requires complex interactive mocking
- `test_audit_product` - Requires complex interactive mocking

These tests are better suited for manual testing or integration testing frameworks that support terminal I/O.

## Adding New Tests

When adding new functionality:

1. Create test file following naming convention: `test_<module_name>.py`
2. Use existing fixtures for setup/teardown
3. Follow test naming convention: `test_<function_name>_<scenario>`
4. Document test purpose in docstring
5. Run full suite to ensure no regressions:
   ```bash
   python3 -m pytest -v
   ```

## Best Practices

1. **Keep tests focused** - Each test should test one behavior
2. **Use descriptive names** - Test name should explain what's being tested
3. **Use fixtures** - Reuse setup code via fixtures
4. **Mock external I/O** - Use monkeypatch for input/file operations
5. **Test edge cases** - Include None, empty, invalid inputs
6. **Test error paths** - Verify error handling works correctly
7. **Document complex tests** - Add comments explaining test logic

## Continuous Integration

To run tests in CI/CD:

```bash
#!/bin/bash
cd /Users/solid24/PycharmProjects/Project_StockRoom/venv
python3 -m pytest -v --tb=short --junit-xml=test-results.xml
```

## Troubleshooting

### Issue: Tests fail with import errors
**Solution**: Ensure all Python files are in the same directory as `conftest.py`

### Issue: Fixture scope errors
**Solution**: Verify `conftest.py` is in the same directory as test files

### Issue: Tests not finding test files
**Solution**: Run pytest from the venv directory

### Issue: File permission errors
**Solution**: Ensure temp_dir fixture is properly cleaning up with `shutil.rmtree()`

## Further Improvements

Future enhancements to the test suite:
- Add performance benchmarks
- Add memory usage tests
- Add concurrent access tests
- Add database transaction tests (if database is added)
- Add API endpoint tests (if REST API is added)
- Add UI/UX tests using Selenium or similar

## Support

For questions about the test suite, refer to the pytest documentation:
https://docs.pytest.org/
