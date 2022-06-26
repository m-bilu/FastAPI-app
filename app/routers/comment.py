
from fastapi import APIRouter, Depends, HTTPException, status
from requests import post
from ..database import get_db 
from .. import oauth2, models, schemas
from sqlalchemy.orm import Session
from typing import List # LIST is required to have response of list of post instances



router = APIRouter(
    prefix="/comments",
    tags=["Comments"])

@router.get("/{id}", response_model = List[schemas.CommentResponse]) # id is postid, since comments are under a specific post, made by specific user
def getPostComments(id: int, db: Session = Depends(get_db), curUser: int = Depends(oauth2.getCurrentUser)):
    comments = db.query(models.Comment).filter(models.Comment.postid == id).all()
    return comments

@router.post("/{id}", response_model = schemas.CommentResponse) # id is postid, since comments are under a specific post, made by specific user
def createPostComments(id: int, input: schemas.Comment, db: Session = Depends(get_db), curUser: int = Depends(oauth2.getCurrentUser)):

    # IF POST DOES NOT EXIST, OR IF USER DOES NOT EXIST, RAISE EXCEPTION
    postQuery = db.query(models.Post).filter(models.Post.id == id).first()
    userQuery = db.query(models.User).filter(models.User.id == curUser.id).first()

    if postQuery == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} not found.")
    if userQuery == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id: {curUser.id} does not exist.")
    comment = models.Comment(**input.dict(), userid = curUser.id, postid = id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
