from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="publisher")

    def __str__(self):
        return f"Publisher(id={self.id}, name={self.name})"


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)
    publisher = relationship("Publisher", back_populates="books")
    stocks = relationship("Stock", back_populates="book")

    def __str__(self):
        return f"Book(id={self.id}, title={self.title}, id_publisher={self.id_publisher})"


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)
    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop")

    def __str__(self):
        return f"Stock(id={self.id}, id_book={self.id_book}, id_shop={self.id_shop}, count={self.count})"


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sales = relationship("Sale", back_populates="shop")

    def __str__(self):
        return f"Shop(id={self.id}, name={self.name})"


class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    date_sale = Column(Date, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False)
    stock = relationship("Stock")

    def __str__(self):
        return f"Sale(id={self.id}, price={self.price}, date_sale={self.date_sale}, id_stock={self.id_stock}, count={self.count})"
