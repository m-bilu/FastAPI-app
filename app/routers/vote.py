from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2, models, schemas


router = APIRouter(
    prefix = "/vote",
    tags=["Vote"]) # prefix means u dont have to repeat /posts all the time

@router.post("/")
def vote(vote: schemas.Vote, curUser: int = Depends(oauth2.getCurrentUser), db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == vote.postid).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with id: {vote.postid} cannot be liked, not found")


    likeEntry = db.query(models.Vote).filter(models.Vote.postid == vote.postid, models.Vote.userid == curUser.id).first()

    if vote.like:

        # IF LIKE ALREADY EXISTS, THROW EXCEPTION
        
        if likeEntry:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"You have already liked post with id: {vote.postid}")

        # Creating entry on votes table

        like = models.Vote(postid = vote.postid, userid = curUser.id)
        db.add(like)
        db.commit()
        db.refresh(like)
        return {"detail" : "Vote successful"}
    
    else:

        # IF UNLIKING, WE CANNOT REMOVE ENTRY IF ENTRY NEVER EXISTED:
        if not likeEntry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"You cannot remove like on post: {vote.postid}, does not exist.")

        # Remove entry from votes table, ensure 1-1 correspondence
        like = db.query(models.Vote).filter(models.Vote.userid == curUser.id and 
        models.Vote.postid == vote.postid)
        like.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
