from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import text
from datetime import datetime

class Post(Base):
  __tablename__ = "posts"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
  title: Mapped[str]
  content: Mapped[str]
  published: Mapped[bool] = mapped_column(server_default='TRUE')
  created_at: Mapped[datetime] = mapped_column(server_default=text('now()'))