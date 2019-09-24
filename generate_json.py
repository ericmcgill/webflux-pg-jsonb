import json
import random
import psycopg2
import os

DB_NAME=os.environ['DB_NAME']
DB_USERNAME=os.environ['DB_USERNAME']
DB_PASSWORD=os.environ['DB_PASSWORD']
DB_HOST=os.environ['DB_HOST']
DB_PORT=os.environ['DB_PORT']



conn = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

def get_random_word():
    words = ["Adult", "Aeroplane", "Air", "Aircraft Carrier", "Airforce", "Airport", "Album", "Alphabet", "Apple", "Arm", "Army", "Baby", "Baby", "Backpack", "Balloon", "Banana", "Bank", "Barbecue", "Bathroom", "Bathtub", "Bed", "Bed", "Bee", "Bible", "Bible", "Bird", "Bomb", "Book", "Boss", "Bottle", "Bowl", "Box", "Boy", "Brain", "Bridge", "Butterfly", "Button", "Cappuccino", "Car", "Car-race", "Carpet", "Carrot", "Cave", "Chair", "Chess Board", "Chief", "Child", "Chisel", "Chocolates", "Church", "Church", "Circle", "Circus", "Circus", "Clock", "Clown", "Coffee", "Coffee-shop", "Comet", "Compact Disc", "Compass", "Computer", "Crystal", "Cup", "Cycle", "Data Base", "Desk", "Diamond", "Dress", "Drill", "Drink", "Drum", "Dung", "Ears", "Earth", "Egg", "Electricity", "Elephant", "Eraser", "Explosive", "Eyes", "Family", "Fan", "Feather", "Festival", "Film", "Finger", "Fire", "Floodlight", "Flower", "Foot", "Fork", "Freeway"]
    return random.choice(words)

def get_number_of_sentences(size_in_mb, example_sentence):
    return int((size_in_mb * 1024 * 1024) / len(example_sentence))

def get_array_of_sentences(number_of_sentences):
    array_of_sentences = []

    for _ in range(number_of_sentences):
        sentence = f"This is my {get_random_word()}"
        array_of_sentences.append(sentence)
    
    return array_of_sentences

def get_payload(aos):
    d = {}
    d['sentences'] = aos
    d['last_item'] = "Yo"
    return d

number_of_records = 20
cur = conn.cursor()

sql = f"TRUNCATE TABLE my_json_table;"
cur.execute(sql)

for i in range(int(number_of_records+1)):
    example_sentence = f"This is my {get_random_word()}"
    n = get_number_of_sentences(random.choice([1,2,3,4,5,6,7]), example_sentence)
    a = get_array_of_sentences(n)
    p = get_payload(a)
    s = json.dumps(p)
    sql = f"INSERT INTO my_json_table (id, my_json) VALUES ({i}, '{s}');"
    cur.execute(sql)

conn.commit()