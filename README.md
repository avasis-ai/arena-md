# README.md - Arena MD

## The Crowdsourced Gladiator Arena for Benchmarking Agent Skills

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/arena-md.svg)](https://pypi.org/project/arena-md/)

**Arena MD** is the revolutionary platform that evolves SKILL.md into an active, competitive benchmarking ecosystem. Developers submit custom markdown skills, which are run against standardized tasks. The system ranks skills based on execution time, token efficiency, and accuracy.

## 🎯 What It Does

- **Skill Benchmarking**: Run SKILL.md files against standardized tasks
- **Performance Metrics**: Track execution time, token usage, and accuracy
- **Competitive Leaderboards**: See which skills perform best
- **Automatic Rating**: Skills are rated from Beginner to Legendary
- **Fair Comparison**: Blind execution ensures unbiased benchmarking

### Example Use Case

```python
from arena_md.arena_engine import ArenaManager, BenchmarkEngine

# Submit your skill
manager = ArenaManager()
manager.submit_skill("my_skill.md", author="your_name")

# Run benchmarks
engine = manager.engine
result = engine.run_benchmark(
    skill_id="my_skill",
    benchmark_id="task_1",
    task={"description": "Test task", "complexity": "medium"}
)

# View leaderboard
leaderboard = engine.get_leaderboard(limit=10)
```

## 🚀 Features

- **Comprehensive Benchmarking**: Execute skills against multiple tasks
- **Performance Tracking**: Monitor execution time, tokens, and accuracy
- **Dynamic Rating System**: Skills automatically progress through ratings
- **Leaderboard API**: RESTful API for leaderboard access
- **CLI Tools**: Command-line interface for benchmarking
- **FastAPI Backend**: Modern web API for integration

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- FastAPI, uvicorn, SQLAlchemy, Rich

### Install from PyPI

```bash
pip install arena-md
```

### Install from Source

```bash
git clone https://github.com/avasis-ai/arena-md.git
cd arena-md
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
pip install pytest pytest-mock black isort
```

## 🔧 Usage

### Command-Line Interface

```bash
# Check version
arena-md --version

# Submit a skill
arena-md submit my_skill.md --author "Your Name"

# View leaderboard
arena-md leaderboard --limit 10

# View skill statistics
arena-md stats skill_id_here
```

### Programmatic Usage

```python
from arena_md.arena_engine import ArenaManager, BenchmarkEngine

# Initialize arena
manager = ArenaManager()

# Submit skill
success, message = manager.submit_skill("my_skill.md")

# Run benchmark
engine = manager.engine
result = engine.run_benchmark(
    skill_id="my_skill",
    benchmark_id="task_1",
    task={"description": "Task", "complexity": "medium"}
)

# View leaderboard
leaderboard = engine.get_leaderboard(limit=10)

# Get stats
stats = engine.get_skill_stats("my_skill")
```

### FastAPI Server

Start the web server:

```bash
uvicorn arena_md.server:app --host 0.0.0.0 --port 8000
```

API Endpoints:

- `GET /` - API information
- `POST /api/skills` - Submit a skill
- `GET /api/skills` - List all skills
- `GET /api/leaderboard` - View leaderboard
- `GET /api/skills/{skill_id}/stats` - Get skill statistics
- `POST /api/benchmarks/run` - Run a benchmark
- `DELETE /api/skills/{skill_id}` - Remove a skill

## 📚 API Reference

### BenchmarkEngine

Core engine for benchmarking.

#### `run_benchmark(skill_id, benchmark_id, task, timeout)` → BenchmarkResult

Run a benchmark against a skill.

**Parameters:**
- `skill_id`: ID of skill to test
- `benchmark_id`: ID of benchmark task
- `task`: Task details
- `timeout`: Maximum execution time

#### `get_leaderboard(limit, skill_rating, min_ratings)` → List[Skill]

Get current leaderboard.

### ArenaManager

Manages the arena ecosystem.

#### `submit_skill(skill_path, author)` → Tuple[bool, str]

Submit a skill.

#### `get_all_submissions()` → List[Dict]

Get all submitted skills.

### Skill Rating System

Skills are automatically rated based on performance:

- **🌱 Beginner**: New skills with few ratings
- **📚 Intermediate**: Skills with decent performance
- **🔥 Advanced**: High accuracy and fast execution
- **🏆 Expert**: Excellent across all metrics
- **⭐ Legendary**: Near-perfect performance

## 🧪 Testing

Run tests with pytest:

```bash
python -m pytest tests/ -v
```

## 📁 Project Structure

```
arena-md/
├── README.md
├── pyproject.toml
├── LICENSE
├── src/
│   └── arena_md/
│       ├── __init__.py
│       ├── arena_engine.py
│       ├── cli.py
│       └── server.py
├── tests/
│   └── test_arena_engine.py
├── benchmarks/
└── .github/
    └── ISSUE_TEMPLATE/
        └── bug_report.md
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `python -m pytest tests/ -v`
5. **Submit a pull request**

### Development Setup

```bash
git clone https://github.com/avasis-ai/arena-md.git
cd arena-md
pip install -e ".[dev]"
pre-commit install
```

## 📝 License

This project is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) for details.

## 🎯 Vision

Arena MD transforms the otherwise tedious process of prompt engineering into a gamified, competitive experience. By creating a trusted standard for evaluating open-source agent tools, we establish a reliable benchmark for the entire field.

### Key Innovations

- **Blind Benchmarking**: No knowledge of the skill during execution
- **Fair Comparison**: Standardized tasks and metrics
- **Data Flywheel**: Millions of execution traces for continuous improvement
- **Community Driven**: Crowdsourced skill submissions

## 🌟 Impact

This tool enables:

- **Rapid skill evaluation**: Benchmark skills in minutes
- **Performance insights**: Understand strengths and weaknesses
- **Community learning**: Learn from top performers
- **Continuous improvement**: Data-driven skill evolution
- **Standardized testing**: Reliable comparison across tools

## 🛡️ Security & Trust

- **Blind execution**: No skill knowledge during benchmarking
- **Trusted dependencies**: FastAPI (9.9), uvicorn (0.23+), SQLAlchemy (9.7), rich (9.4) - [Context7 verified](https://context7.com)
- **Apache 2.0**: Open source, community-driven
- **No external calls**: All processing local

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/avasis-ai/arena-md/wiki)
- **Issues**: [GitHub Issues](https://github.com/avasis-ai/arena-md/issues)
- **Community**: [Developer Discord](https://discord.gg/arena-md)

## 🙏 Acknowledgments

- **LMSYS Chatbot Arena**: Inspiration for competitive benchmarking
- **LlamaIndex**: Data handling patterns
- **Aider**: Competitive mechanics
- **Developer community**: Shared knowledge and best practices

---

**Made with ❤️ by [Avasis AI](https://avasis.ai)**

*Gamify your prompt engineering. Compete, learn, and evolve.*
