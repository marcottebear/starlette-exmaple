import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.schemas import SchemaGenerator
from starlette.config import Config
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from users.adapters import orm, repository

# Configuration from environment variables or '.env' file.
from users.service_layer import services

config = Config(".env")
DATABASE_URL = config("DATABASE_URL")

schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Example API", "version": "1.0"}}
)

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(DATABASE_URL))

def list_users(request):
    """
    responses:
      200:
        description: A list of users.
        examples:
          [{"username": "tom"}, {"username": "lucy"}]
    """
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    users = services.users(repo)

    content = [
        {
            "email": user.email,
        }
        for user in users
    ]
    return JSONResponse(content)

async def create_user(request):
    """
    responses:
      200:
        description: A user.
        examples:
          {"username": "tom"}
    """

    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    data = await request.json()

    services.add_user(data["email"], data["password"], repo, session)
    return JSONResponse({"status_code": 201, "id": id})


def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)


routes = [
    Route("/users", endpoint=list_users, methods=["GET"]),
    Route("/create_user", endpoint=create_user, methods=["POST"]),
    Route("/schema", endpoint=openapi_schema, include_in_schema=False),
]


app = Starlette(
    debug=True,
    routes=routes,
)


@app.route("/")
async def homepage(request):
    return JSONResponse({"hello": "world"})


@app.route("/error")
async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
