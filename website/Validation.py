from pydantic import BaseModel, Field, EmailStr, model_validator

class UserModel(BaseModel):
    email: EmailStr
    firstName: str = Field(max_length=256)
    password1: str = Field(max_length=20, min_length=6)
    password2: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserModel':
        pw1 = self.password1
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self

class NoteModel(BaseModel):
    note: str = Field(max_length=256)

