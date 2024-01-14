from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self):
        return "<{class_name}[{_id}] ({attr})>".format(
            class_name=self.__class__.__name__,
            _id=id(self),
            attr=", ".join("{}={!r}".format(k, v) for k, v in vars(self).items())
        )
