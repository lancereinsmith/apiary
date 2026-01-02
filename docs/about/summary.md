# Documentation Overview

Comprehensive documentation for the Apiary framework.

## Documentation Structure

### Getting Started
Learn the basics and get Apiary running:

- **[Installation](../getting-started/installation.md)** - Install and configure Apiary
- **[Quick Start](../getting-started/quickstart.md)** - Build your first endpoint in minutes
- **[Configuration](../getting-started/configuration.md)** - Configure settings and endpoints

### User Guide
Master Apiary's features:

- **[Overview](../guide/overview.md)** - Architecture and concepts
- **[Adding Endpoints](../guide/adding-endpoints.md)** - Code-based and config-based endpoints
- **[Creating Services](../guide/creating-services.md)** - Build business logic services
- **[Authentication](../guide/authentication.md)** - Implement API key auth
- **[Built-in Endpoints](../guide/builtin-endpoints.md)** - Health, metrics, and discovery
- **[Configurable Endpoints](../guide/configurable-endpoints.md)** - Dynamic endpoint system

### Development
Contribute to Apiary:

- **[Development Setup](../development/setup.md)** - Set up dev environment
- **[CLI Reference](../development/cli.md)** - Command-line tools
- **[Testing](../development/testing.md)** - Write and run tests
- **[Code Quality](../development/code-quality.md)** - Maintain standards
- **[Project Structure](../development/structure.md)** - Understand the codebase

### Deployment
Deploy Apiary to production:

- **[Overview](../deployment/overview.md)** - Deployment strategies
- **[Server Setup](../deployment/server-setup.md)** - Configure servers
- **[Configuration](../deployment/configuration.md)** - Production settings
- **[Monitoring](../deployment/monitoring.md)** - Monitor your API

### Reference
API and configuration reference:

- **[Core Modules](../reference/core.md)** - Core framework APIs
- **[Services](../reference/services.md)** - Service base classes
- **[Models](../reference/models.md)** - Request/response models
- **[Configuration Options](../reference/config.md)** - All config options

### About
Project information:

- **[Changelog](changelog.md)** - Version history
- **[Contributing](contributing.md)** - Contribution guidelines
- **[License](license.md)** - MIT License

## Key Features Covered

### Configuration-Driven Endpoints
Add endpoints via JSON configuration without code changes. Perfect for rapid prototyping and non-technical configuration.

### Service-Based Architecture
Build reusable services that can be called by multiple endpoints. Clean separation of business logic.

### Production Features
- Rate limiting with different tiers
- Metrics collection for monitoring
- Health checks (liveness/readiness)
- Structured logging with correlation IDs
- Request validation and size limits
- Response caching

### Security
- API key authentication
- CORS configuration
- Security headers
- Input validation

## Quick Links

- [Installation Guide](../getting-started/installation.md)
- [Quick Start Tutorial](../getting-started/quickstart.md)
- [Contributing Guidelines](contributing.md)
- [API Reference](../reference/core.md)

## Documentation Features

- **Search**: Use the search bar to find topics quickly
- **Code Examples**: All guides include practical examples
- **Dark Mode**: Toggle theme in the header
- **Navigation**: Left sidebar for sections, right sidebar for page contents

## Contributing to Docs

Documentation improvements welcome! Edit Markdown files in the `docs/` directory and submit a PR.

See [Contributing Guide](contributing.md) for details.

## Feedback

Found an issue or have a suggestion?

- [GitHub Issues](https://github.com/lancereinsmith/apiary/issues)
- [GitHub Discussions](https://github.com/lancereinsmith/apiary/discussions)

---

*Documentation built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)*
