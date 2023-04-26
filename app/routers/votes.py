from fastapi import APIRouter, status, HTTPException, Depends 
from sqlalchemy.orm import Session
from .. import database, models, oauth2, schema


router = APIRouter(tags=['Vote'], prefix='/vote')

@router.post('/', status_code = status.HTTP_201_CREATED)
async def vote(vote:schema.Vote, db:Session = Depends(database.get_db), current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == vote.post_id)

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    
    if vote.dir == 1:
        if post_query.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'The post is not found')
        
        if vote_query.first() != None:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'You cannot vote twice on one vote')
        
        vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(vote)
        db.commit()

        return {'message':'successfully vote for the post'}
    else:
        if post_query.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'the post is not found')
        
        if vote_query.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'the vote does not exists')
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message':'the vote was successfully removed'}

