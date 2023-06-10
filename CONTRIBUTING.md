# Contributing to Smart Expense Analyzer

Thank you for your interest in contributing to the Smart Expense Analyzer Dashboard!

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, SQLite works by default)

### Development Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/smart-expense-analyzer.git
cd smart-expense-analyzer
```

2. Set up the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend
```bash
cd frontend
npm install
```

## Running the Application

### Backend
```bash
cd backend
python main.py
```

### Frontend
```bash
cd frontend
npm run dev
```

## Code Style

- **Python**: Follow PEP 8 guidelines
- **TypeScript/React**: Use ESLint and Prettier configurations
- **Commits**: Use clear, descriptive commit messages

## Testing

### Backend Tests
```bash
cd backend
python test_backend.py
```

### Frontend Testing
```bash
cd frontend
npm run test
```

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test thoroughly
4. Commit with clear messages
5. Push to your fork
6. Create a Pull Request with a detailed description

## Reporting Issues

Please use GitHub Issues to report bugs or suggest features. Include:
- Clear description of the issue
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Screenshots if applicable

## License

This project is licensed under the MIT License - see LICENSE file for details.
