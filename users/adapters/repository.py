import abc

from users.domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, email: str) -> model.User:
        raise NotImplementedError

    def list(self):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def create(self, user: model.User):
        self.session.add(user)

    def get(self, reference):
        return self.session.query(model.User).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.User).all()
