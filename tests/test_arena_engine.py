"""Tests for the arena engine."""

import pytest
import sys
import os
from datetime import datetime
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from arena_md.arena_engine import (
    ArenaManager,
    BenchmarkEngine,
    Skill,
    BenchmarkResult,
    BenchmarkStatus,
    SkillRating
)


class TestBenchmarkResult:
    """Tests for BenchmarkResult."""
    
    def test_benchmark_result_to_dict(self):
        """Test converting result to dictionary."""
        result = BenchmarkResult(
            run_id="test_run",
            skill_name="TestSkill",
            skill_version="1.0.0",
            task_description="Test task",
            status=BenchmarkStatus.COMPLETED,
            execution_time=1.5,
            tokens_used=500,
            accuracy=0.85
        )
        
        data = result.to_dict()
        
        assert data["run_id"] == "test_run"
        assert data["skill_name"] == "TestSkill"
        assert data["status"] == "completed"
        assert data["accuracy"] == 0.85
    
    def test_benchmark_result_from_dict(self):
        """Test creating from dictionary."""
        data = {
            "run_id": "test_run",
            "skill_name": "TestSkill",
            "skill_version": "1.0.0",
            "task_description": "Test",
            "status": "completed",
            "execution_time": 1.5,
            "tokens_used": 500,
            "accuracy": 0.85,
            "started_at": datetime.now().isoformat()
        }
        
        result = BenchmarkResult.from_dict(data)
        
        assert result.run_id == "test_run"
        assert result.status == BenchmarkStatus.COMPLETED


class TestSkill:
    """Tests for Skill."""
    
    def test_skill_add_rating(self):
        """Test adding rating to skill."""
        skill = Skill(
            skill_id="test",
            name="Test",
            version="1.0.0",
            description="Test",
            tagline="Test",
            what_it_does="Test",
            inspired_by=[],
            dependencies=[],
            content="# Test",
            author="test"
        )
        
        result = BenchmarkResult(
            run_id="run_1",
            skill_name="Test",
            skill_version="1.0.0",
            task_description="Test",
            status=BenchmarkStatus.COMPLETED,
            execution_time=1.0,
            tokens_used=100,
            accuracy=0.9
        )
        
        skill.add_rating(result)
        
        assert len(skill.ratings) == 1
        assert skill.get_average_accuracy() == 0.9
    
    def test_skill_get_skill_rating(self):
        """Test skill rating determination."""
        skill = Skill(
            skill_id="test",
            name="Test",
            version="1.0.0",
            description="Test",
            tagline="Test",
            what_it_does="Test",
            inspired_by=[],
            dependencies=[],
            content="# Test",
            author="test"
        )
        
        # No ratings yet
        assert skill.get_skill_rating() == SkillRating.BEGINNER
        
        # Add some ratings
        for i in range(10):
            result = BenchmarkResult(
                run_id=f"run_{i}",
                skill_name="Test",
                skill_version="1.0.0",
                task_description="Test",
                status=BenchmarkStatus.COMPLETED,
                execution_time=0.5,
                tokens_used=100,
                accuracy=0.95
            )
            skill.add_rating(result)
        
        # Should be LEGENDARY now
        assert skill.get_skill_rating() == SkillRating.LEGENDARY


