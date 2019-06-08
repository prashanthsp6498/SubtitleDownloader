#! /usr/bin/python3
import os
import requests
import sys
from bs4 import BeautifulSoup

try:
    url = "https://opensubtitles.co/search?q="
    movie_name = input("Enter movie name: ")
    if movie_name == '':
        print("Input is not given")
        sys.exit(0)
    try:
        resp = requests.get(url+movie_name.replace(' ', '+'))
    except Exception as e:
        print(e)
    soup = BeautifulSoup(resp.text, 'lxml')
    movie_links = soup.find_all('a', class_="list-group-item")
    count = 0
    if len(movie_links) == 0:
        print("No result found")
        sys.exit()

    for link in movie_links:
        print("[", count, "] ", link['href'].split('/')[-1])
        count += 1

    choice = int(input("choice: "))
    if choice > count:
        print("Invalid choice")
        sys.exit()

    movie_name = movie_links[choice]['href'].split('/')[-1]

    try:
        resp = requests.get(movie_links[choice]['href'])
    except Exception as e:
        print(e)

    soup = BeautifulSoup(resp.text, 'lxml')
    link = soup.find('ul', class_="list-group").a['href']

    try:
        resp = requests.get(link)
    except Exception as e:
        print(e)

    soup = BeautifulSoup(resp.text, 'lxml')
    sub_link = soup.find('a', class_='btn btn-danger')['href']
    full_link = 'https://opensubtitles.co' + sub_link

    try:
        resp = requests.get(full_link)
    except Exception as e:
        print(e)

    with open(movie_name+".srt", "wb") as fo:
        fo.write(resp.content)
        print(movie_name, " subtitle downloaded in ", os.getcwd())

except Exception:
    print("Bye")
