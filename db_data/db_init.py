
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from db_data.models import Base


class StartDB:
    session: Session
    __engine: Engine

    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        """
        При инициализации происходит определение движка и создание сессии для работы с БД
        """
        self.db_name = db_name
        self.db_user = db_user
        self.sb_password = db_password
        self.db_host = db_host
        self.db_port = db_port

        self.__engine = create_engine(
            f"postgresql+psycopg2://{self.db_user}:{self.sb_password}@{self.db_host}:{self.db_port}/{self.db_name}")
        self.session = Session(bind=self.__engine)


    def create_tables(self):
        """
        Создает таблицы, определенные в models.py
        """
        Base.metadata.create_all(bind=self.__engine)


    def delete_table(self):
        """
        Удаляет таблицы, определенные в models.py
        """
        Base.metadata.drop_all(bind=self.__engine)
