"""FastAPI server for Arena MD."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import json

from .arena_engine import (
    ArenaManager,
    BenchmarkEngine,
    Skill,
    BenchmarkResult,
    BenchmarkStatus,
    SkillRating
)


# FastAPI app
app = FastAPI(
    title="Arena MD",
    description="Crowdsourced benchmarking platform for agent skills",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize arena manager
arena_manager = ArenaManager()


class SkillSubmit(BaseModel):
    """Model for skill submission."""
    content: str
    author: Optional[str] = "anonymous"


class SkillUpdate(BaseModel):
    """Model for skill updates."""
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None


class BenchmarkTask(BaseModel):
    """Model for benchmark task."""
    description: str
    complexity: str = "medium"
    parameters: Optional[Dict[str, Any]] = None


class LeaderboardResponse(BaseModel):
    """Response model for leaderboard."""
    rank: int
    skill_id: str
    name: str
    version: str
    author: str
    rating: str
    accuracy: float
    execution_time: float
    benchmark_count: int


class SkillStatsResponse(BaseModel):
    """Response model for skill statistics."""
    skill_id: str
    total_benchmarks: int
    average_accuracy: float
    average_execution_time: float
    average_tokens_used: float
    current_rating: Optional[str]
    success_rate: float
    last_benchmark: Optional[str]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Arena MD",
        "version": "0.1.0",
        "description": "Crowdsourced benchmarking platform for agent skills",
        "endpoints": {
            "submit": "POST /api/skills",
            "leaderboard": "GET /api/leaderboard",
            "stats": "GET /api/skills/{skill_id}/stats",
            "benchmark": "POST /api/benchmarks/run"
        }
    }


@app.post("/api/skills")
async def submit_skill(skill: SkillSubmit):
    """
    Submit a new skill to the arena.
    
    Args:
        skill: Skill data including content and author
        
    Returns:
        Submission result
    """
    try:
        success, message = arena_manager.submit_from_string(skill.content, skill.author)
        
        if success:
            return {"success": True, "message": message}
        else:
            raise HTTPException(status_code=400, detail=message)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/skills")
async def list_skills(
    limit: int = 10,
    offset: int = 0,
    min_ratings: int = 0
):
    """
    List all submitted skills.
    
    Args:
        limit: Maximum number of skills to return
        offset: Number of skills to skip
        min_ratings: Minimum number of ratings required
        
    Returns:
        List of skills
    """
    try:
        skills = arena_manager.get_all_submissions()
        
        # Filter by min ratings
        skills = [s for s in skills if s.get("rating_count", 0) >= min_ratings]
        
        # Paginate
        paginated_skills = skills[offset:offset + limit]
        
        return {
            "total": len(skills),
            "limit": limit,
            "offset": offset,
            "skills": paginated_skills
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/leaderboard")
async def get_leaderboard(
    limit: int = 10,
    rating: Optional[str] = None,
    min_ratings: int = 3
):
    """
    Get current leaderboard.
    
    Args:
        limit: Number of skills to return
        rating: Filter by skill rating
        min_ratings: Minimum number of ratings required
        
    Returns:
        Leaderboard data
    """
    try:
        engine = arena_manager.engine
        
        # Get leaderboard
        leaderboard = engine.get_leaderboard(
            limit=limit,
            skill_rating=SkillRating(rating) if rating else None,
            min_ratings=min_ratings
        )
        
        # Format response
        response = []
        for i, skill in enumerate(leaderboard, 1):
            response.append(LeaderboardResponse(
                rank=i,
                skill_id=skill.skill_id,
                name=skill.name,
                version=skill.version,
                author=skill.author,
                rating=skill.get_skill_rating().value,
                accuracy=skill.get_average_accuracy(),
                execution_time=skill.get_average_execution_time(),
                benchmark_count=len(skill.ratings)
            ).dict())
        
        return {"leaderboard": response}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/skills/{skill_id}/stats")
async def get_skill_stats(skill_id: str):
    """
    Get statistics for a specific skill.
    
    Args:
        skill_id: ID of the skill
        
    Returns:
        Skill statistics
    """
    try:
        stats = arena_manager.engine.get_skill_stats(skill_id)
        
        return SkillStatsResponse(
            skill_id=stats["skill_id"],
            total_benchmarks=stats["total_benchmarks"],
            average_accuracy=stats["average_accuracy"],
            average_execution_time=stats["average_execution_time"],
            average_tokens_used=stats["average_tokens_used"],
            current_rating=stats["current_rating"],
            success_rate=stats["success_rate"],
            last_benchmark=stats["last_benchmark"]
        ).dict()
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/benchmarks/run")
async def run_benchmark(
    skill_id: str,
    task: BenchmarkTask
):
    """
    Run a benchmark against a skill.
    
    Args:
        skill_id: ID of skill to test
        task: Benchmark task details
        
    Returns:
        Benchmark result
    """
    try:
        engine = arena_manager.engine
        
        # Run benchmark
        result = engine.run_benchmark(
            skill_id=skill_id,
            benchmark_id=f"bench_{task.description[:20]}",
            task=task.dict(),
            timeout=30.0
        )
        
        return {
            "success": True,
            "run_id": result.run_id,
            "status": result.status.value,
            "execution_time": result.execution_time,
            "tokens_used": result.tokens_used,
            "accuracy": result.accuracy,
            "error_message": result.error_message
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/skills/{skill_id}")
async def remove_skill(skill_id: str):
    """
    Remove a skill from the arena.
    
    Args:
        skill_id: ID of skill to remove
        
    Returns:
        Removal confirmation
    """
    try:
        success = arena_manager.remove_submission(skill_id)
        
        if success:
            return {"success": True, "message": f"Skill {skill_id} removed"}
        else:
            raise HTTPException(status_code=404, detail="Skill not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
