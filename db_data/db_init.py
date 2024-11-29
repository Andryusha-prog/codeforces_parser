
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from db_data.models import Base


class StartDB:
    session: Session
    __engine: Engine

    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.sb_password = db_password
        self.db_host = db_host
        self.db_port = db_port

        self.__engine = create_engine(
            f"postgresql+psycopg://{self.db_user}:{self.sb_password}@{self.db_host}:{self.db_port}/{self.db_name}")
            #f"postgresql+psycopg://{self.db_user}:{self.sb_password}@localhost:5432/{self.db_name}")
        self.session = Session(bind=self.__engine)


    def create_tables(self):
        Base.metadata.create_all(bind=self.__engine)


    def delete_table(self):
        Base.metadata.drop_all(bind=self.__engine)


    # @staticmethod
    # def create_session():
    #     engine = create_engine("postgresql+psycopg://postgres:admin@localhost:5432/cf_data")
    #     Base.metadata.drop_all(bind=engine)
    #     Base.metadata.create_all(bind=engine)
    #     return Session(bind=engine)

# def start_db():
#     engine = create_engine("postgresql+psycopg://postgres:admin@localhost:5432/cf_data")
#
#     # with engine.connect() as conn:
#     #     res = conn.execute(text('SELECT VERSION()'))
#     #     print(res.all())
#
#     #print(ProblemsTable.__tablename__)
#
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#
#     session = Session(bind=engine)
#
#     return session



    #Вставка данных
    # with Session(bind=engine) as session:
    #     smtm = insert(Problems_table).values(
    #         [
    #             {'contestId': 2041},
    #             {'contestId': 2042}
    #         ]
    #     )
    #     session.execute(smtm)
    #     session.commit()

    #Еще НЕ РАБОЧИЙ способ вставки через SQL запрос
    # with Session(bind=engine) as session:
    #     smtm = '''INSERT INTO problems (contestId) VALUES (2042), (2041);'''
    #     session.execute(text(smtm))
    #     session.commit()

    #И еще способ добавления данных
    # with Session(bind=engine) as session:
    #     data_test = Problems_table(contestId=2042)
    #     data_test2 = Problems_table(contestId=2045)
    #     session.add_all([data_test, data_test2])
    #     session.commit()
