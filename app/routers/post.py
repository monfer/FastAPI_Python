import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from typing import List, Optional

router = APIRouter(tags=['Posts'])


#@router.get("/post", response_model=List[schemas.PostVote])
@router.get("/post")
def get_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user),
limit:int=10, skip:int=0, search:Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

   # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
            models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return  posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = 
Depends(oauth2.get_current_user)):
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    # (post.title, post.content, post.publish))
    
    # new_post = cursor.fetchone()

    # conn.commit()

    #new_post = models.Post(title= post.title, content=post.content, published=post.publish)

    print(current_user)

    print(post.dict())
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#@router.get("/post/{id}", response_model=schemas.PostOut)
@router.get("/post/{id}")
def get_post(id:int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
            models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    query= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
            models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)

    print(query)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    
    print(post)
    return post


@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # print (post.owner_id)

    # print(current_user.id)
    
    if post_query.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id {id} does not exist')

    
    elif str(post.owner_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f'You are not allowed to perform this operation')

    else:
        post_query.delete(synchronize_session=False)
        db.commit()
    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/post/{id}", response_model=schemas.PostOut)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = 
Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title =%s, content=%s, published=%s WHERE id = %s RETURNING *""", 
    # (post.title, post.content, post.publish, str(id)))

    # updated_post = cursor.fetchone()

    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id {id} does not exist')
    
    elif str(post.owner_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f'You are not allowed to perform this operation')

    else:
        post_query.update(updated_post.dict(), synchronize_session=False)
        db.commit()

    return  post_query.first()