from fastapi import FastAPI

from routers import companies, projects, users

app = FastAPI(debug=True, port=5001)

app.include_router(companies.api)
app.include_router(users.api)
app.include_router(projects.api)
