from fastapi import FastAPI

from routers import companies, projects, users

app = FastAPI()

app.include_router(companies.api)
app.include_router(users.api)
app.include_router(projects.api)
