# Contributing to Logseq to Obsidian Migration Tool

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Logseq to Obsidian migration tool.

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- Git
- A Logseq graph for testing

### Setting Up Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/logseq-to-obsidian-migration.git
   cd logseq-to-obsidian-migration
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv logseq_env
   source logseq_env/bin/activate  # On Windows: logseq_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the installation**
   ```bash
   python3 logseq_to_obsidian.py --help
   ```

## 🐛 Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to avoid duplicates
2. **Test with the latest version** of the script
3. **Provide detailed information**:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Sample files (if applicable)

### Issue Templates

Use the provided issue templates:
- 🐛 **Bug Report**: For reporting bugs
- ✨ **Feature Request**: For suggesting new features
- 📚 **Documentation**: For documentation improvements

## 🔧 Making Changes

### Code Style

- Follow Python PEP 8 style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small

### Testing

Before submitting changes:

1. **Test with sample data**
   ```bash
   python3 logseq_to_obsidian.py --src examples/sample_logseq --out test_output --dry-run
   ```

2. **Test all command-line options**
   ```bash
   python3 logseq_to_obsidian.py --src examples/sample_logseq --out test_output --frontmatter --status-tags --strip-properties --rename-journals --dry-run
   ```

3. **Verify error handling** with malformed files

### Commit Messages

Use clear, descriptive commit messages:

```
Add support for custom date formats

- Parse additional date formats in frontmatter
- Update documentation with new formats
- Add test cases for edge cases
```

## 📝 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, well-documented code
   - Add tests if applicable
   - Update documentation

3. **Test thoroughly**
   - Run the script with various options
   - Test with different Logseq graph structures
   - Verify error handling

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Use the PR template
   - Describe what changes you made
   - Link any related issues
   - Request review from maintainers

## 🎯 Areas for Contribution

### High Priority
- **Bug fixes**: Fix reported issues
- **Error handling**: Improve robustness
- **Documentation**: Improve README and examples
- **Testing**: Add automated tests

### Medium Priority
- **Performance**: Optimize for large graphs
- **Features**: New conversion options
- **CLI**: Better command-line interface
- **Logging**: Add verbose output options

### Low Priority
- **GUI**: Optional graphical interface
- **Plugins**: Obsidian plugin integration
- **Batch processing**: Multiple graph support

## 📋 Development Guidelines

### File Structure
```
logseq-to-obsidian-migration/
├── logseq_to_obsidian.py    # Main script
├── README.md                # Documentation
├── CONTRIBUTING.md          # This file
├── LICENSE                  # MIT License
├── requirements.txt         # Dependencies
├── .gitignore              # Git ignore rules
├── examples/               # Sample files
└── tests/                  # Test files (future)
```

### Code Organization
- Keep the main script focused on core functionality
- Use helper functions for complex operations
- Maintain backward compatibility when possible
- Document all public functions

## 🤝 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the golden rule

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For private concerns

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors list

Thank you for contributing to this project! 🎉
