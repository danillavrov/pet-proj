from pydantic import BaseModel

class StatScheme(BaseModel):
    user: int
    task_completed: int
    task_failed: int
    task_processed: int