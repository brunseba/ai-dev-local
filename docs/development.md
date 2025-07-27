# Development Guide

This guide provides information for contributing to and developing AI Dev Local.

## Development Environment Setup

### Prerequisites

- **Python 3.10+** with uv package manager
- **Docker & Docker Compose** for containerized services
- **Git** for version control
- **pipx** for isolated Python package installation
- **pre-commit** for code quality hooks

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/brunseba/ai-dev-local.git
   cd ai-dev-local
   ```

2. **Install in development mode:**
   ```bash
   # Using uv (recommended)
   uv pip install -e .
   
   # Or using pip
   pip install -e .
   ```

3. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

4. **Initialize development configuration:**
   ```bash
   ai-dev-local config init
   ```

## Project Structure

The project follows Python best practices with the root folder for code in `src/`:

```
ai-dev-local/
├── src/                    # Main source code
├── docs/                   # Documentation (MkDocs)
├── tests/                  # Unit tests
├── configs/                # Configuration templates
├── docker/                 # Docker configurations
├── scripts/                # Utility scripts
├── mkdocs.yml             # Documentation configuration
├── pyproject.toml         # Python project configuration
└── README.md              # Project overview
```

## Development Workflow

### Git Workflow

The project uses conventional commits and follows these practices:

1. **Use conventional commit format:**
   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve bug in service"
   git commit -m "docs: update documentation"
   ```

2. **Pre-commit hooks automatically run:**
   - Code formatting and linting
   - Type checking
   - Documentation validation

3. **Create tags for releases:**
   ```bash
   git tag -a v0.x.x -m "Release version 0.x.x"
   ```

### Running Tests

Unit tests are created by default using pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_specific.py
```

### Documentation

Documentation is managed with MkDocs and Material theme:

```bash
# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### Code Quality

The project uses several tools for code quality:

- **Linting:** flake8, pylint
- **Formatting:** black, isort
- **Type checking:** mypy
- **Security:** bandit

Pre-commit hooks ensure all checks pass before commits.

## Packaging and Distribution

### Package Management

- **Package engine:** uv
- **CLI management:** Click
- **Deployment:** pipx

### Building and Publishing

```bash
# Build package
python -m build

# Publish to PyPI (for maintainers)
python -m twine upload dist/*
```

## Contributing Guidelines

### Issue Management

- **GitHub labels** map to conventional commit standards
- **Issues** are assigned to @me by default
- **GitHub Pages** is enabled for documentation

### Pull Request Process

1. Create a feature branch
2. Make changes following coding standards
3. Add/update tests as needed
4. Update documentation
5. Ensure all checks pass
6. Submit pull request

### GitHub Actions

The project includes workflows for:

- **MkDocs publishing** to GitHub Pages
- **Continuous integration** testing
- **Automated releases** and packaging

## Security Considerations

- Never commit sensitive data like API keys
- Use environment variables for configuration
- Follow security best practices for Docker containers
- Keep dependencies up to date

## Support and Community

- **GitHub Issues:** [Report bugs or request features](https://github.com/brunseba/ai-dev-local/issues)
- **GitHub Discussions:** [Community support](https://github.com/brunseba/ai-dev-local/discussions)
- **Documentation:** [Latest docs](https://brunseba.github.io/ai-dev-local/)

For questions or contributions, please refer to the project's GitHub repository.
