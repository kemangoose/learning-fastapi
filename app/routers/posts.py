from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db
from ..schema import PostOut, PostBase, Post
from ..oauth2 import get_current_user
from .. import models

router = APIRouter(tags = ['Posts'])

@router.get('/posts', status_code = status.HTTP_200_OK, response_model=List[PostOut])
async def get_posts(limit:int=10, skip:int = 0, search:Optional[str] = "", db:Session = Depends(get_db)):
        posts = db.query(models.Posts, func.count(models.Vote.post_id).label('votes')
                ).join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True
                ).group_by(models.Posts.id).filter(models.Posts.title.contains(search)
                ).limit(limit).offset(skip).all()

        posts = list(map (lambda x : x._mapping, posts) )
        return posts

@router.get('/posts/{id}', status_code = status.HTTP_200_OK)
async def get_post(id:int, db:Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    post = db.query(models.Posts).filter(models.Posts.title.contains('I')).first()
    #post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'not found')
    return post

@router.post('/posts', status_code = status.HTTP_201_CREATED,response_model = Post)
async def create_post(posts:PostBase, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    post_in = models.Posts(owner_id = current_user.id,**posts.dict())
    db.add(post_in)
    db.commit()
    db.refresh(post_in)

    return post_in

@router.put('/posts/{id}', status_code = status.HTTP_200_OK)
async def update_post(id:int, posts:PostBase, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = 'you are not authorized to perform this request'
        )
    
    post_query.update(posts.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

@router.delete('/posts/{id}', status_code=status.HTTP_200_OK)
async def delete_post(id:int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = 'you are not authorized to perform this request'
        )
    
    post_query.delete(synchronize_session=False)

    db.commit()

    return {'message':'post was deleted successfully'}
    

    
