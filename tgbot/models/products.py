from sqlalchemy import Column, BigInteger, String, Integer, DateTime, func, select, insert, update
from sqlalchemy.orm import sessionmaker

from tgbot.services.db_base import Base


class Product(Base):
    __tablename__ = "product"

    item_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(length=50))
    description = Column(String(length=600))
    price = Column(BigInteger)
    quantity = Column(Integer, default=1)
    url_img = Column(String(250))
    created_at = Column(DateTime(True), server_default=func.now())

    @classmethod
    async def get_product(cls, session_maker: sessionmaker, item_id: int) -> 'Product':
        async with session_maker() as db_session:
            sql = select(cls).where(cls.item_id == item_id)
            request = await db_session.execute(sql)
            user: cls = request.scalar()
        return user

    @classmethod
    async def get_all_product(cls, session_maker: sessionmaker, query: str, offset: int):
        async with session_maker() as db_session:
            if query:
                sql = select(cls).filter(
                    func.lower(cls.name).like(f'%{query.lower()}%')).order_by(cls.name).offset(offset).limit(20)
            else:
                sql = select(cls).order_by(cls.name).offset(offset).limit(20)
            request = await db_session.execute(sql)
            product: cls = request.scalars()
        return product

    @classmethod
    async def add_product(cls,
                          session_maker: sessionmaker,
                          name: str,
                          description: str,
                          price: int,
                          url_img: str) -> 'Product':
        async with session_maker() as db_session:
            sql = insert(cls).values(name=name,
                                     description=description,
                                     price=price,
                                     url_img=url_img).returning('*')
            result = await db_session.execute(sql)
            await db_session.commit()
            return result.first()

    @classmethod
    async def update_product(cls, session_maker: sessionmaker, item_id: int, updated_fields: dict) -> 'Product':
        async with session_maker() as db_session:
            sql = update(cls).where(cls.item_id == item_id).values(**updated_fields)
            result = await db_session.execute(sql)
            await db_session.commit()
            return result

    def __repr__(self):
        return f'Product (ID: {self.item_id} - {self.name})'
