from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oath2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func


router = APIRouter(
    prefix = "/posts", 
    tags = ["posts"]
)

#@router.get("/", response_model = List[schemas.PostOut])
@router.get("/", response_model = List[schemas.PostOut])
# @app.get("/posts")
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user), 
             limit: int = 10, 
             skip: int = 0,
             search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).
                     label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                          isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # return posts
    return posts
    # return 0
    # return [Post.from_orm[Post] for Post in posts]

# @app.post("/createpost")ß
# def create_post(certain_post: dict = Body(...)):
#     print(certain_post)
#     title = certain_post['title']
#     body = certain_post['content']
#     return {
#         "new_post": f"Title {title}, Body: {body}"
#         }

# @app.post("/posts")
# def create_post(new_post: Post):
#     post_dict = new_post.dict()
#     post_dict["id"] = randrange(0, 10000000)
#     my_posts.append(post_dict)
#     return {"data": post_dict}


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(new_post: schemas.CreatedPost, db: Session = Depends(get_db), 
                current_user: int = Depends(oath2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #               (new_post.title, new_post.content, new_post.published))
    # the_post = cursor.fetchone()

    # conn.commit()
    #CREATED A POST 
    created_post = models.Post(owner_id = current_user.id, **new_post.dict())
    #ADDING NEW POST TO THE DB 
    db.add(created_post)
    #COMMITTING NEW POST 
    db.commit()
    #SHOWING NEW POST TO THE USER AFTER CREATION 
    db.refresh(created_post)

    return created_post

# @app.get("/posts/{id}")
# def get_certain_post(id: int, response: Response):

#     searched_post = find_post(id)
#     if not searched_post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"post with id {id} was not found"}
#     return {"your post": searched_post}

# @app.get("/posts/{id}")
# def get_certain_post(id: int):

#     searched_post = find_post(id)
#     if not searched_post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was not found")
#     return {"your post": searched_post}

@router.get("/{id}", response_model = schemas.PostOut)
def get_certain_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # searched_post = cursor.fetchone()    
    #searched_post = db.query(models.Post).filter(models.Post.id == id).first()
    searched_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(searched_post)

    if not searched_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was not found")
    
    return searched_post

# @app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index = find_post_index(id)

#     if index == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"the post with id {id} does not exist")
    
#     my_posts.pop(index)
#     return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # searched_post = cursor.fetchone()   
    # conn.commit() 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"the post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized for required action")
    
    post_query.delete(synchronize_session = False)
    db.commit()

    
    return Response(status_code = status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id: int, post: Post): 

#     index = find_post_index(id)

#     if index == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"the post with id {id} does not exist")
    
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_posts[index] = post_dict

#     return {"data": post_dict}

@router.put("/{id}", response_model = schemas.PostResponse)
def update_post(id: str, post: schemas.PostBase, db: Session = Depends(get_db), 
                current_user: int = Depends(oath2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                (post.title, post.content, post.published, str(id)))
    # new_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    new_post = post_query.first()


    if new_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"the post with id {id} does not exist")
    
    post_query.update(post.dict(), synchronize_session = False)

    db.commit()

    return post_query.first()