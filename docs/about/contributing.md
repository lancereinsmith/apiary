# Contributing to Apiary

Thank you for your interest in contributing to Apiary!

## Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following our code style
4. Run tests: `pytest`
5. Format code: `ruff format .`
6. Lint code: `ruff check .`
7. Type check: `ty check .`
8. Commit and push your changes
9. Open a Pull Request

## Development Setup

```bash
git clone https://github.com/lancereinsmith/apiary.git
cd apiary
uv sync
uv run apiary init
uv run apiary serve --reload
```

## Code Style

- Use type hints for all function parameters and return values
- Write docstrings for modules and functions
- Keep functions focused and single-purpose
- Maximum line length: 88 characters
- Follow existing code patterns

## Testing

Write tests for all new features:

```python
import pytest
from fastapi.testclient import TestClient


def test_endpoint_success(client: TestClient):
    """Test that the endpoint returns success for valid input."""
    response = client.get("/api/endpoint")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

Run tests with:

```bash
pytest              # All tests
pytest --cov        # With coverage
pytest tests/unit/  # Unit tests only
```

## Pull Request Checklist

Before submitting:

- [ ] Tests pass locally
- [ ] Code is formatted with `ruff format .`
- [ ] No linting errors from `ruff check .`
- [ ] Type checking passes with `ty check .`
- [ ] Documentation updated (if needed)
- [ ] Commit messages are descriptive

## Reporting Issues

When reporting bugs, include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment (Python version, OS, Apiary version)
- Relevant logs or error messages

## Feature Requests

When requesting features, include:

- Clear description of the feature
- Use case and motivation
- Proposed implementation approach (if applicable)
- Any alternative solutions considered

## Code of Conduct

- Be respectful
- Give constructive feedback

## Questions?

- Check the [documentation](https://lancereinsmith.github.io/apiary/)
- Search existing [issues](https://github.com/lancereinsmith/apiary/issues)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to Apiary!
