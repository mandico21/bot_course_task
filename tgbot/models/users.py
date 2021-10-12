from typing import Optional, List

from sqlalchemy import Column, BigInteger, insert, String, ForeignKey, update, func, Boolean, DateTime
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from tgbot.services.db_base import Base


class User(Base):
    __tablename__ = "telegram_users"

    telegram_id: int = Column(BigInteger, primary_key=True)
    full_name = Column(String(length=100))
    username = Column(String(length=100), nullable=True)
    invite_code = Column(String(length=5), default=None)
    balance = Column(BigInteger, default=0)
    passed = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    created_at = Column(DateTime(True), server_default=func.now())
    updated_at = Column(DateTime(True), default=func.now(), onupdate=func.now(), server_default=func.now())

    @classmethod
    async def get_user(cls, session_maker: sessionmaker, telegram_id: int) -> 'User':
        async with session_maker() as db_session:
            sql = select(cls).where(cls.telegram_id == telegram_id)
            request = await db_session.execute(sql)
            user: cls = request.scalar()
        return user

    @classmethod
    async def get_user_code(cls, session_maker: sessionmaker, invite_code: str) -> 'User':
        async with session_maker() as db_session:
            sql = select(cls).where(cls.invite_code == invite_code)
            request = await db_session.execute(sql)
            user: cls = request.scalar()
        return user

    @classmethod
    async def get_all_user(cls, session_maker: sessionmaker, query: str) -> List['User']:
        async with session_maker() as db_session:
            if query:
                sql = select(cls).filter(
                    func.lower(cls.full_name).like(f'%{query.lower()}%')).order_by(cls.full_name)
            else:
                sql = select(cls).order_by(cls.full_name)
            request = await db_session.execute(sql)
            user: cls = request.scalars()
        return user\

    @classmethod
    async def get_users(cls, session_maker: sessionmaker) -> 'User':
        async with session_maker() as db_session:
            sql = select(cls.telegram_id)
            request = await db_session.execute(sql)
            user: cls = request.scalars()
        return user.all()

    @classmethod
    async def add_user(cls,
                       session_maker: sessionmaker,
                       telegram_id: int,
                       full_name: str,
                       username: str = None) -> 'User':
        async with session_maker() as db_session:
            sql = insert(cls).values(telegram_id=telegram_id,
                                     full_name=full_name,
                                     username=username).returning('*')
            result = await db_session.execute(sql)
            await db_session.commit()
            return result.first()

    async def update_user(self, session_maker: sessionmaker, updated_fields: dict,
                          telegram_id: Optional = None) -> 'User':
        telegram_id = self.telegram_id if not telegram_id else telegram_id
        async with session_maker() as db_session:
            sql = update(User).where(User.telegram_id == telegram_id).values(**updated_fields)
            result = await db_session.execute(sql)
            await db_session.commit()
            return result

    @classmethod
    async def count_referrals(cls, session_maker: sessionmaker, user: "User"):
        async with session_maker() as db_session:
            sql = select(
                func.count(Referral.telegram_id)
            ).where(
                Referral.referrer == user.telegram_id
            ).join(
                User
            ).group_by(
                Referral.referrer
            )
            result = await db_session.execute(sql)
            return result.scalar()

    def __repr__(self):
        return f'User (ID: {self.telegram_id} - {self.full_name} )'


class Referral(Base):
    __tablename__ = "referral_users"
    telegram_id = Column(BigInteger, primary_key=True)
    referrer = Column(ForeignKey(User.telegram_id, ondelete='CASCADE'))

    @classmethod
    async def add_user(cls,
                       db_session: sessionmaker,
                       telegram_id: int,
                       referrer: int
                       ) -> 'User':
        async with db_session() as db_session:
            sql = insert(cls).values(
                telegram_id=telegram_id,
                referrer=referrer
            )
            result = await db_session.execute(sql)
            await db_session.commit()
            return result
