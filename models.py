from sqlalchemy import Column, Integer, String
from database import Base

# 用户表（增加密码字段）
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # 用户名唯一
    age = Column(Integer)
    password = Column(String)  # 密码（加密存储）