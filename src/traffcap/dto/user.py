from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str
    fullname: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int = Field(json_schema_extra={
        "resource_id": True
    })

    class Config:
        from_attributes = True
        resource_name: str = "user"
        resource_id: str = "id"
