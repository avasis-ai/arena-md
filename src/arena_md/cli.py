"""CLI for Arena MD."""

import click
import sys
import os
from pathlib import Path

from .arena_engine import ArenaManager, BenchmarkEngine, SkillRating, BenchmarkStatus


@click.group()
@click.version_option(version="0.1.0", prog_name="arena-md")
def main():
    """Arena MD - Crowdsourced benchmarking platform for agent skills."""
    pass


@main.command()
@click.argument('skill_path', type=click.Path(exists=True))
@click.option('--author', '-a', default='anonymous',
              help='Author name')
def submit(skill_path: str, author: str) -> None:
    """Submit a skill to the arena."""
    try:
        manager = ArenaManager()
        
        success, message = manager.submit_skill(skill_path, author)
        
        if success:
            click.echo(f"✅ {message}")
        else:
            click.echo(f"❌ {message}", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
def leaderboard(limit: int = 10, rating: str = None) -> None:
    """Show current leaderboard."""
    try:
        engine = BenchmarkEngine()
        
        # Load existing submissions (in production, from database)
        submissions = engine.get_all_submissions()
        
        click.echo("\n🏆 Arena Leaderboard")
        click.echo("=" * 60)
        
        # For demo, create some sample data
        from arena_md.arena_engine import Skill, BenchmarkResult, datetime
        
        # Sample skills for demonstration
        sample_skills = [
            Skill(
                skill_id="sample_1",
                name="Advanced Agent",
                version="1.0.0",
                description="High performance agent",
                tagline="Elite capabilities",
                what_it_does="Performs complex tasks",
                inspired_by=["LMSYS", "Benchmark"],
                dependencies=["fastapi", "click"],
                content="# Advanced Agent",
                author="expert_user",
                ratings=[
                    BenchmarkResult(
                        run_id=f"run_{i}",
                        skill_name="Advanced Agent",
                        skill_version="1.0.0",
                        task_description="Complex task",
                        status=BenchmarkStatus.COMPLETED,
                        execution_time=1.0 + (i * 0.1),
                        tokens_used=500 + (i * 50),
                        accuracy=0.90 + (i * 0.01),
                        started_at=datetime.now()
                    )
                    for i in range(10)
                ]
            ),
            Skill(
                skill_id="sample_2",
                name="Basic Agent",
                version="0.9.0",
                description="Basic capabilities",
                tagline="Entry level",
                what_it_does="Handles simple tasks",
                inspired_by=["Simple"],
                dependencies=["click"],
                content="# Basic Agent",
                author="beginner_user",
                ratings=[
                    BenchmarkResult(
                        run_id=f"run_{i}",
                        skill_name="Basic Agent",
                        skill_version="0.9.0",
                        task_description="Simple task",
                        status=BenchmarkStatus.COMPLETED,
                        execution_time=2.0 + (i * 0.2),
                        tokens_used=300 + (i * 30),
                        accuracy=0.75 + (i * 0.02),
                        started_at=datetime.now()
                    )
                    for i in range(8)
                ]
            )
        ]
        
        # Register sample skills
        for skill in sample_skills:
            engine.register_skill(skill)
        
        # Get leaderboard
        filtered_rating = SkillRating(rating) if rating else None
        
        leaderboard = engine.get_leaderboard(
            limit=limit,
            skill_rating=filtered_rating,
            min_ratings=3
        )
        
        # Display leaderboard
        for i, skill in enumerate(leaderboard, 1):
            avg_time = skill.get_average_execution_time()
            avg_accuracy = skill.get_average_accuracy()
            rating_count = len(skill.ratings)
            skill_rating = skill.get_skill_rating()
            
            rank_emoji = {
                1: "🥇",
                2: "🥈",
                3: "🥉"
            }.get(i, f"#{i:2d}")
            
            rating_emoji = {
                SkillRating.LEGENDARY: "⭐",
                SkillRating.EXPERT: "🏆",
                SkillRating.ADVANCED: "🔥",
                SkillRating.INTERMEDIATE: "📚",
                SkillRating.BEGINNER: "🌱"
            }.get(skill_rating, "📊")
            
            click.echo(f"\n{rank_emoji} {rating_emoji} {i}. {skill.name} v{skill.version}")
            click.echo(f"   Author: {skill.author}")
            click.echo(f"   Rating: {skill_rating.value.upper()}")
            click.echo(f"   Accuracy: {avg_accuracy:.1%}")
            click.echo(f"   Avg Time: {avg_time:.2f}s")
            click.echo(f"   Benchmarks: {rating_count}")
        
        click.echo("\n" + "=" * 60)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('skill_id')
def stats(skill_id: str) -> None:
    """Show statistics for a skill."""
    try:
        engine = BenchmarkEngine()
        
        # Load sample skills
        from arena_md.arena_engine import Skill, BenchmarkResult, datetime
        
        sample_skills = [
            Skill(
                skill_id=skill_id,
                name="Sample Skill",
                version="1.0.0",
                description="Sample",
                tagline="Test",
                what_it_does="Test",
                inspired_by=["test"],
                dependencies=[],
                content="# Sample",
                author="test",
                ratings=[
                    BenchmarkResult(
                        run_id=f"run_{i}",
                        skill_name="Sample Skill",
                        skill_version="1.0.0",
                        task_description="Task",
                        status=BenchmarkStatus.COMPLETED,
                        execution_time=1.0 + (i * 0.1),
                        tokens_used=500 + (i * 50),
                        accuracy=0.85 + (i * 0.01),
                        started_at=datetime.now()
                    )
                    for i in range(5)
                ]
            )
        ]
        
        for skill in sample_skills:
            engine.register_skill(skill)
        
        stats = engine.get_skill_stats(skill_id)
        
        click.echo(f"\n📊 Skill Statistics: {skill_id}")
        click.echo("=" * 60)
        
        click.echo(f"Total Benchmarks: {stats['total_benchmarks']}")
        click.echo(f"Average Accuracy: {stats['average_accuracy']:.1%}")
        click.echo(f"Avg Execution Time: {stats['average_execution_time']:.2f}s")
        click.echo(f"Avg Tokens Used: {stats['average_tokens_used']:.0f}")
        click.echo(f"Current Rating: {stats['current_rating']}")
        click.echo(f"Success Rate: {stats['success_rate']:.1%}")
        
        if stats['last_benchmark']:
            click.echo(f"Last Benchmark: {stats['last_benchmark']}")
        
        click.echo("=" * 60)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
