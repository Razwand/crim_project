#!/usr/bin/env python

__author__ = "Alicia Sánchez R."

import requests
from bs4 import BeautifulSoup
import urllib
import string
from os import path
import random

def read_sub_page(url_m, path_folder_img):

    '''
    From the single profile url:
    TRY:
    - Read html looking for container id
    - Filter by 'image' class
    - find 'img'
    - Save image in selected path with name refering to the profile name
    IF NOT:
    - Img saving has not been possible and print out the name of the profile that hasn't been scrapped

    '''

    try:
        subpage = requests.get(url_m)
        subsoup = BeautifulSoup(subpage.content, 'html.parser')
        results_subpage = subsoup.find_all(id="container")
        job_elems = results_subpage[0].find('div', class_='image')
        img_elem = job_elems.findAll('img')
        url_img = img_elem[0]['data-src'] 
        urllib.request.urlretrieve(url_img, path_folder_img + url_img.split('/')[-1])
    except:
        print('NOT SAVED: ',url_m)
  

def read_details(job_el,path_folder_img):

    '''
    For each element (from index 1 as first position stores the table tittle):
    - Name extraction
    - Look for 'more' class
    - href filter to take url from single profile
    - read page extracted in the previous step

    '''
    
    for i in range(1,len(job_el)):
        name_murder = job_el[i].find('div', class_='name')
        more = name_murder.find_all('a', class_='more')
        url_murder = more[0].get('href')
        read_sub_page(url_murder, path_folder_img)


def read_murder_browser(gender_selected,letter,country):

    'Bulding queries for search'

    url_root = 'https://criminalia.es/resultados-de-la-busqueda/'
    if letter is None:
         query = '?g=' + gender_selected + '&c='+ country
    else:
         query = '?l='+letter+'&g=' + gender_selected
    url = url_root + query
    return(url)

def give_me_imgs(gender_selected, path_folder_img, letters_list):
    '''
    Letter by letter the following steps will be taken:
    - Build url searching by gender & letter
    - Parse html filtering by id=content
    - Extract all block elements in a list job_elems
    - read details from the table of all elements of the page search.
    '''
    print('🔍 Searching for results considering letters: ', letters_list)
    for t in range(0, len(letters_list)):
        url = read_murder_browser(gender_selected,letters_list[t], None)
        print('🌐 URL: ',url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all(id="content")
        job_elems = results[0].find_all('li', class_='block')
        read_details(job_elems,path_folder_img)

def take_args():
    '''
    Preparing process taking arguments and selecting letter list for searching
    '''
    gender = input('Gender (M/W): ')
    while gender not in ['W','M']:
        print('🤔 Please select valid gender')
        gender = input('Gender (M/W): ')
    if gender == 'M':
        gender_selected = 'hombre'
    else:
        gender_selected = 'mujer'

    path_folder_img = input('Folder to store images: ')
    while path.exists(path_folder_img) is False:
        print(' 🤔 Please select valid path')
        path_folder_img = input('Folder to store images: ')  
    print('Images will be stored in: {}'.format(path_folder_img))

    n = int(input('Number of letters for searching: '))
    while n not in range(0,27):
        print('Enter a number between  1 and 26  or set to 0 to get all')
        n = int(input('Number of letters for searching: '))
    
    letters_list = list(string.ascii_lowercase)
    if n != 0:
        letters_list = random.sample(letters_list, n)
    return(gender_selected, path_folder_img, letters_list )

def main():

    '''
    Main flow starting with parameter 'Gender' and path where the images will be stored.
    Also, if user doesn't want to obtain the search results for all letter n random letters will be considered.
    '''
    gender_selected, path_folder_img, letters_list = take_args()
    
    give_me_imgs(gender_selected, path_folder_img, letters_list)

    print('-------------------------')
    print('🙃 Images have been stored in {}'.format(path_folder_img))
    print('-------------------------')

if __name__ == "__main__":
    main()



