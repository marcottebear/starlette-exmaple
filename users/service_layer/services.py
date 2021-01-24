from users.adapters.repository import AbstractRepository
from users.domain import model


def add_user(
    email: str,
    password: str,
    repo: AbstractRepository,
    session,
) -> int:
    user = model.User(email, password)
    print(user)
    repo.create(user)
    session.commit()
    print(user)
    return user.id


def users(repo: AbstractRepository):
    return repo.list()
