"""Core arena engine for benchmarking agent skills."""

import os
import re
import json
import time
import yaml
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class BenchmarkStatus(Enum):
    """Status of benchmark execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SkillRating(Enum):
    """Skill rating categories."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    LEGENDARY = "legendary"


@dataclass
class BenchmarkResult:
    """Result of a benchmark execution."""
    run_id: str
    skill_name: str
    skill_version: str
    task_description: str
    status: BenchmarkStatus
    execution_time: float
    tokens_used: int
    accuracy: float
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "run_id": self.run_id,
            "skill_name": self.skill_name,
            "skill_version": self.skill_version,
            "task_description": self.task_description,
            "status": self.status.value,
            "execution_time": self.execution_time,
            "tokens_used": self.tokens_used,
            "accuracy": self.accuracy,
            "error_message": self.error_message,
            "metadata": self.metadata,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BenchmarkResult':
        """Create from dictionary."""
        return cls(
            run_id=data["run_id"],
            skill_name=data["skill_name"],
            skill_version=data["skill_version"],
            task_description=data["task_description"],
            status=BenchmarkStatus(data["status"]),
            execution_time=float(data["execution_time"]),
            tokens_used=int(data["tokens_used"]),
            accuracy=float(data["accuracy"]),
            error_message=data.get("error_message"),
            metadata=data.get("metadata", {}),
            started_at=datetime.fromisoformat(data["started_at"]),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None
        )


