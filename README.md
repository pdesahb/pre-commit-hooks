# pre-commit-hooks

A collection of custom pre-commit hooks for various development workflows.

## Installation

### Using pre-commit

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pdesahb/pre-commit-hooks
    rev: v1.0.0  # Use the ref you want to point at
    hooks:
      - id: trailing-whitespace
      # Add more hooks as needed
```

## Available Hooks

### `check-commit-size`

Checks that commits don't exceed size limits based on the number of additions and deletions.

**Usage:**
```yaml
- id: check-commit-size
  args: [--max-additions, '1000', --max-deletions, '500']
```

**Arguments:**
- `--max-additions`: Maximum number of additions allowed (optional)
- `--max-deletions`: Maximum number of deletions allowed (optional)

**What it does:**
- Analyzes the staged changes using `git diff --cached --numstat`
- Counts total additions and deletions across all files
- Blocks the commit if either limit is exceeded
- If no limits are specified, the hook always passes
- Handles binary files gracefully (skips them in the count)
- Provides clear error messages when limits are exceeded

**Examples:**
```yaml
# Check only additions (max 1000 lines)
- id: check-commit-size
  args: [--max-additions, '1000']

# Check only deletions (max 500 lines)
- id: check-commit-size
  args: [--max-deletions, '500']

# Check both additions and deletions
- id: check-commit-size
  args: [--max-additions, '1000', --max-deletions, '500']
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/pdesahb/pre-commit-hooks.git
cd pre-commit-hooks
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pre_commit_hooks

# Run linting
tox -e lint

# Run tests for all Python versions
tox
```

### Adding New Hooks

1. Create a new Python file in the `pre_commit_hooks/` directory
2. Implement your hook function following the pattern:
   ```python
   def your_hook_name(filenames: List[str]) -> int:
       # Your hook logic here
       # Return 0 for success, 1 for failure
       pass
   ```
3. Add a `main` function:
   ```python
   if __name__ == '__main__':
       exit(main(description='Your hook description', hook=your_hook_name))
   ```
4. Add the entry point to `setup.py` and `setup.cfg`
5. Write tests in `tests/test_your_hook.py`
6. Update this README with documentation

### Code Style

This project uses:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **Pre-commit** for automated checks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
