from project import db
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func


@dataclass
class Task(db.Model):
    id: int
    project_id:int
    title:str
    comment:str
    status:str
    is_active:bool
    last_completed_at:str
    created_by:int
    created_at:str

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, db.ForeignKey("projects.id"), nullable=False)
    title = Column(String(50))
    comment = Column(String(50))
    status = Column(String(20), default="incomplete")
    is_active = Column(Boolean, default=True)
    last_completed_at = Column(DateTime(timezone=True))
    created_by = Column(Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(
        self,
        project_id: int,
        title="",
        comment="",
        status="incomplete",
        created_by=None,
    ):
        self.title = title
        self.project_id = project_id
        self.comment = comment
        self.status = status
        self.created_by = created_by

    def __repr__(self) -> str:
        return str(f"<Task {self.id} {self.title}>")


# worked_by: []
# assignees: []
# reviewers: []
# tags: []
