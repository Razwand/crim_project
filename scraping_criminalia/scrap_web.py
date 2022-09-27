#!/usr/bin/env python

__author__ = "Alicia Sánchez R."

import requests
from bs4 import BeautifulSoup
import urllib
import string
import os
import pandas as pd
import itertools

# TEXT SCRAPPING

def read_sub_page_text(url_m,classif,condena,loc,subclass,victims,date,deten,victimprof):

    '''
    Extract from each profile the required data filtering by id container, class text and later class dd
    Note: class dd is the same for all the string data. Knowing the structure and the data that is always inside this string (not all the data is always shown)
    some characters are deleted and the string becomes a list of variable values that will be stored in variables classif,condena,loc,subclass,victims,date,deten and victimprof
    '''

    subpage = requests.get(url_m)
    subsoup = BeautifulSoup(subpage.content, 'html.parser')
    results_subpage = subsoup.find_all(id="container")
    job_elems = results_subpage[0].find('div', class_='text')
    job_elems_ = job_elems.findAll('span', class_='dd')
    l = []
    for ele in job_elems_:
        ele = str(ele).replace('<span ','')
        ele = ele.replace('</span>','')
        ele = ele.replace('class="dd">','')
        l.append(ele)


    for t in range(-2,6):
        if l[t]=='':
            l[t]='NA'

    classif.append(l[0])
    subclass.append(l[1])
    condena.append(l[-1])
    loc.append(l[-2])
    victims.append(l[2])
    date.append(l[3])
    deten.append(l[4])
    victimprof.append(l[5])

    return(classif,condena,loc,subclass,victims,date,deten,victimprof)
 
def read_details_text(job_el, actual_profile_processed, n):
    '''
    Read variables from each profile in the gender-letter list of profiles that corresponds to the built url
    '''
    classif = []
    condena = []
    loc = []
    subclass = []
    victims = []
    date = []
    deten = []
    victimprof = []

    number_to_process = len(job_el) -1

    if number_to_process+ actual_profile_processed > n:
        number_to_process = (n - actual_profile_processed) 

    for i in range(1,number_to_process+1):
        name_murder = job_el[i].find('div', class_='name')
        more = name_murder.find_all('a', class_='more')
        url_murder = more[0].get('href')
        classif,condena,loc,subclass,victims,date,deten,victimprof = read_sub_page_text(url_murder,classif,condena,loc,subclass,victims,date,deten,victimprof)

    return(classif,condena,loc,subclass,victims,date,deten,victimprof, number_to_process)


def give_me_text(gender_selected, n):
    '''
    - Store each scrapped variable in a list that will serve later as a dataframe column
    - For each letter the scrapping process goes:
        - read_murder_browser in order to get a group of profiles (gender and letter) url
        - Read html
        - Read content id and block class
        - Read each single variable with read_details and store them in their list
    - Build a dataframe and store it as .csv file
    '''

    df = pd.DataFrame()
    
    classif_l,condena_l,loc_l,subclass_l,victims_l,date_l,deten_l,victimprof_l = [],[],[],[],[],[],[],[]

    return_warning = 0
    abc = list(string.ascii_lowercase)

    count_profiles = 0
    letter = 0
    while count_profiles <n:
        if letter < len(abc):
            url = read_murder_browser(gender_selected,abc[letter],None)

            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find_all(id="content")
            job_elems = results[0].find_all('li', class_='block')

            classif,condena,loc,subclass,victims,date,deten,victimprof,number_processed =read_details_text(job_elems,count_profiles, n)

            letter +=1
            count_profiles += number_processed

            classif_l.append(classif)
            condena_l.append(condena)
            loc_l.append(loc)
            subclass_l.append(subclass)
            victims_l.append(victims)
            date_l.append(date)
            deten_l.append(deten)
            victimprof_l.append(victimprof)
        else:
            return_warning = 1
            count_profiles = n

    df['Class'] = list(itertools.chain.from_iterable(classif_l))
    df['Subclass'] = list(itertools.chain.from_iterable(subclass_l))
    df['Condena'] = list(itertools.chain.from_iterable(condena_l))
    df['Location'] = list(itertools.chain.from_iterable(loc_l))
    df['Victims'] = list(itertools.chain.from_iterable(victims_l))
    df['Date murder'] = list(itertools.chain.from_iterable(date_l))
    df['Date Detention'] = list(itertools.chain.from_iterable(deten_l))
    df['Victim Profile'] = list(itertools.chain.from_iterable(victimprof_l))


    df.to_csv('./output_text/result_table.csv', index=False, encoding='utf-8')

    return(return_warning)

