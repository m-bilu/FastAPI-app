from datetime import date, datetime
from pickletools import int4
from click import password_option
from pydantic import BaseModel, EmailStr
from typing import Optional


####################### IMPORTANT:
###### THS FILE IS FOR PYDANTIC MODELS. THESE ORGANIZE THE FORMAT
######  OF THE INPUT AND RESPONSE FROM DATABASE USING PYDANTICS LIBRARY


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    # FOR response models, u must add this line for some reason, dont forget!!
    class Config:
        orm_mode = True
    # Reason: This line tells Pydantic's Model to read the response as an ORM model
        # instead of a dict (since pydantic mainly works with dicts, and we are using an 
        # ORM to communicate with PostgreSQL, so our response is originally ORM)

# This schema organizes login info for user to log in with
class UserLogin(BaseModel):  # Currently using OAuth thing, USELESS atm
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# ALLOWS us to use inheritance
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):

    userid: int
    user: UserResponse
    created_at: datetime


    # FOR response models, u must add this line for some reason, dont forget!!
    class Config:
        orm_mode = True
    # Reason: This line tells Pydantic's Model to read the response as an ORM model
        # instead of a dict (since pydantic mainly works with dicts, and we are using an 
        # ORM to communicate with PostgreSQL, so our response is originally ORM)


class PostResponseVote(BaseModel):
    Post: PostResponse
    numVotes: int

    class Config:
        orm_mode = True


# Schema for reading in Access Tokens
class Token(BaseModel):
    accessToken: str
    tokenType: str
    id: str

class TokenData(BaseModel):
    id: Optional[str]


########## Votes Schemas
class VoteBase(BaseModel):
    postid: int
    like: bool

class Vote(VoteBase):
    pass

class VoteResponse(VoteBase):
    created_at: datetime
    userid: int

    # FOR response models, u must add this line for some reason, dont forget!!
    class Config:
        orm_mode = True
    # Reason: This line tells Pydantic's Model to read the response as an ORM model
        # instead of a dict (since pydantic mainly works with dicts, and we are using an 
        # ORM to communicate with PostgreSQL, so our response is originally ORM)



############## COMMENTS SCHEMAS
class CommentBase(BaseModel):
    content: str

class Comment(CommentBase):
    pass

class CommentResponse(CommentBase):
    postid: int
    userid: int
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


