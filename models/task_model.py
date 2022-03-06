from sqlalchemy import String, DateTime, text, Boolean
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Task(Base):
    __tablename__ = 'Tasks'

    task_id = Column(String(36), primary_key=True, default=text('UUID()'))
    author_id = Column(String(36), ForeignKey('Users.user_id'), nullable=False)
    task_name = Column(String(255), nullable=False)
    task_is_complete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    author = relationship('User', back_populates='tasks')