# IMAGE SCRAPPING
def read_sub_page_img(url_m, path_folder_img):

    '''
    From the single profile url:
    TRY:
    - Read html looking for container id
    - Filter by 'image' class
    - find 'img'
    - Save image in selected path with name referring to the profile name
    IF NOT:
    - Img saving has not been possible and printing out the name of the profile that hasn't been scrapped

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

def read_details_img(job_el,path_folder_img, n,actual_number_scrapped):

    '''
    For each element (from index 1 as first position stores the table tittle):
    - Name extraction
    - Look for 'more' class
    - href filter to take a url from a single profile
    - read page extracted in the previous step

    '''

    number_to_process = len(job_el) -1

    if number_to_process+ actual_number_scrapped > n:
        number_to_process = (n - actual_number_scrapped) 

    for i in range(1,number_to_process+1):
        name_murder = job_el[i].find('div', class_='name')
        more = name_murder.find_all('a', class_='more')
        url_murder = more[0].get('href')
        read_sub_page_img(url_murder, path_folder_img)


    return(number_to_process)

def give_me_imgs(gender_selected, path_folder_img, n):
    '''
    Letter by letter, the following steps will be taken:
    - Build url searching by gender & letter
    - Parse html filtering by id=content
    - Extract all block elements from a list job_elems
    - read details from the table of all elements of the page search.
    '''
    return_warning = 0
    abc = list(string.ascii_lowercase)[:1]

    count_profiles = 0
    letter = 0
    while count_profiles <n:
        if letter < len(abc):
                url = read_murder_browser(gender_selected,abc[letter], None)
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                results = soup.find_all(id="content")
                job_elems = results[0].find_all('li', class_='block')
                number_processed = read_details_img(job_elems,path_folder_img,n, count_profiles)
                letter +=1
                count_profiles += number_processed
        else:
            return_warning = 1
            count_profiles = n

    return(return_warning)

# COMMON
def read_murder_browser(gender_selected,letter,country):

    '''
    Builds the url from parameters letter and gender
    '''

    url_root = 'https://criminalia.es/resultados-de-la-busqueda/'
    if letter is None:
         query = '?g=' + gender_selected + '&c='+ country
    else:
         query = '?l='+letter+'&g=' + gender_selected
    url = url_root + query
    return(url)

def take_args():
    '''
    Preparing process by checking arguments 
    '''
    gender = input('Gender (M/W): ')
    while gender not in ['W','M']:
        print('\U0001F914 Please select a valid gender')
        gender = input('Gender (M/W): ')
    if gender == 'M':
        gender_selected = 'hombre'
    else:
        gender_selected = 'mujer'
   
    n = int(input('Number of profiles to scrap: '))

    mode = input('MODE (IMG/TEXT): ')
    while mode not in ['IMG','TEXT']:
        print('\U0001F914 Please select a valid mode (IMG/TEXT)')
        mode = input('MODE (IMG/TEXT): ')
    
    return(gender_selected, n , mode)

def prepare_folders(mode):
    if mode == 'IMG':
        path_folder = './output_img/'
        if  os.path.exists(path_folder)==False:
            os.mkdir(path_folder)
    elif mode == 'TEXT':
        path_folder = './output_text/'
        if  os.path.exists(path_folder)==False:
            os.mkdir(path_folder)

    return(path_folder)
       
def main():

    '''
    Main flow starts with the parameter 'Gender'.
    Also, users must specify how many profiles to scrap with the parameter 'n'.
    '''
    gender_selected,n,mode = take_args()
    
    path_folder = prepare_folders(mode)

    if mode == 'IMG':
    
        warning = give_me_imgs(gender_selected, path_folder, n)

        if warning == 1:
            print('You asked for more profiles than the ones  available! Check all the available results in  {}'.format(path_folder))

        print('-------------------------')
        print('\U0001F643 Images have been stored in {}'.format(path_folder))
        print('-------------------------')

    elif mode == 'TEXT':
        
        warning = give_me_text(gender_selected, n)

        if warning == 1:
            print('You asked for more profiles than the ones  available! Check all the available results in {}'.format(path_folder))
        
        print('-------------------------')
        print('\U0001F643 Table has been stored in {}'.format(path_folder))
        print('-------------------------')

if __name__ == "__main__":
    main()



