from fastapi import Response, status, HTTPException, Depends, APIRouter 
                                                        ## Response imports error codes
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional # LIST is required to have response of list of post instances
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]) # prefix means u dont have to repeat /posts all the time

# Tags allows for cleaner organization on FastAPI Docs Page


@router.get("/", response_model=List[schemas.PostResponseVote])

def getPosts(db: Session = Depends(get_db), curUser: int = Depends(oauth2.getCurrentUser), 
limit: int = 10, skip: int = 0, search: str = ""):


    # posts = db.query(models.Post).filter(
    #     models.Post.content.contains(search)).limit(limit).offset(skip).all() # .limit is sqlalchemy method allowing query params

    voteResults = db.query(models.Post, func.count(models.Vote.postid).label("numVotes")).join(
        models.Vote, models.Vote.postid == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.content.contains(search)).limit(limit).offset(skip).all()

    return voteResults ## Dict auto-converted to JSON for HTTP request



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createPosts(newPost: schemas.PostCreate, db: Session = Depends(get_db), 
    curUser: int = Depends(oauth2.getCurrentUser)):

    # Second depends forces users to be logged in before they can use the createPosts function
    # Whenever createPosts is called, getCurrentUser is called, and must not raise exception in
    # order for createPosts to continue

    # Instead of listing all fields in the Post param, instead convert post object to dict
    #   (Is possible since Post follows Pydantic model, easily convertable into dict)
    print(curUser.email)

    #Creating instance of Post type auto adds fields as entry in database
    post = models.Post(**newPost.dict(), userid = curUser.id)

    db.add(post)
    db.commit()
    db.refresh(post)    # Refresh returns all datapoints selected from prev SQL query, 
                        # Similar to RETURNING * statement
                        # With commit, posts auto-get ID, get saved on database
 
    # Instance of entry is made, but not commited to PostgreSQL database. So remember to COMMIT
    return post


## IMPORTANT NOTES ABOUT SQL INJECTION ATTACK:
    # Above, we could have instead used an fstring for the parameters of the new post.
    # We instead used the % form, and passed parameters to execute for the new fields.
    # We did this because through the initial method, one can pass SQL commands 
    # as values for the cells, and that would cause a subquery to run, potentially 
    # allowing outsiders to access any data in our database. HENCE, this is secure.


## What is our Schema? Using Pydantics
# title str, content str

@router.get("/{id}", response_model=schemas.PostResponseVote) ## Specific decorator. @app is the FastAPI instance,
                        ##  get is the HTTP request for reading info from database,
                        ##  /posts/{id} is url of specific post u want to read
def getPost(id: int, db: Session = Depends(get_db), curUser: int = Depends(oauth2.getCurrentUser)):
    
    post = db.query(models.Post, func.count(models.Vote.postid).label("numVotes")).join(
        models.Vote, models.Vote.postid == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail = f"posts with id: {id} not found.")

    return post


    ## DELETING POSTS
@router.delete("/{id}", response_model=schemas.PostResponse)

def deletePost(id: int, db: Session = Depends(get_db),
 curUser: int = Depends(oauth2.getCurrentUser)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"post with id: {id} cannot be deleted, does not exist.")

    if (post.first().userid != curUser.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail = f"You are not the owner of post with id: {id}.")
        
    
    post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


## UPDATING POSTS
@router.put("/{id}", response_model=schemas.PostResponse)

def updatePost(id: int, newPost: schemas.PostCreate, db: Session = Depends(get_db),
    curUser: int = Depends(oauth2.getCurrentUser)): ## newPost is taken from FrontEnd/Postman requests


    print(newPost.dict())

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with ID {id} was not found.")

    post_query.update(newPost.dict(), synchronize_session=False)
    db.commit()

    return post