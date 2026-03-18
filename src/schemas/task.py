from pydantic import BaseModel, EmailStr, Field


class TaskIn(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=4000)
    is_active: bool | None = None
     
class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    is_active: bool
    created_at: str | None
    updated_at: str | None
