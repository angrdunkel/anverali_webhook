import requests
import json
import psycopg2

class DataBase():
    def connect_db(self):
        return psycopg2.connect(dbname='dbname', user='user', password='password', host='host')
    
    def get_gender(self, data):
        #ищем в таблицах имя и определяем гендер
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT (*) FROM male WHERE name='{data['name']}';")
        check = cursor.fetchone()
        if check[0] != 0:
            return {
                'id': data['id'],
                'gender': 'male'
            }
        cursor.execute(f"SELECT COUNT (*) FROM female WHERE name='{data['name']}';")
        check = cursor.fetchone()
        if check[0] != 0:
            return {
                'id': data['id'],
                'gender': 'female'
            }
        return False

class Utils():
    def get_request(self, url):
        return requests.get(url)
    
    def post_request(self, url, data):
        return requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

class Main(Utils, DataBase): 
    def __init__(self):
        #адрес webhook
        url = 'https://example.com/webhook'
        #получаем данные для сравнения
        get_data = self.get_request(url).json()
        #получаем гендер
        gender = self.get_gender(get_data)
        #если ксть имя отправляем гендер и id
        if gender:
            post_data = self.post_request(url, get_data)
        else:
            print(f'{get_data['name']} no matches')

main = Main()

if __name__ == '__main__':
    main