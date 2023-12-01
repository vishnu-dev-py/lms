from fastapi import FastAPI, Body
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import uvicorn

import mysql.connector

#connection_String
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql123",
    database="lms"
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods = ['*']
)


@app.post("/create_student")
async def create_student(student_details:Dict = Body(...)):
    student_details = jsonable_encoder(student_details)
    try:
        cursor = connection.cursor()
        statement = "insert into student (name,age,department) values('{}',{},'{}')".format(student_details['name'], student_details['age'], student_details['department'])
        cursor.execute(statement)
        connection.commit()
        return "Student '{}' Created".format(student_details['name'])

    except Exception as e:
        return "Student not created"


@app.post("/update_student")
async def update_student(student_details:Dict = Body(...)):
    student_details = jsonable_encoder(student_details)
    try:
        cursor = connection.cursor()
        statement = "update student set age = {}, department = '{}', name = '{}' where rollno = {}".format(student_details['age'], student_details['department'],student_details['name'],student_details['roll_no'])
        cursor.execute(statement)
        connection.commit()
        return "Student '{}' Updated!".format(student_details['name'])

    except Exception as e:
        return e


@app.get("/delete_student/{id}")
async def delete_student(id):
    try:
        cursor = connection.cursor()
        statement = "select * from student where rollno = {}".format(int(id))
        cursor.execute(statement)
        student = cursor.fetchone()
        if student:
            statement = "delete from student where rollno = {}".format(int(id))
            cursor.execute(statement)
            connection.commit()
            return "Student {} deleted!".format(id)
        else:
            return "Student {} not found".format(id)
    except Exception as e:
        return e

@app.get("/get_student/{id}")
async def get_student(id):
    try:
        cursor = connection.cursor()
        if int(id) == -1:
            statement = "select * from student"
            cursor.execute(statement)
            rows = cursor.fetchall()
            students = []
            for row in rows:
                students.append(dict(zip(['roll_no', 'name', 'age', 'department'], row)))
            return students
        else:
            statement = "select * from student where rollno = {}".format(int(id))
            cursor.execute(statement)
            student = cursor.fetchone()
            if student:
                return dict(zip(['roll_no', 'name', 'age', 'department'], student))
            else:
                return "Student not found"
    except Exception as e:
        return "Something went wrong"


@app.post("/create_book")
async def books(book_details:Dict = Body(...)):
    book_details = jsonable_encoder(book_details)
    try:
        cursor = connection.cursor()
        statement = "insert into books (bname,author,genre,availability) values('{}','{}','{}', {})".format(book_details['bname'], book_details['author'],book_details['genre'], 1)
        cursor.execute(statement)
        connection.commit()
        return "book '{}' created".format(book_details['bname'])

    except Exception as e:
        return "book not created"
@app.get("/available_books")
async def available_books():
    try:
        cursor = connection.cursor()
        statement = "select * from books where availability = 1"
        cursor.execute(statement)
        rows = cursor.fetchall()
        books = []
        for row in rows:
            books.append(dict(zip(['bid', 'bname', 'author', 'genre', 'availablity'],row)))
        return books
    except Exception as e:
        return "NO Available Books"



@app.get("/get_book/{id}")
async def get_book(id):
    try:
        cursor = connection.cursor()
        if int(id) == -1:
            statement = "select * from books"
            cursor.execute(statement)
            rows = cursor.fetchall()
            books = []
            for row in rows:
                books.append(dict(zip(['bid', 'bname', 'author','genre', 'availability'], row)))
            return books
        else:
            statement = "select * from books where bid = {}".format(int(id))
            cursor.execute(statement)
            book = cursor.fetchone()
            if book:
                return dict(zip(['bid', 'bname', 'author','genre', 'availability'], book))
            else:
                return "book not found"
    except Exception as e:
        return "Something went wrong"

@app.post("/update_book")
async def update_book(book_details: Dict = Body(...)):
        book_details = jsonable_encoder(book_details)
        try:
            cursor = connection.cursor()
            statement = "update books set bname = '{}', genre = '{}', author = '{}' where bid = {}".format(
                book_details['name'], book_details['genre'], book_details['author'],
                book_details['bid'])
            cursor.execute(statement)
            connection.commit()
            return "book '{}' Updated!".format(book_details['name'])

        except Exception as e:
            return e

@app.get("/delete_book/{id}")
async def delete_book(id):
    try:
        cursor = connection.cursor()
        statement = "select * from books where bid= {}".format(int(id))
        cursor.execute(statement)
        book = cursor.fetchone()
        if book:
            statement = "delete from books where bid = {}".format(int(id))
            cursor.execute(statement)
            connection.commit()
            return "book {} deleted!".format(id)
        else:
            return "book {} not found".format(id)
    except Exception as e:
        return e

@app.get("/issue_book/{sid}/{bid}")
async def issue_book(sid,bid):
    try:
        cursor = connection.cursor()
        statement = "insert into issue (sid,bid,status) values ({}, {}, {})".format(sid,bid,1)
        cursor.execute(statement)
        statement = "update books set availability = 0 where bid = {}".format(bid)
        cursor.execute(statement)
        connection.commit()
        return "Book Issued!"
    except Exception as e:
        connection.rollback()
        return "Book not Issued!"


@app.get("/return_book/{issueid}/{bid}")
async def return_book(issueid,bid):
    try:
        cursor = connection.cursor()
        statement = "update issue set status = 0 where issueid = {}".format(issueid)
        cursor.execute(statement)
        statement = "update books set availability = 1 where bid = {}".format(bid)
        cursor.execute(statement)
        connection.commit()
        return "Book returned!!"
    except Exception as e:
        connection.rollback()
        return "Book not returned!!"

@app.get("/get_issued_books")
async def get_issued_books():
    try:
        cursor = connection.cursor()
        statement = "select * from issue where status = 1"
        cursor.execute(statement)
        rows = cursor.fetchall()
        issued_books = []
        for row in rows:
            issued_books.append(dict(zip(['issueid', 'sid', 'bid','status'], row)))
        return issued_books
    except Exception as e:
        return "Somoething went wrong"

@app.get("/issue_book/{sid}/{bid}")
async def issue_book(sid,bid):
    try:
        cursor = connection.cursor()
        statement = "insert into issue (sid,bid,status) values ({}, {}, {})".format(sid,bid,1)
        cursor.execute(statement)
        statement = "update books set eligible= 0 where bid = {}".format(bid)
        cursor.execute(statement)
        connection.commit()
        return "Book Issued to the student!"
    except Exception as e:
        connection.rollback()
        return "Book not Issued to the student!"

@app.get("/return_book/{issueid}/{bid}")
async def return_book(issueid,bid):
    try:
        cursor = connection.cursor()
        statement = "update issue set status = 0 where issueid = {}".format(issueid)
        cursor.execute(statement)
        statement = "update books set eligible = 1 where bid = {}".format(bid)
        cursor.execute(statement)
        connection.commit()
        return "Book returned by the student!!"
    except Exception as e:
        connection.rollback()
        return "Book not returned by the student!!"

if __name__ == "__main__":
    uvicorn.run(
        "main:app"
    )