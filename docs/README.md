# MatrixCalc Documentation

Welcome to the MatrixCalc documentation! This guide will help you get started with using, developing, and deploying MatrixCalc.

---

## 📚 Documentation Structure

### For Users

- [Getting Started](./user/getting-started.md) - Quick start guide
- [Features](./user/features.md) - Complete feature documentation
- [API Reference](./user/api-reference.md) - REST API documentation

### For Developers

- [Architecture](./developer/architecture.md) - System architecture overview
- [Development Setup](./developer/development.md) - Local development guide
- [Testing Guide](./developer/testing.md) - How to run and write tests
- [Contributing](./developer/contributing.md) - Contribution guidelines

### Deployment

- [Deployment Guide](./deployment/README.md) - Complete deployment guide
  - Google Cloud Run (recommended)
  - Docker Compose
  - Traditional server
- [Docker Guide](./deployment/docker.md) - Docker-specific documentation
- [Troubleshooting](./deployment/troubleshooting.md) - Common deployment issues

### Migration

- [v1.0 to v2.0 Migration](./migration/v1-to-v2.md) - Tkinter to Web migration guide

### Archive

- [v2.0 Documentation](./archive/v2.0/) - Historical v2.0 documents
- [v3.0 Planning](./archive/v3.0/) - v3.0 feature planning and roadmap

---

## 🚀 Quick Links

### Getting Started

1. **Installation**: See [Deployment Guide](./deployment/README.md)
2. **First Steps**: See [Getting Started](./user/getting-started.md)
3. **API Usage**: See [API Reference](./user/api-reference.md)

### Development

1. **Setup**: See [Development Setup](./developer/development.md)
2. **Architecture**: See [Architecture](./developer/architecture.md)
3. **Testing**: See [Testing Guide](./developer/testing.md)

### Deployment

1. **Cloud Run**: See [Deployment Guide - Cloud Run](./deployment/README.md#google-cloud-run-recommended)
2. **Docker**: See [Deployment Guide - Docker Compose](./deployment/README.md#docker-compose)
3. **Troubleshooting**: See [Troubleshooting Guide](./deployment/troubleshooting.md)

---

## 📖 What is MatrixCalc?

MatrixCalc is a professional matrix calculator with:

- **Web Interface**: Modern Vue.js 3 frontend with TypeScript
- **REST API**: Django backend with comprehensive API
- **Matrix Operations**: Sum, subtract, multiply, inverse, determinant, transpose
- **Data Management**: CRUD operations, backup/restore, history
- **Statistics**: Interactive dashboard with Chart.js
- **Modern UX**: Dark mode, animations, keyboard shortcuts, LaTeX export

---

## 🎯 Key Features

### Matrix Operations

- ✅ Basic operations (sum, subtract, multiply)
- ✅ Advanced operations (inverse, determinant, transpose)
- ✅ Matrix templates (identity, zeros, random, etc.)
- ✅ Validation and error handling

### User Experience

- ✅ Dark mode (light/dark/auto)
- ✅ Toast notifications
- ✅ Keyboard shortcuts
- ✅ LaTeX export (6 formats)
- ✅ Responsive design

### Developer Experience

- ✅ TypeScript throughout
- ✅ Comprehensive API
- ✅ Docker support
- ✅ CI/CD ready
- ✅ Well-documented

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Vue.js 3 SPA  │  ← Frontend (TypeScript + Tailwind)
└────────┬────────┘
         │ HTTP/HTTPS
┌────────┴────────┐
│  Django 4.2 API │  ← Backend (Python + DRF)
└────────┬────────┘
         │ ORM
┌────────┴────────┐
│   PostgreSQL    │  ← Database
└─────────────────┘
```

See [Architecture Documentation](./developer/architecture.md) for details.

---

## 🛠️ Tech Stack

### Backend

- **Django 4.2** - Web framework
- **Django REST Framework** - API toolkit
- **PostgreSQL 15** - Database
- **NumPy** - Matrix calculations
- **Gunicorn** - WSGI server

### Frontend

- **Vue.js 3.5** - JavaScript framework
- **TypeScript 5.7** - Type safety
- **Pinia** - State management
- **Vue Router** - Routing
- **Tailwind CSS 4** - Styling
- **Chart.js** - Visualizations

### DevOps

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Web server
- **Cloud Run** - Serverless deployment

---

## 📝 Version History

### v3.0 (In Development)

- LaTeX export with 6 formats
- Enhanced keyboard shortcuts
- Animation system
- Command palette
- Improved heatmap visualization

### v2.0 (Current)

- Complete web migration from Tkinter
- REST API with Django
- Modern Vue.js frontend
- Dark mode
- Statistics dashboard
- Docker support

### v1.0 (Legacy)

- Desktop GUI with Tkinter
- Basic matrix operations
- Available in tag `v1.0-tkinter-desktop`

---

## 🤝 Contributing

We welcome contributions! Please see:

- [Contributing Guide](./developer/contributing.md)
- [Development Setup](./developer/development.md)
- [Code of Conduct](../CONTRIBUTING.md)

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](../LICENSE) for details.

---

## 🆘 Need Help?

- **Documentation Issues**: Create an issue on GitHub
- **Deployment Problems**: See [Troubleshooting Guide](./deployment/troubleshooting.md)
- **Feature Requests**: Open a GitHub issue
- **Bug Reports**: Open a GitHub issue with reproduction steps

---

## 📚 Additional Resources

- [Main README](../README.md) - Project overview
- [API Documentation](./user/api-reference.md) - REST API reference
- [Deployment Guide](./deployment/README.md) - Production deployment
- [Testing Guide](./developer/testing.md) - Running tests

---

**Last updated:** January 19, 2026  
**MatrixCalc v3.0** - Professional Matrix Calculator
