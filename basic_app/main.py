from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #default value will be true if user doesnt populate this in req
    
#establish DB connection
try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                            password='Geetha@1955', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection successfull")
except Exception as error:
    print("database conn failed ",error)

my_posts = [{"id":1, "title":"tiruchendur", "content":"Senthil andavar"},
            {"id":2, "title":"Palani", "content":"Dandhayudhapani"}]

@app.get("/")
async def root():
    return {"message":"hello world"}

@app.get("/posts")
async def get_posts():
    cursor.execute("""select * from "Posts" """)    
    posts = cursor.fetchall()    
    return {"data":posts}
    #return {"data":my_posts}

#get the payload (json) in dict format.
@app.post("/posts")
def create_post(post_payload: Post):
    pass

    #print(new_post)
    #return {"message":new_post}

#second param in decorator/annotation is the default status code when post is created
@app.post("/createpost", status_code=status.HTTP_201_CREATED)
async def create_new_post(post:Post):   
   cursor.execute("""Insert INTO "Posts" (title, content) values(%s,%s) Returning *""",
                   (post.title, post.content))
   new_post = cursor.fetchone()
   conn.commit()
   return {"data":new_post}

    #post_dict = post.model_dump()
    #post_dict['id'] = randrange(0,100000)
    #my_posts.append(post_dict)
    

@app.get("/posts/latest")
def get_latest_post():
    return {"data":my_posts[len(my_posts)-1]}

@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute(""" Select * from "Posts" where id = %s""",(str(id),))
    post = cursor.fetchone()
    #post = find_post(id)
    if not(post):
        # way to handle data not exists. the get method signature should be get_post(id: int, response: Response)
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"data":f"post with id {id} not found"}
        #best approach below
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"data" : post}

@app.get("/deletepost/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, ):
    for i, post in enumerate(my_posts):
        if(post['id'] == id):
            my_posts.pop(i)
            return {"data":f"record with {id} found and deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data with {id} not found")

@app.put("/posts/{id}")
async def update_post(id:int, post:Post):
    index= find_index_post(id)
    if index == None:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data" : f"post with id {id} updated successfully"}


def find_post(id: int):
     for post in my_posts:
        if(post["id"] == id):
            return post

def find_index_post(id: int):
    for i, post in enumerate(my_posts):
        if(post['id'] == id):
            return i
    
