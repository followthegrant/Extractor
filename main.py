import csv
import os
from bs4 import BeautifulSoup as bs



dir = 'data/papers/nature-com/american-journal-of-gastroenterology'
for filename in os.listdir(dir):
    print(filename)

    with open(dir +'/'+ filename,'r') as file:
        soup = bs(file, 'lxml')
        print(soup.text)