from pydantic import BaseModel

class TaskSchema(BaseModel):
    name: str
    user: str
    description: str