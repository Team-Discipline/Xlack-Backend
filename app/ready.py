import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.model.database as database


def ready_for_cors(app: FastAPI) -> FastAPI:
    origins = [
        '*'
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def ready_for_db():
    database.Base.metadata.create_all(bind=database.engine)
    print(f'Ready for db!')


def ready_app() -> FastAPI:
    ready_for_db()

    app = FastAPI(
        title='Xlack',
        description='Furthermore Workspace.',
        version='0.1.0'
    )

    app = ready_for_cors(app)

    is_debugging = os.getenv('IS_DEBUGGING')
    if not bool(is_debugging if is_debugging is not None else False):
        print(f'DEPLOY MODE.')
        app.root_path = '/api'

    return app
