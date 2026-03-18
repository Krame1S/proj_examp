from pydantic import BaseModel, EmailStr


class TaskIn(BaseModel):
    title: str
    description: str
     
class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    is_active: bool