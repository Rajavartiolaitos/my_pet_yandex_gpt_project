from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


engine = create_engine(url="postgresql://pet_user:pet_password@localhost/pet_database")
session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class AnswersRequests(Base):
    __tablename__ = 'answers_requests'

    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(index=True)
    answer: Mapped[str]
    role: Mapped[str]
    response: Mapped[str]


def get_user_requests(ip_address: str):
    with session() as ss:
        query = select(AnswersRequests).filter_by(ip_address=ip_address)
        result = ss.execute(query)
        return result.scalars().all()


def add_user_data(ip_address: str, answer: str, role: str, response: str) -> None:
    with session() as ss:
        new_request = AnswersRequests(
            ip_address=ip_address,
            answer=answer,
            role=role,
            response=response
        )
        ss.add(new_request)
        ss.commit()
