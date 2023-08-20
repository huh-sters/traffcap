from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    email: str
    fullname: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(json_schema_extra={
        "resource_id": True
    })
