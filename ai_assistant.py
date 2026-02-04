"""
AI Assistant Module for aiD_PM
Provides intelligent features:
- Auto task breakdown
- Smart scheduling
- Resource recommendations
- Risk prediction
"""

from typing import List, Dict, Optional
import datetime
import json
from sqlalchemy.orm import Session
import models

# Configuration
USE_OPENAI = False  # Set to True to use OpenAI API
OPENAI_API_KEY = None  # Set your API key here

if USE_OPENAI and OPENAI_API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
    except ImportError:
        print("⚠️  OpenAI package not installed. Install with: pip install openai")
        USE_OPENAI = False


class AIAssistant:
    """AI-powered project management assistant"""
    
    @staticmethod
    def breakdown_task(task_name: str, task_type: str, resource_speed: int = 5, resource_quality: int = 5) -> List[Dict[str, str]]:
        """
        Break down a task into subtasks, adjusting for resource DNA
        
        Returns: List of subtasks with name and estimated duration
        """
        if USE_OPENAI:
            return AIAssistant._breakdown_with_openai(task_name, task_type, resource_speed, resource_quality)
        else:
            return AIAssistant._breakdown_with_rules(task_name, task_type, resource_speed, resource_quality)
    
    @staticmethod
    def _breakdown_with_openai(task_name: str, task_type: str, resource_speed: int = 5, resource_quality: int = 5) -> List[Dict[str, str]]:
        """Use OpenAI GPT-4 to break down tasks with Resource DNA"""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": f"You are a project management expert. Break down tasks into 3-7 actionable subtasks. Return JSON array with 'subtask_name' and 'estimated_days' fields. Consider Resource Speed (1-10, current={resource_speed}) and Quality (1-10, current={resource_quality}). Higher speed means faster execution."
                }, {
                    "role": "user",
                    "content": f"Break down this {task_type} task: {task_name}"
                }],
                temperature=0.7,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            # Parse JSON from response
            subtasks = json.loads(result)
            return subtasks
        except Exception as e:
            print(f"OpenAI Error: {e}")
            return AIAssistant._breakdown_with_rules(task_name, task_type, resource_speed, resource_quality)
    
    @staticmethod
    def _breakdown_with_rules(task_name: str, task_type: str, resource_speed: int = 5, resource_quality: int = 5) -> List[Dict[str, str]]:
        """Rule-based task breakdown (fallback) with Resource DNA adjustment"""
        
        # Task breakdown templates by type
        templates = {
            "Dev": [
                {"subtask_name": "Requirements Analysis", "estimated_days": 1},
                {"subtask_name": "Design & Architecture", "estimated_days": 2},
                {"subtask_name": "Implementation", "estimated_days": 5},
                {"subtask_name": "Unit Testing", "estimated_days": 2},
                {"subtask_name": "Code Review", "estimated_days": 1},
                {"subtask_name": "Integration Testing", "estimated_days": 2},
                {"subtask_name": "Documentation", "estimated_days": 1},
            ],
            "Fix": [
                {"subtask_name": "Bug Investigation", "estimated_days": 1},
                {"subtask_name": "Root Cause Analysis", "estimated_days": 1},
                {"subtask_name": "Fix Implementation", "estimated_days": 2},
                {"subtask_name": "Testing & Verification", "estimated_days": 1},
                {"subtask_name": "Deployment", "estimated_days": 0.5},
            ],
            "Admin": [
                {"subtask_name": "Planning & Preparation", "estimated_days": 1},
                {"subtask_name": "Execution", "estimated_days": 2},
                {"subtask_name": "Review & Documentation", "estimated_days": 1},
            ],
            "Procurement (PR/PO)": [
                {"subtask_name": "Vendor Research", "estimated_days": 2},
                {"subtask_name": "Quote Comparison", "estimated_days": 1},
                {"subtask_name": "PR/PO Creation", "estimated_days": 1},
                {"subtask_name": "Approval Process", "estimated_days": 3},
                {"subtask_name": "Order Confirmation", "estimated_days": 1},
            ]
        }
        
        # Get template or default
        subtasks = templates.get(task_type, templates["Admin"])
        
        # Customize based on task name keywords
        task_lower = task_name.lower()
        
        if "api" in task_lower or "backend" in task_lower:
            subtasks = [
                {"subtask_name": "API Design & Specification", "estimated_days": 1},
                {"subtask_name": "Database Schema Design", "estimated_days": 1},
                {"subtask_name": "Endpoint Implementation", "estimated_days": 3},
                {"subtask_name": "Authentication & Authorization", "estimated_days": 2},
                {"subtask_name": "API Testing", "estimated_days": 2},
                {"subtask_name": "API Documentation", "estimated_days": 1},
            ]
        elif "ui" in task_lower or "frontend" in task_lower or "interface" in task_lower:
            subtasks = [
                {"subtask_name": "UI/UX Design Mockup", "estimated_days": 2},
                {"subtask_name": "Component Development", "estimated_days": 3},
                {"subtask_name": "Styling & Responsiveness", "estimated_days": 2},
                {"subtask_name": "Integration with Backend", "estimated_days": 2},
                {"subtask_name": "Cross-browser Testing", "estimated_days": 1},
            ]
        elif "database" in task_lower or "db" in task_lower:
            subtasks = [
                {"subtask_name": "Schema Design", "estimated_days": 2},
                {"subtask_name": "Migration Scripts", "estimated_days": 1},
                {"subtask_name": "Data Migration", "estimated_days": 2},
                {"subtask_name": "Performance Optimization", "estimated_days": 1},
                {"subtask_name": "Backup & Recovery Setup", "estimated_days": 1},
            ]
        elif "test" in task_lower or "qa" in task_lower:
            subtasks = [
                {"subtask_name": "Test Plan Creation", "estimated_days": 1},
                {"subtask_name": "Test Case Development", "estimated_days": 2},
                {"subtask_name": "Test Execution", "estimated_days": 3},
                {"subtask_name": "Bug Reporting", "estimated_days": 1},
                {"subtask_name": "Regression Testing", "estimated_days": 2},
            ]
        elif "deploy" in task_lower or "release" in task_lower:
            subtasks = [
                {"subtask_name": "Pre-deployment Checklist", "estimated_days": 1},
                {"subtask_name": "Staging Deployment", "estimated_days": 1},
                {"subtask_name": "Staging Testing", "estimated_days": 1},
                {"subtask_name": "Production Deployment", "estimated_days": 1},
                {"subtask_name": "Post-deployment Monitoring", "estimated_days": 1},
            ]
            
        # --- Apply Resource DNA Adjustment ---
        # Speed Score 1-10 (5 is neutral)
        # >5 means faster (reduce days), <5 means slower (increase days)
        # Factor: 10 -> 0.7x, 5 -> 1.0x, 1 -> 1.4x
        speed_factor = 1.0 - ((resource_speed - 5) * 0.06)
        speed_factor = max(0.5, min(1.5, speed_factor)) # Clamp between 0.5x and 1.5x
        
        adjusted_subtasks = []
        for task in subtasks:
            original_days = float(task["estimated_days"])
            adjusted_days = round(original_days * speed_factor, 1)
            # Ensure minimum 0.5 days unless it was 0
            if original_days > 0 and adjusted_days < 0.5:
                adjusted_days = 0.5
                
            adjusted_subtasks.append({
                "subtask_name": task["subtask_name"],
                "estimated_days": adjusted_days
            })
        
        return adjusted_subtasks
    
    @staticmethod
    def suggest_schedule(
        subtasks: List[Dict[str, str]],
        start_date: datetime.date,
        skip_weekends: bool = True
    ) -> List[Dict[str, any]]:
        """
        Generate smart schedule for subtasks
        
        Returns: List of subtasks with planned_start and planned_end dates
        """
        scheduled_tasks = []
        current_date = start_date
        
        for subtask in subtasks:
            task_start = current_date
            
            # Calculate end date based on estimated days
            days = float(subtask.get("estimated_days", 1))
            days_added = 0
            task_end = task_start
            
            while days_added < days:
                task_end += datetime.timedelta(days=1)
                
                # Skip weekends if needed
                if skip_weekends and task_end.weekday() >= 5:  # Saturday = 5, Sunday = 6
                    continue
                
                days_added += 1
            
            scheduled_tasks.append({
                "subtask_name": subtask["subtask_name"],
                "estimated_days": subtask["estimated_days"],
                "planned_start": task_start.strftime("%Y-%m-%d"),
                "planned_end": task_end.strftime("%Y-%m-%d")
            })
            
            # Next task starts after this one ends
            current_date = task_end + datetime.timedelta(days=1)
            
            # Skip weekends for next task start
            if skip_weekends:
                while current_date.weekday() >= 5:
                    current_date += datetime.timedelta(days=1)
        
        return scheduled_tasks
    
    @staticmethod
    def recommend_resources(
        task_type: str,
        required_skills: List[str],
        db: Session,
        top_n: int = 3
    ) -> List[Dict[str, any]]:
        """
        Enhanced AI-powered resource recommendation
        
        Returns: Top N recommended resources with match scores
        """
        resources = db.query(models.Resource).filter(
            models.Resource.is_active == True
        ).all()
        
        if not resources:
            return []
        
        scored_resources = []
        
        for resource in resources:
            score = 0
            reasons = []
            
            # Get current workload
            tasks_old = db.query(models.Task).filter(
                models.Task.assigned_resource_id == resource.id,
                models.Task.actual_progress < 100
            ).count()
            
            task_ids_new = db.query(models.TaskResource.task_id).filter(
                models.TaskResource.resource_id == resource.id
            ).all()
            tasks_new = db.query(models.Task).filter(
                models.Task.id.in_([t.task_id for t in task_ids_new]),
                models.Task.actual_progress < 100
            ).count()
            
            current_workload = tasks_old + tasks_new
            
            # 1. Skill Match (0-50 points)
            # Parse skills if it's a string
            resource_skills = resource.skills
            if isinstance(resource_skills, str):
                try:
                    import json
                    resource_skills = json.loads(resource_skills)
                except:
                    resource_skills = {}
            elif not isinstance(resource_skills, dict):
                resource_skills = {}
            
            if resource_skills and required_skills:
                matched_skills = 0
                total_skill_level = 0
                
                for skill in required_skills:
                    skill_level = resource_skills.get(skill, 0)
                    if skill_level > 0:
                        matched_skills += 1
                        total_skill_level += skill_level
                        reasons.append(f"{skill}: {skill_level}/10")
                
                if matched_skills > 0:
                    skill_score = (matched_skills / len(required_skills)) * 30
                    skill_quality = (total_skill_level / matched_skills) * 2
                    score += skill_score + skill_quality
            
            # 2. Speed Score (0-20 points)
            if resource.speed_score:
                score += resource.speed_score * 2
                reasons.append(f"Speed: {resource.speed_score}/10")
            
            # 3. Quality Score (0-20 points)
            if resource.quality_score:
                score += resource.quality_score * 2
                reasons.append(f"Quality: {resource.quality_score}/10")
            
            # 4. Workload Factor (0-10 points penalty)
            # Less workload = higher score
            if current_workload == 0:
                workload_bonus = 10
            elif current_workload <= 2:
                workload_bonus = 5
            elif current_workload <= 5:
                workload_bonus = 0
            else:
                workload_bonus = -10
            
            score += workload_bonus
            reasons.append(f"Current tasks: {current_workload}")
            
            scored_resources.append({
                "resource": resource,
                "score": score,
                "reasons": reasons,
                "current_workload": current_workload,
                "match_percentage": min(score, 100)
            })
        
        # Sort by score (descending)
        scored_resources.sort(key=lambda x: x["score"], reverse=True)
        
        return scored_resources[:top_n]
    
    @staticmethod
    def predict_risk(task: models.Task, db: Session) -> Dict[str, any]:
        """
        Predict task risk level using AI
        
        Returns: Risk assessment with score and factors
        """
        risk_score = 0
        risk_factors = []
        
        # 1. Schedule Risk
        if task.planned_end:
            days_remaining = (task.planned_end - datetime.date.today()).days
            
            if days_remaining < 0:
                risk_score += 40
                risk_factors.append(f"⚠️ Overdue by {abs(days_remaining)} days")
            elif days_remaining <= 2:
                risk_score += 30
                risk_factors.append(f"⚠️ Due in {days_remaining} days")
            elif days_remaining <= 7:
                risk_score += 15
                risk_factors.append(f"⏰ Due in {days_remaining} days")
        
        # 2. Progress Risk
        if task.planned_start and task.planned_end:
            total_duration = (task.planned_end - task.planned_start).days
            elapsed_duration = (datetime.date.today() - task.planned_start).days
            
            if total_duration > 0 and elapsed_duration > 0:
                expected_progress = (elapsed_duration / total_duration) * 100
                progress_gap = expected_progress - task.actual_progress
                
                if progress_gap > 30:
                    risk_score += 30
                    risk_factors.append(f"📉 {progress_gap:.0f}% behind schedule")
                elif progress_gap > 15:
                    risk_score += 15
                    risk_factors.append(f"📊 {progress_gap:.0f}% behind schedule")
        
        # 3. Resource Risk
        assigned_count = db.query(models.TaskResource).filter(
            models.TaskResource.task_id == task.id
        ).count()
        
        if assigned_count == 0 and not task.assigned_resource_id:
            risk_score += 20
            risk_factors.append("👤 No resource assigned")
        
        # 4. Dependency Risk (if task is blocked)
        # (This would require a dependencies table - placeholder for now)
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "Critical"
            risk_color = "red"
        elif risk_score >= 50:
            risk_level = "High"
            risk_color = "orange"
        elif risk_score >= 30:
            risk_level = "Medium"
            risk_color = "yellow"
        else:
            risk_level = "Low"
            risk_color = "green"
        
        return {
            "risk_score": min(risk_score, 100),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "risk_factors": risk_factors,
            "recommendations": AIAssistant._get_risk_recommendations(risk_factors)
        }
    
    @staticmethod
    def _get_risk_recommendations(risk_factors: List[str]) -> List[str]:
        """Generate recommendations based on risk factors"""
        recommendations = []
        
        for factor in risk_factors:
            if "Overdue" in factor or "Due in" in factor:
                recommendations.append("🎯 Consider extending deadline or adding resources")
            if "behind schedule" in factor:
                recommendations.append("⚡ Increase task priority and check blockers")
            if "No resource assigned" in factor:
                recommendations.append("👥 Assign qualified resource immediately")
        
        if not recommendations:
            recommendations.append("✅ Continue monitoring task progress")
        
        return recommendations
    
    @staticmethod
    def generate_insights(project_id: int, db: Session) -> Dict[str, any]:
        """
        Generate AI insights for a project
        
        Returns: Project insights and recommendations
        """
        project = db.query(models.Project).filter(models.Project.id == project_id).first()
        
        if not project:
            return {"error": "Project not found"}
        
        tasks = db.query(models.Task).filter(models.Task.project_id == project_id).all()
        
        if not tasks:
            return {
                "message": "No tasks found for analysis",
                "recommendations": ["Start by creating tasks for this project"]
            }
        
        # Calculate metrics
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.actual_progress == 100])
        in_progress_tasks = len([t for t in tasks if 0 < t.actual_progress < 100])
        not_started_tasks = len([t for t in tasks if t.actual_progress == 0])
        
        # Risk analysis
        high_risk_tasks = []
        for task in tasks:
            risk = AIAssistant.predict_risk(task, db)
            if risk["risk_level"] in ["High", "Critical"]:
                high_risk_tasks.append({
                    "task": task,
                    "risk": risk
                })
        
        # Calculate project health
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        if completion_rate >= 80:
            health = "Excellent"
            health_color = "green"
        elif completion_rate >= 60:
            health = "Good"
            health_color = "blue"
        elif completion_rate >= 40:
            health = "Fair"
            health_color = "yellow"
        else:
            health = "At Risk"
            health_color = "red"
        
        # Generate recommendations
        recommendations = []
        
        if high_risk_tasks:
            recommendations.append(f"🚨 {len(high_risk_tasks)} task(s) at high risk - review immediately")
        
        if not_started_tasks > in_progress_tasks + completed_tasks:
            recommendations.append("📋 Many tasks not started - consider sprint planning")
        
        if in_progress_tasks > 5:
            recommendations.append("⚠️ Too many tasks in progress - focus on completion")
        
        if not recommendations:
            recommendations.append("✨ Project is on track - keep up the good work!")
        
        return {
            "project_health": health,
            "health_color": health_color,
            "completion_rate": round(completion_rate, 1),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "not_started_tasks": not_started_tasks,
            "high_risk_tasks_count": len(high_risk_tasks),
            "high_risk_tasks": high_risk_tasks[:5],  # Top 5
            "recommendations": recommendations
        }


# Export singleton instance
ai_assistant = AIAssistant()

