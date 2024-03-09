import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Stock, Shop, Sale


def load_data_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def save_data_to_database(data, session):
    for item in data:
        model_name = item['model']
        fields = item['fields']

        if model_name == 'publisher':
            publisher = Publisher(name=fields['name'])
            session.add(publisher)

        elif model_name == 'book':
            book = Book(title=fields['title'], id_publisher=fields['id_publisher'])
            session.add(book)

        elif model_name == 'shop':
            shop = Shop(name=fields['name'])
            session.add(shop)

        elif model_name == 'stock':
            stock = Stock(id_shop=fields['id_shop'], id_book=fields['id_book'], count=fields['count'])
            session.add(stock)

        elif model_name == 'sale':
            sale = Sale(price=fields['price'], date_sale=fields['date_sale'], count=fields['count'], id_stock=fields['id_stock'])
            session.add(sale)

    session.commit()


def connect_to_database():
    # Получаем значения параметров подключения из переменных окружения
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    # Формируем строку подключения
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def fetch_publisher_books(session, publisher_name):
    publisher = session.query(Publisher).filter_by(name=publisher_name).first()
    if publisher:
        books = session.query(Book).filter_by(id_publisher=publisher.id).all()
        return books
    else:
        return None

def print_purchase_facts(session, books):
    for book in books:
        sales = session.query(Sale).join(Stock).filter(Stock.id_book == book.id).all()
        for sale in sales:
            shop = session.query(Shop).filter_by(id=sale.stock.id_shop).first()
            print(f"{book.title} | {shop.name} | {sale.price} | {sale.date_sale}")

if __name__ == "__main__":

    session = connect_to_database()

    json_file = 'test_data.json'

    data = load_data_from_json(json_file)

    save_data_to_database(data, session)

    print("Данные успешно загружены в базу данных.")

   

    publisher_name = input("Введите имя издателя: ")
    books = fetch_publisher_books(session, publisher_name)
    if books:
        print_purchase_facts(session, books)
    else:
        print("Издатель не найден.")


