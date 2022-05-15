from fastapi import FastAPI

from routers import users, companies, projects

app = FastAPI()

app.include_router(companies.api)
app.include_router(users.api)
app.include_router(projects.api)
