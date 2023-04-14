from fastapi import FastAPI, HTTPException, Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to simple Python REST API by Samuel Christopher S"}


@app.get("/books")
def getBooks(session: Session = Depends(get_session)):
    # query select * from books
    data = session.query(models.Book).all()
    return {
        "timestamp": datetime.now(),
        "status": 200,
        "message": "Retrieve All Data Successfully",
        "books": data,
    }


@app.get("/books/{id}")
def getBook(id: int, session: Session = Depends(get_session)):
    # query select * from books where id = ?
    data = session.query(models.Book).get(id)
    if data is None:
        raise HTTPException(status_code=404, detail="Data Not Found")

    return {
        "timestamp": datetime.now(),
        "status": 200,
        "message": "Retrieve Data by ID Successfully",
        "books": {
            "id": data.id,
            "title": data.title,
            "year": data.year,
            "author": data.author,
            "publisher": data.publisher,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
            "deleted_at": data.deleted_at
        },
    }


@app.post("/books", status_code=201)
def addBook(book: schemas.Book, session=Depends(get_session)):
    # query select * from books where title = ? and deleted_at is null (status still active)
    get_data_by_title = session.query(models.Book).filter(
        models.Book.title == book.title,
        models.Book.deleted_at == None
    ).first()
    # if query above return data, show message Data Already Registered
    if get_data_by_title:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Data Already Registered"
            }
        )

    # else mapping data to Book models using Book schemas and insert to database
    data = models.Book(
        title=book.title,
        year=book.year,
        author=book.author,
        publisher=book.publisher
    )
    session.add(data)
    session.commit()
    session.refresh(data)
    return {
        "timestamp": datetime.now(),
        "status": 201,
        "message": "New Data Created",
        "books": {
            "id": data.id,
            "title": data.title,
            "year": data.year,
            "author": data.author,
            "publisher": data.publisher,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
            "deleted_at": data.deleted_at
        },
    }


@app.put("/books/{id}")
def updateBook(id: int, book: schemas.Book, session=Depends(get_session)):
    # query select * from books where id = ? and deleted_at is null (status still active)
    data = session.query(models.Book).filter(
        models.Book.id == id,
        models.Book.deleted_at == None
    ).first()
    # if query above return nothing, show message Data not Found
    if data is None:
        raise HTTPException(status_code=404, detail="Data Not Found")

    # query select * from books where id != ? and title = ? and deleted_at is null (status still active)
    get_data_by_title = session.query(models.Book).filter(
        models.Book.id != id,
        models.Book.title == book.title,
        models.Book.deleted_at == None
    ).first()
    # if query above return data, show message Data Already Registered
    if get_data_by_title:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Data Already Registered"
            }
        )

    # else mapping data to Book models using Book schemas and insert to database
    data.title = book.title
    data.year = book.year
    data.author = book.author
    data.publisher = book.publisher
    data.updated_at = datetime.now()
    session.commit()
    return {
        "timestamp": datetime.now(),
        "status": 200,
        "message": "Successfully Updated Data by ID",
        "books": {
            "id": data.id,
            "title": data.title,
            "year": data.year,
            "author": data.author,
            "publisher": data.publisher,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
            "deleted_at": data.deleted_at
        },
    }


@app.delete("/books/{id}")
def deleteBook(id: int, session=Depends(get_session)):
    # query select * from books where id = ? and deleted_at is null (status still active)
    data = session.query(models.Book).filter(
        models.Book.id == id,
        models.Book.deleted_at == None
    ).first()
    # if query above return nothing, show message Data Not Found
    if data is None:
        raise HTTPException(status_code=404, detail="Data Not Found")

    # else set data
    data.deleted_at = datetime.now()
    session.commit()
    session.close()
    return {
        "timestamp": datetime.now(),
        "status": 200,
        "message": "Successfully Deleted Data by ID",
        "books": None,
    }