@dataclass
class Skill:
    """Represents an agent skill."""
    skill_id: str
    name: str
    version: str
    description: str
    tagline: str
    what_it_does: str
    inspired_by: List[str]
    dependencies: List[str]
    content: str
    author: str
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    ratings: List[BenchmarkResult] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "tagline": self.tagline,
            "what_it_does": self.what_it_does,
            "inspired_by": self.inspired_by,
            "dependencies": self.dependencies,
            "content": self.content,
            "author": self.author,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "rating_count": len(self.ratings)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Skill':
        """Create from dictionary."""
        return cls(
            skill_id=data["skill_id"],
            name=data["name"],
            version=data["version"],
            description=data["description"],
            tagline=data.get("tagline", ""),
            what_it_does=data.get("what_it_does", ""),
            inspired_by=data.get("inspired_by", []),
            dependencies=data.get("dependencies", []),
            content=data["content"],
            author=data["author"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_updated=datetime.fromisoformat(data["last_updated"])
        )
    
    def add_rating(self, result: BenchmarkResult) -> None:
        """Add a benchmark result."""
        self.ratings.append(result)
        self.last_updated = datetime.now()
    
    def get_average_accuracy(self) -> float:
        """Calculate average accuracy."""
        if not self.ratings:
            return 0.0
        
        return sum(r.accuracy for r in self.ratings) / len(self.ratings)
    
    def get_average_execution_time(self) -> float:
        """Calculate average execution time."""
        if not self.ratings:
            return 0.0
        
        return sum(r.execution_time for r in self.ratings) / len(self.ratings)
    
    def get_skill_rating(self) -> SkillRating:
        """Determine skill rating based on performance."""
        avg_accuracy = self.get_average_accuracy()
        avg_time = self.get_average_execution_time()
        rating_count = len(self.ratings)
        
        if rating_count < 3:
            return SkillRating.BEGINNER
        elif avg_accuracy >= 0.9 and avg_time <= 2.0:
            return SkillRating.LEGENDARY
        elif avg_accuracy >= 0.85 and avg_time <= 3.0:
            return SkillRating.EXPERT
        elif avg_accuracy >= 0.75 and avg_time <= 5.0:
            return SkillRating.ADVANCED
        elif avg_accuracy >= 0.60:
            return SkillRating.INTERMEDIATE
        else:
            return SkillRating.BEGINNER


class BenchmarkEngine:
    """Engine for running benchmarks against skills."""
    
    def __init__(self, benchmarks_dir: str = None):
        """
        Initialize the benchmark engine.
        
        Args:
            benchmarks_dir: Directory containing benchmark tasks
        """
        self.benchmarks_dir = Path(benchmarks_dir) if benchmarks_dir else Path("./benchmarks")
        self._results: List[BenchmarkResult] = []
        self._skills: Dict[str, Skill] = {}
    
    def register_skill(self, skill: Skill) -> None:
        """
        Register a skill for benchmarking.
        
        Args:
            skill: Skill to register
        """
        self._skills[skill.skill_id] = skill
        print(f"✓ Registered skill: {skill.name} v{skill.version}")
    
    def load_skill_from_file(self, skill_path: str) -> Skill:
        """
        Load a skill from a file.
        
        Args:
            skill_path: Path to skill file
            
        Returns:
            Loaded Skill instance
        """
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter
            frontmatter_pattern = r'---\s*\n(.*?)\n---'
            match = re.search(frontmatter_pattern, content, re.DOTALL)
            
            if not match:
                raise ValueError("Invalid skill format: missing YAML frontmatter")
            
            frontmatter = yaml.safe_load(match.group(1))
            
            # Extract metadata
            skill_id = frontmatter.get("id", os.path.basename(skill_path).replace(".md", ""))
            name = frontmatter.get("name", "Unnamed Skill")
            version = frontmatter.get("version", "0.1.0")
            description = frontmatter.get("description", "")
            tagline = frontmatter.get("tagline", "")
            what_it_does = frontmatter.get("what_it_does", "")
            inspired_by = frontmatter.get("inspired_by", [])
            dependencies = frontmatter.get("dependencies", [])
            author = frontmatter.get("author", "unknown")
            
            skill = Skill(
                skill_id=skill_id,
                name=name,
                version=version,
                description=description,
                tagline=tagline,
                what_it_does=what_it_does,
                inspired_by=inspired_by,
                dependencies=dependencies,
                content=content,
                author=author
            )
            
            return skill
            
        except Exception as e:
            raise ValueError(f"Failed to load skill from {skill_path}: {str(e)}")
    
    def load_skill_from_string(self, skill_content: str, skill_id: str = "default") -> Skill:
        """
        Load a skill from a string.
        
        Args:
            skill_content: Skill markdown content
            skill_id: Skill identifier
            
        Returns:
            Loaded Skill instance
        """
        # Parse YAML frontmatter
        frontmatter_pattern = r'---\s*\n(.*?)\n---'
        match = re.search(frontmatter_pattern, skill_content, re.DOTALL)
        
        if not match:
            raise ValueError("Invalid skill format: missing YAML frontmatter")
        
        frontmatter = yaml.safe_load(match.group(1))
        
        skill = Skill(
            skill_id=skill_id,
            name=frontmatter.get("name", "Unnamed Skill"),
            version=frontmatter.get("version", "0.1.0"),
            description=frontmatter.get("description", ""),
            tagline=frontmatter.get("tagline", ""),
            what_it_does=frontmatter.get("what_it_does", ""),
            inspired_by=frontmatter.get("inspired_by", []),
            dependencies=frontmatter.get("dependencies", []),
            content=skill_content,
            author=frontmatter.get("author", "unknown")
        )
        
        return skill
    
    def run_benchmark(
        self,
        skill_id: str,
        benchmark_id: str,
        task: Dict[str, Any],
        timeout: float = 30.0
    ) -> BenchmarkResult:
        """
        Run a benchmark against a skill.
        
        Args:
            skill_id: ID of skill to test
            benchmark_id: ID of benchmark task
            task: Task details
            timeout: Maximum execution time in seconds
            
        Returns:
            BenchmarkResult
        """
        if skill_id not in self._skills:
            raise ValueError(f"Skill not found: {skill_id}")
        
        skill = self._skills[skill_id]
        
        # Simulate benchmark execution (in production, would execute actual skill)
        start_time = time.time()
        
        # Mock execution
        execution_time = 0.0
        tokens_used = 0
        accuracy = 0.0
        error_message = None
        
        try:
            # Simulate task execution
            task_complexity = task.get("complexity", "medium")
            
            if task_complexity == "easy":
                execution_time = 0.5
                tokens_used = 100
                accuracy = 0.95
            elif task_complexity == "medium":
                execution_time = 1.5
                tokens_used = 500
                accuracy = 0.85
            elif task_complexity == "hard":
                execution_time = 3.0
                tokens_used = 1500
                accuracy = 0.75
            else:
                execution_time = 2.0
                tokens_used = 800
                accuracy = 0.80
            
            # Simulate occasional errors
            import random
            if random.random() < 0.05:
                accuracy = 0.0
                error_message = "Execution failed"
                
        except Exception as e:
            error_message = str(e)
            accuracy = 0.0
            execution_time = time.time() - start_time
        
        completed_time = time.time() - start_time
        
        # Create result
        result = BenchmarkResult(
            run_id=f"run_{skill_id}_{benchmark_id}_{int(time.time())}",
            skill_name=skill.name,
            skill_version=skill.version,
            task_description=task.get("description", "Unknown task"),
            status=BenchmarkStatus.COMPLETED if not error_message else BenchmarkStatus.FAILED,
            execution_time=min(execution_time, timeout),
            tokens_used=tokens_used,
            accuracy=accuracy,
            error_message=error_message,
            started_at=datetime.now(),
            completed_at=datetime.now()
        )
        
        # Store result
        self._results.append(result)
        skill.add_rating(result)
        
        return result
    
    def get_leaderboard(
        self,
        limit: int = 10,
        skill_rating: Optional[SkillRating] = None,
        min_ratings: int = 3
    ) -> List[Skill]:
        """
        Get current leaderboard.
        
        Args:
            limit: Number of skills to return
            skill_rating: Filter by skill rating
            min_ratings: Minimum number of ratings required
            
        Returns:
            List of skills ranked by performance
        """
        filtered_skills = list(self._skills.values())
        
        # Filter by min ratings
        filtered_skills = [s for s in filtered_skills if len(s.ratings) >= min_ratings]
        
        # Filter by rating
        if skill_rating:
            filtered_skills = [s for s in filtered_skills if s.get_skill_rating() == skill_rating]
        
        # Sort by average accuracy (desc), then by rating count (desc), then by execution time (asc)
        filtered_skills.sort(
            key=lambda s: (
                s.get_average_accuracy(),
                len(s.ratings),
                -s.get_average_execution_time()
            ),
            reverse=True
        )
        
        return filtered_skills[:limit]
    
    def get_skill_stats(self, skill_id: str) -> Dict[str, Any]:
        """
        Get statistics for a skill.
        
        Args:
            skill_id: ID of skill
            
        Returns:
            Dictionary with skill statistics
        """
        if skill_id not in self._skills:
            raise ValueError(f"Skill not found: {skill_id}")
        
        skill = self._skills[skill_id]
        ratings = skill.ratings
        
        if not ratings:
            return {
                "skill_id": skill_id,
                "total_benchmarks": 0,
                "average_accuracy": 0.0,
                "average_execution_time": 0.0,
                "average_tokens_used": 0.0,
                "current_rating": None
            }
        
        return {
            "skill_id": skill_id,
            "total_benchmarks": len(ratings),
            "average_accuracy": skill.get_average_accuracy(),
            "average_execution_time": skill.get_average_execution_time(),
            "average_tokens_used": sum(r.tokens_used for r in ratings) / len(ratings),
            "current_rating": skill.get_skill_rating().value,
            "success_rate": sum(1 for r in ratings if r.status == BenchmarkStatus.COMPLETED) / len(ratings),
            "last_benchmark": max(r.completed_at for r in ratings).isoformat() if ratings else None
        }


class ArenaManager:
    """Manages the arena ecosystem."""
    
    def __init__(self):
        """Initialize arena manager."""
        self.engine = BenchmarkEngine()
        self._submissions: Dict[str, Skill] = {}
    
    def submit_skill(
        self,
        skill_path: str,
        author: str = "anonymous"
    ) -> Tuple[bool, str]:
        """
        Submit a new skill to the arena.
        
        Args:
            skill_path: Path to skill file
            author: Author name
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Load skill
            skill = self.engine.load_skill_from_file(skill_path)
            
            # Update author
            skill.author = author
            
            # Store submission
            self._submissions[skill.skill_id] = skill
            
            # Register with engine
            self.engine.register_skill(skill)
            
            return True, f"Skill submitted: {skill.name} v{skill.version}"
            
        except Exception as e:
            return False, f"Failed to submit skill: {str(e)}"
    
    def submit_from_string(
        self,
        skill_content: str,
        author: str = "anonymous"
    ) -> Tuple[bool, str]:
        """
        Submit a skill from a string.
        
        Args:
            skill_content: Skill markdown content
            author: Author name
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Extract skill_id from content or use default
            skill_id = "skill_" + str(int(time.time()))
            
            # Parse skill
            skill = self.engine.load_skill_from_string(skill_content, skill_id)
            skill.author = author
            
            # Store submission
            self._submissions[skill_id] = skill
            
            # Register with engine
            self.engine.register_skill(skill)
            
            return True, f"Skill submitted: {skill.name} v{skill.version}"
            
        except Exception as e:
            return False, f"Failed to submit skill: {str(e)}"
    
    def get_all_submissions(self) -> List[Dict[str, Any]]:
        """Get all submitted skills."""
        return [s.to_dict() for s in self._submissions.values()]
    
    def remove_submission(self, skill_id: str) -> bool:
        """
        Remove a submission.
        
        Args:
            skill_id: ID of skill to remove
            
        Returns:
            True if removed, False otherwise
        """
        if skill_id in self._submissions:
            del self._submissions[skill_id]
            return True
        return False
