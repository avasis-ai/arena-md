# Arena.md (#2)

## Tagline
The crowdsourced gladiator arena for benchmarking agent skills.

## What It Does
This platform evolves the static SKILL.md into an active, competitive benchmarking ecosystem. Developers submit custom markdown skills, which an orchestration engine runs blindly against standardized tasks. The system ranks skills based on execution time, token efficiency, and accuracy.

## Inspired By
LMSYS Chatbot Arena, LlamaIndex, Aider + Competitive leaderboard mechanics

## Viral Potential
Gamifies the otherwise tedious process of prompt engineering. Developers actively share their high ranks on social platforms, creating a viral loop. Becomes the definitive, trusted standard for evaluating open-source agent tools.

## Unique Defensible Moat
The project accumulates a proprietary dataset of millions of skill execution traces, edge-cases, and failure modes, forming an unassailable data flywheel for training future meta-agents and routing algorithms.

## Repo Starter Structure
/benchmarks, /arena-engine, Apache 2.0, live leaderboard UI

## Metadata
- **License**: Apache-2.0
- **Org**: avasis-ai
- **PyPI**: arena-md
- **Dependencies**: fastapi>=0.100, uvicorn>=0.23, sqlalchemy>=2.0, rich>=13.0
