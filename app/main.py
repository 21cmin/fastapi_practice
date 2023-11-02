from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, Response, Depends
import psycopg
from psycopg.rows import dict_row
import time
from . import models, schemas
from .database import engine, Session, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(engine)

app = FastAPI()

my_posts = [
  {
    "title": "title of post 1", 
    "content": "content of post 1",
    "id": 1
  },
  {
    "title": "favorite foods", 
    "content": "i like pizza",
    "id": 2
  },
]

# while True:
#   try:
#     conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=1234", row_factory=dict_row)

#     print("Database connection was successfull")
#     break
#   except Exception as error:
#     print("err: ", error)
#     time.sleep(2)

def find_post(id):
  for p in my_posts:
    if p['id'] == id:
      return p

def find_index_post(id):
  for i, p in enumerate(my_posts):
    if p['id'] == id:
      return i


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
  # cur = conn.execute("SELECT * FROM posts").fetchall()
  posts = db.query(models.Post).all()
  return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
  # cur = conn.execute("""
  #   INSERT INTO posts (title, content, published) 
  #   VALUES (%s, %s, %s) returning *""", (post.title, post.content, post.published))
  # new_post = cur.fetchone()
  # conn.commit()
  # new_post = models.Post(title=post.title, content=post.content, published=post.published)
  new_post = models.Post(**post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
#   cur = conn.execute("SELECT * FROM posts WHERE id = %s", (id,))
#   post = cur.fetchone()
  post = db.query(models.Post).filter(models.Post.id == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
  return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  db.query(models.Post).filter(models.Post.id == id)
  # cur = conn.execute("DELETE FROM posts WHERE id = %s returning *", (id,))
  # deleted_post = cur.fetchone()
  # conn.commit()
  post_query = db.query(models.Post).filter(models.Post.id == id)
  if not post_query.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

  post_query.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
  # cur = conn.execute(
  #   "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
  #   (post.title, post.content, post.published, id)
  # )
  # updated_post = cur.fetchone()
  # conn.commit()
  post_query = db.query(models.Post).filter(models.Post.id == id)
  find_post = post_query.first()
  if not find_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

  post_query.update(post.model_dump(), synchronize_session=False)
  db.commit()
  db.refresh(find_post)
  return find_post
