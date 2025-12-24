from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    customer = Column(String, nullable=True)
    methodology = Column(String, default="Waterfall")  # Waterfall, Scrum, Kanban
    is_recovery_mode = Column(Boolean, default=False)
    budget_masked = Column(String, nullable=True)
    progress = Column(Float, default=0.0)  # Real-time calculated progress
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    tasks = relationship("Task", back_populates="project")
    phases = relationship("ProjectPhase", back_populates="project")

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    nickname = Column(String, nullable=True)
    position = Column(String, nullable=True)
    speed_score = Column(Integer, default=5)
    quality_score = Column(Integer, default=5)
    company = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    skills = Column(String, nullable=True)  # JSON String
    is_active = Column(Boolean, default=True)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    task_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)  # Dev, Admin, Procurement, Fix
    weight_score = Column(Float, default=1.0)
    assigned_resource_id = Column(Integer, ForeignKey("resources.id"), nullable=True)
    actual_progress = Column(Float, default=0.0)
    planned_start = Column(Date, nullable=True)
    planned_end = Column(Date, nullable=True)
    phase_id = Column(Integer, ForeignKey("project_phases.id"), nullable=True)  # NEW: Link to phase
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="tasks")
    assigned_resource = relationship("Resource", foreign_keys=[assigned_resource_id])
    phase = relationship("ProjectPhase", back_populates="tasks")  # NEW
    task_resources = relationship("TaskResource", back_populates="task", cascade="all, delete-orphan")

class TaskResource(Base):
    """Many-to-Many: Task <-> Resource (Multi-assign support)"""
    __tablename__ = "task_resources"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    role = Column(String, nullable=True)  # Lead, Support, Reviewer, etc.
    assigned_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    task = relationship("Task", back_populates="task_resources")
    resource = relationship("Resource")

class WeeklySnapshot(Base):
    __tablename__ = "weekly_snapshots"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    week_number = Column(Integer)
    plan_acc = Column(Float)  # For PB Curve plotting
    actual_acc = Column(Float)  # For PB Curve plotting
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    action_type = Column(String)  # created, updated, assigned, etc.
    description = Column(String)
    user_name = Column(String, default="System")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_name = Column(String, default="User")
    comment_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ProjectPhase(Base):
    __tablename__ = "project_phases"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    phase_name = Column(String, nullable=False)
    phase_order = Column(Integer, default=0)
    planned_start = Column(Date, nullable=True)
    planned_end = Column(Date, nullable=True)
    status = Column(String, default="pending")  # pending, in_progress, completed
    description = Column(String, nullable=True)
    is_recovery_mode = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="phases")
    tasks = relationship("Task", back_populates="phase")  # NEW

class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    phase_id = Column(Integer, ForeignKey("project_phases.id"), nullable=True)
    issue_title = Column(String, nullable=False)
    issue_description = Column(String, nullable=True)
    issue_type = Column(String, default="Bug")
    severity = Column(String, default="Medium")
    priority = Column(String, default="Medium")
    status = Column(String, default="Open")
    pic_resource_id = Column(Integer, ForeignKey("resources.id"), nullable=True)
    reporter_name = Column(String, default="System")
    resolution = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

class IssueResource(Base):
    """Many-to-Many: Issue <-> Resource"""
    __tablename__ = "issue_resources"
    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    role = Column(String, nullable=True)
    assigned_at = Column(DateTime, default=datetime.datetime.utcnow)

class IssueComment(Base):
    __tablename__ = "issue_comments"
    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"))
    user_name = Column(String, default="User")
    comment_text = Column(String, nullable=False)
    comment_type = Column(String, default="comment")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class IssueAttachment(Base):
    __tablename__ = "issue_attachments"
    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"))
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_by = Column(String, default="User")
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
