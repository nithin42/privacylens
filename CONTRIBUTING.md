# Contributing to privacylens

Thank you for your interest in contributing! 🎉

## Getting Started

```bash
git clone https://github.com/nithin42/privacylens.git
cd privacylens
pip install -e ".[dev]"
```

## Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Run linting: `python -m flake8 src/ tests/`
6. Submit a Pull Request to `dev`

## Code Style

- Max line length: 100 characters
- Formatter: `black` (`black src/ tests/`)
- Linter: `flake8`
- All public functions must have docstrings

## Reporting Issues

Use [GitHub Issues](https://github.com/nithin42/privacylens/issues) with the appropriate template.

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.
