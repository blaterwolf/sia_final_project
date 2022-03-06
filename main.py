from fastapi import FastAPI
from routes import auth_router, user_router, task_router
import models.task_model
import models.user_model
from database import engine

app = FastAPI()

# * Bind all models to the database.
models.task_model.Base.metadata.create_all(bind=engine)
models.user_model.Base.metadata.create_all(bind=engine)


# * Register Routes: Auth/User/Task
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(task_router.router)

# * Test run application


@app.get('/')
def index():
    return {'message': 'Hello World!'}
