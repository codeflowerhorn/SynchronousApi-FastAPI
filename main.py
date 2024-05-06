import uvicorn 
import asyncio

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() # fastapi object
id_counter = [0] # temporary id
books = {} # store our temporary data

app = FastAPI(
    title="Books API",
    description="A simple api for CRUD operations",
    version="1.0",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def insert(title: str, author: str, genre: str):
    id_counter[0] = id_counter[0] + 1 
    id = id_counter[0]
    books[id] = {
        "id": id,
        "title": title,
        "author": author,
        "genre": genre
    }

    data = {
        "message": "Created",
        "results": books[id]
    }

    await asyncio.sleep(1)
    return data

async def get(id: int):
    data = None
    if id in books:
        data = {
            "message": "Get",
            "results": books[id]
        }
    else:
        data = {
            "message": "Item not found",
            "results": {}
        }
    await asyncio.sleep(1)
    return data

async def getall():
    data = {
        "message": "Get",
        "results": books
    }
    await asyncio.sleep(1)
    return data

async def update(id: int, title: str, author: str, genre: str):
    data = None
    if id in books:
        if title != None:
            books[id]["title"] = title
        if author != None:
            books[id]["author"] = author
        if genre != None:
            books[id]["genre"] = genre
        data = {
            "message": "Updated",
            "results": books[id]
        }
    else:
        data = {
            "message": "Item not found",
            "results": {}
        }

    await asyncio.sleep(1)
    return data
   
async def delete(id: int):
    data = None
    if id in books: 
        results = books[id]
        del books[id]
        data = {
            "message": "Deleted",
            "results": results
        }
    else:
        data = {
            "message": "Item not found",
            "results": {}
        }

    await asyncio.sleep(1)
    return data
   
@app.get("/book/{id}", status_code=status.HTTP_200_OK)
async def get_book(id: int):
    book = await get(id)
    return book

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books():
    books = await getall()
    return books
    
@app.post("/book", status_code=status.HTTP_201_CREATED)
async def create_book(title: str, author: str, genre: str):
    book = await insert(title, author, genre)
    return book

@app.put("/book/{id}", status_code=status.HTTP_200_OK)
async def update_book(id: int, title: str = None, author: str = None, genre: str = None):
    return await update(id, title, author, genre)

@app.delete("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int):
    return await delete(id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
        