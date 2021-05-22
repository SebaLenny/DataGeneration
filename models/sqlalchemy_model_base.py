from base.model_base import ModelBase
from base.class_base import ClassBase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class SqlAlchemyModelBase(ModelBase):
    def __init__(self,
                 dialect: str,
                 username: str,
                 password: str,
                 host: str,
                 port: str,
                 database: str,
                 declarative_base,
                 driver: str = "") -> None:
        super().__init__()
        self.connection_string = ""
        self.set_connection_string(
            dialect, username, password, host, port, database, driver)
        self.db = create_engine(self.connection_string)
        self.declarative_base = declarative_base
        self.SessionMaker = sessionmaker(self.db)

    def set_connection_string(self,
                              dialect: str,
                              username: str,
                              password: str,
                              host: str,
                              port: str,
                              database: str,
                              driver: str = "") -> None:
        if driver != "":
            dialect = f"{driver}+{dialect}"
        self.connection_string = f"{dialect}://{username}:{password}@{host}:{port}/{database}"

    def save_to_db(self):
        session = self.SessionMaker()
        self.declarative_base.metadata.create_all(self.db)
        for class_base in self.classes:
            session.add_all(class_base.instances)
        session.commit()

    def clear_instances(self):
        for b_class in self.classes:
            b_class.clear_instances()

    def generate_data_batches(self, batches: int):
        for _ in range(batches):
            print(f"{_+1} batch out of {batches}")
            self.generate_data()
            self.save_to_db()
            self.clear_instances()
