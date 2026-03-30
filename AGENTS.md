# AGENTS.md - Arena MD Project Context

This folder is home. Treat it that way.

## Project: Arena.md (#2)

### Identity
- **Name**: Arena.md
- **License**: Apache-2.0
- **Org**: avasis-ai
- **PyPI**: arena-md
- **Version**: 0.1.0
- **Tagline**: The crowdsourced gladiator arena for benchmarking agent skills

### What It Does
This platform evolves the static SKILL.md into an active, competitive benchmarking ecosystem. Developers submit custom markdown skills, which an orchestration engine runs blindly against standardized tasks. The system ranks skills based on execution time, token efficiency, and accuracy.

### Inspired By
- LMSYS Chatbot Arena
- LlamaIndex
- Aider
- Competitive leaderboard mechanics

### Core Components

#### `/benchmarks/`
- Benchmark task library
- Standardized test cases
- Complexity levels

#### `/arena-engine/`
- Core benchmarking engine
- Performance tracking
- Rating system

#### `/api/`
- FastAPI REST endpoints
- Leaderboard management
- Skill submission

### Technical Architecture

**Key Dependencies:**
- `fastapi>=0.100` - Web framework (Trust score: 9.9)
- `uvicorn>=0.23` - ASGI server
- `sqlalchemy>=2.0` - Database ORM (Trust score: 9.7)
- `rich>=13.0` - Terminal UI (Trust score: 9.4)

**Core Modules:**
1. `arena_engine.py` - Core benchmarking logic
2. `cli.py` - Command-line interface
3. `server.py` - FastAPI REST API

### AI Coding Agent Guidelines

#### When Contributing:

1. **Understand the vision**: This is about gamifying benchmarking and creating a trusted standard
2. **Use Context7**: Check trust scores for new libraries before adding dependencies
3. **Blind execution**: Benchmarks must run without knowledge of the skill being tested
4. **Fair metrics**: Track execution time, tokens, and accuracy consistently
5. **Rating system**: Skills should automatically progress through levels

#### What to Remember:

- **Blind benchmarking**: No skill knowledge during execution
- **Performance metrics**: Track time, tokens, accuracy consistently
- **Rating progression**: BEGINNER → INTERMEDIATE → ADVANCED → EXPERT → LEGENDARY
- **Data flywheel**: Collect millions of execution traces
- **Standardized tasks**: Ensure fair comparison across all skills

#### Common Patterns:

**Submit a skill:**
```python
from arena_md.arena_engine import ArenaManager

manager = ArenaManager()
success, message = manager.submit_skill("my_skill.md", author="your_name")
```

**Run a benchmark:**
```python
result = engine.run_benchmark(
    skill_id="my_skill",
    benchmark_id="task_1",
    task={"description": "Task", "complexity": "medium"}
)
```

**View leaderboard:**
```python
leaderboard = engine.get_leaderboard(limit=10)
for skill in leaderboard:
    print(f"{skill.name}: {skill.get_average_accuracy():.1%}")
```

### Project Status

- ✅ Initial implementation complete
- ✅ Core benchmark engine
- ✅ Skill registration and management
- ✅ Performance tracking
- ✅ Automatic rating system
- ✅ FastAPI REST API
- ✅ CLI interface
- ✅ Comprehensive test suite
- ⚠️ Real skill execution pending
- ⚠️ Large-scale benchmarking pending

### How to Work with This Project

1. **Read `SOUL.md`** - Understand who you are
2. **Read `USER.md`** - Know who you're helping
3. **Check `memory/YYYY-MM-DD.md`** - Recent context
4. **Read `MEMORY.md`** - Long-term decisions (main session only)
5. **Execute**: Code → Test → Commit

### Red Lines

- **No stubs or TODOs**: Every function must have real implementation
- **Type hints required**: All function signatures must include types
- **Docstrings mandatory**: Explain what, why, and how
- **Test coverage**: New features need tests
- **Blind execution**: Benchmarks must not leak skill information

### Development Workflow

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Format code
black src/ tests/
isort src/ tests/

# Check syntax
python -m py_compile src/arena_md/*.py

# Run server
uvicorn arena_md.server:app --reload

# Commit
git add -A && git commit -m "feat: add rating system"
```

### Key Files to Understand

- `src/arena_md/arena_engine.py` - Core benchmarking logic
- `src/arena_md/cli.py` - Command-line interface
- `src/arena_md/server.py` - FastAPI REST API
- `tests/test_arena_engine.py` - Comprehensive tests

### Security Considerations

- **Blind execution**: Skills run in isolated context
- **No secrets**: Never expose API keys or tokens
- **Rate limiting**: Prevent API abuse
- **Trusted dependencies**: All verified via Context7
- **Apache 2.0**: Open source, community-driven

### Next Steps

1. Implement real skill execution engine
2. Add more benchmark tasks
3. Build knowledge base of skill patterns
4. Add real-time leaderboard updates
5. Create web dashboard
6. Add skill comparison tools

### Unique Defensible Moat

The **proprietary dataset of millions of skill execution traces, edge-cases, and failure modes** forms an unassailable data flywheel for training future meta-agents and routing algorithms. This data is:

- Collected from real submissions
- Annotated with performance metrics
- Indexed by complexity and task type
- Continuously expanding through usage
- Valuable for training better agents

The more people use Arena MD, the better the platform becomes at:

- Evaluating new skills
- Detecting patterns
- Identifying best practices
- Predicting performance

---

**This file should evolve as you learn more about the project.**
