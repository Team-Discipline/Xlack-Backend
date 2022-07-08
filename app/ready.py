import os

from fastapi import FastAPI

import app.model.database as database


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

    is_debugging = os.getenv('IS_DEBUGGING')
    if not bool(is_debugging if is_debugging is not None else False):
        print(f'DEPLOY MODE.')
        app.root_path = '/api'

    return app
