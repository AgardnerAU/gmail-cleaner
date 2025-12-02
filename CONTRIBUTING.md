# Contributing to Gmail Cleaner

Thanks for your interest in contributing! 🎉

## Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gmail-cleaner.git
   cd gmail-cleaner
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites
- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Your own Google Cloud OAuth credentials

### Running Locally

```bash
# Install dependencies
uv sync

# Run the app
uv run python main.py
```

The app will be available at http://localhost:8766

### Docker Development

```bash
docker compose up --build
```

## Code Style

- **Python**: Follow PEP 8, use type hints where possible

## Making Changes

### For New Features
1. Open a feature request issue to discuss the idea or feel free to open an pr
2. Keep PRs focused and small

## Pull Request Process

1. Update documentation if needed
2. Please Test your changes locally
3. Please Test Docker build if you modified Dockerfile or dependencies
4. A maintainer will be automatically requested for review via CODEOWNERS on all pull requests


## Questions?

Feel free to open an issue or start a discussion!

---

Thank you for contributing! ❤️
