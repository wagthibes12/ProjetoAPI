from pydantic import BaseModel,Field,EmailStr

class Agenda(BaseModel):
    id: int = Field(default=None,gt=10,description="id do contato")
    email : EmailStr
