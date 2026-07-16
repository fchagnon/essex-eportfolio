from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol
from datetime import datetime, timezone

@dataclass
class ActionContext:
    correlation_id: str
    user_id: str
    payload: Any

class Action(ABC):
    @abstractmethod
    def execute(self, context: ActionContext) -> None:
        pass

@dataclass
class Submission:
    student_id: str
    assignment_id: str
    file_content: bytes
    comments: str
    submitted_at: datetime

@dataclass
class SubmitAssignmentPayload:
    assignment_id: str
    student_id: str
    file_content: bytes | None
    student_comments: str

# We define a clean boundary interface for persistence
class SubmissionRepository(Protocol):
    def save(self, submission: Submission) -> None: ...

class SubmitAssignmentAction(Action):
    def __init__(self, repository: SubmissionRepository):
        self.repository = repository  # Injected dependency

    def execute(self, context: ActionContext) -> None:
        payload: SubmitAssignmentPayload = context.payload
        
        # 1. Validation
        if payload.file_content is None:
            raise ValueError("File content is required.")
        if not payload.assignment_id or not payload.assignment_id.strip():
            raise ValueError("Assignment ID is required and cannot be empty.")

        # 2. Business Logic & Translation
        submission = Submission(
            student_id=payload.student_id,
            assignment_id=payload.assignment_id,
            file_content=payload.file_content,
            comments=payload.student_comments,
            submitted_at=datetime.now(timezone.utc)  # Real business side-effect
        )

        # 3. Persistence side-effect
        self.repository.save(submission)
