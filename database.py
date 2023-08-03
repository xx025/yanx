from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    # echo=True 表示引擎将用repr() 函数记录所有的语句及参数列表到日志
    # 由于SQLAlchemy 是多线程，指定check_same_thread=False来让建立的对象任意线程都可用

    SQLALCHEMY_DATABASE_URL, encoding='utf-8', echo=True, connect_args={'check_same_thread': False}

)

# 在SQLAlchemy中 ，CURD都是通过会话(session)进行的，所以我们必须要先创建会话，每一个SessionLocal实例就是一个数据库session
# flush()是指发送数据库语句到数据库，但数据库不一定执行写入磁盘；commit()是指提交事务，将变更保存到数据库文件
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本的映射类
Base = declarative_base(bind=engine, name='Base')


def get_db() -> Session:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
