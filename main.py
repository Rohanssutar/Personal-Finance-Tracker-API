from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import transactions, users
from database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Personal Finance Tracker API",
    version='1.0.0',
    description="""
A backend API for managing income and expense transactions, with summaries and filtering.
              
### Features
* Create, read, update, and delete transactions
* Get transactions and users by id
* Filter transactions by amount range, type, category, and date
* View financial summaries (Total Expenses, Total Income and Current Balance)
* View analytical summaries (Monthly Expenses, Category-wise Expenses)
* Input Validation and custom error handling
    """,
    servers=[
        {"url": "http://localhost:8000", "description": "Local Development Server"}
    ]
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": request.url.path,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid input",
            "details": exc.errors(),
            "body": exc.body,
            "path": request.url.path,
        },
    )


app.include_router(transactions.router)
app.include_router(users.router)
