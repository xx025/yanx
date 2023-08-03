from sqlalchemy import Column, String, Boolean

from database import Base


class Download(Base):
    __tablename__ = 'download_task'

    task_name = Column(String)
    id = Column(String, primary_key=True)
    available = Column(Boolean)
    atime = Column(String)
