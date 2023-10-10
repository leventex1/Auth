from service import db
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from service.utils.expiration import get_expiration_refresh_token

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    refresh_token: Mapped['RefreshToken'] = relationship(back_populates='user')

class RefreshToken(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, nullable=True, default=None)
    valid_until: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None, onupdate=get_expiration_refresh_token)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='refresh_token')