class TestBenchmarkEngine:
    """Tests for BenchmarkEngine."""
    
    def test_engine_initialization(self):
        """Test engine initialization."""
        engine = BenchmarkEngine()
        
        assert engine._skills == {}
        assert engine._results == []
    
    def test_register_skill(self):
        """Test skill registration."""
        engine = BenchmarkEngine()
        
        skill = Skill(
            skill_id="test",
            name="Test",
            version="1.0.0",
            description="Test",
            tagline="Test",
            what_it_does="Test",
            inspired_by=[],
            dependencies=[],
            content="# Test",
            author="test"
        )
        
        engine.register_skill(skill)
        
        assert "test" in engine._skills
        assert engine._skills["test"].name == "Test"
    
    def test_load_skill_from_file(self, tmp_path):
        """Test loading skill from file."""
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("""
---
id: test_skill
name: Test Skill
version: 1.0.0
description: Test description
author: test_author
---
# Test Skill Content
""")
            skill_path = f.name
        
        try:
            engine = BenchmarkEngine()
            skill = engine.load_skill_from_file(skill_path)
            
            assert skill.skill_id == "test_skill"
            assert skill.name == "Test Skill"
            assert skill.author == "test_author"
        finally:
            os.unlink(skill_path)
    
    def test_run_benchmark(self):
        """Test running a benchmark."""
        engine = BenchmarkEngine()
        
        skill = Skill(
            skill_id="test",
            name="Test",
            version="1.0.0",
            description="Test",
            tagline="Test",
            what_it_does="Test",
            inspired_by=[],
            dependencies=[],
            content="# Test",
            author="test"
        )
        
        engine.register_skill(skill)
        
        result = engine.run_benchmark(
            skill_id="test",
            benchmark_id="bench_1",
            task={"description": "Test task", "complexity": "easy"},
            timeout=10.0
        )
        
        assert result.run_id.startswith("run_test_bench_1_")
        assert result.skill_name == "Test"
        assert result.execution_time > 0
        assert result.accuracy >= 0.0
    
    def test_get_leaderboard(self):
        """Test getting leaderboard."""
        engine = BenchmarkEngine()
        
        # Add skills with different performance
        for i in range(3):
            skill = Skill(
                skill_id=f"skill_{i}",
                name=f"Skill {i}",
                version="1.0.0",
                description="Test",
                tagline="Test",
                what_it_does="Test",
                inspired_by=[],
                dependencies=[],
                content="# Test",
                author="test",
                ratings=[
                    BenchmarkResult(
                        run_id=f"run_{i}_{j}",
                        skill_name=f"Skill {i}",
                        skill_version="1.0.0",
                        task_description="Test",
                        status=BenchmarkStatus.COMPLETED,
                        execution_time=1.0 + (i * 0.1),
                        tokens_used=500 + (i * 50),
                        accuracy=0.85 + (i * 0.05)
                    )
                    for j in range(5)
                ]
            )
            engine.register_skill(skill)
        
        leaderboard = engine.get_leaderboard(limit=10)
        
        assert len(leaderboard) == 3
        assert leaderboard[0].skill_id == "skill_2"  # Best performer


class TestArenaManager:
    """Tests for ArenaManager."""
    
    def test_submit_skill(self):
        """Test skill submission."""
        manager = ArenaManager()
        
        success, message = manager.submit_from_string(
            """
---
id: test
name: Test Skill
version: 1.0.0
description: Test
---
# Test
""",
            author="test_user"
        )
        
        assert success is True
        assert "submitted" in message.lower()
    
    def test_get_all_submissions(self):
        """Test getting all submissions."""
        manager = ArenaManager()
        
        # Submit multiple skills
        for i in range(3):
            manager.submit_from_string(
                f"""
---
id: skill_{i}
name: Skill {i}
version: 1.0.0
description: Test {i}
---
# Skill {i}
""",
                author=f"user_{i}"
            )
        
        submissions = manager.get_all_submissions()
        
        assert len(submissions) == 3
        assert all("skill_id" in s for s in submissions)


class TestIntegration:
    """Integration tests."""
    
    def test_full_benchmark_workflow(self):
        """Test complete benchmark workflow."""
        manager = ArenaManager()
        
        # Submit skill
        success, _ = manager.submit_from_string("""
---
id: test_skill
name: Test Skill
version: 1.0.0
description: Test skill for benchmarking
---
# Test Skill
""")
        
        assert success
        
        # Run benchmarks
        engine = manager.engine
        
        result1 = engine.run_benchmark(
            skill_id="test_skill",
            benchmark_id="bench_1",
            task={"description": "Test task 1", "complexity": "easy"},
            timeout=30.0
        )
        
        result2 = engine.run_benchmark(
            skill_id="test_skill",
            benchmark_id="bench_2",
            task={"description": "Test task 2", "complexity": "medium"},
            timeout=30.0
        )
        
        assert result1.status == BenchmarkStatus.COMPLETED
        assert result2.status == BenchmarkStatus.COMPLETED
        
        # Get stats
        stats = engine.get_skill_stats("test_skill")
        
        assert stats["total_benchmarks"] == 2
        assert stats["current_rating"] is not None
        
        # Get leaderboard
        leaderboard = engine.get_leaderboard(limit=10, min_ratings=2)
        
        assert len(leaderboard) >= 1
