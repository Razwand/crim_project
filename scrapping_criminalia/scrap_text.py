#!/usr/bin/env python
__author__ = "Alicia SR."

import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
import itertools
import random

def read_sub_page(url_m,classif,condena,loc,subclass,victims,date,deten,victimprof):

    '''
    Extract from each profile the required data filtering by id container, class text and later class dd
    Note: class dd is the same for all the string data. Knowing the structure and the data that is always inside this string (not all the data is allways shown)
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
            l[t]=='NA'

    classif.append(l[0])
    subclass.append(l[1])
    condena.append(l[-1])
    loc.append(l[-2])
    victims.append(l[2])
    date.append(l[3])
    deten.append(l[4])
    victimprof.append(l[5])

    return(classif,condena,loc,subclass,victims,date,deten,victimprof)
 
def read_details(job_el):
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
    for i in range(1,len(job_el)):
        name_murder = job_el[i].find('div', class_='name')
        more = name_murder.find_all('a', class_='more')
        url_murder = more[0].get('href')
        classif,condena,loc,subclass,victims,date,deten,victimprof = read_sub_page(url_murder,classif,condena,loc,subclass,victims,date,deten,victimprof)

    return(classif,condena,loc,subclass,victims,date,deten,victimprof)

def read_murder_browser(gender_selected,letter,country):

    '''
    Build url from parameters letter and gender
    '''

    url_root = 'https://criminalia.es/resultados-de-la-busqueda/'
    if letter is None:
         query = '?g=' + gender_selected + '&c='+ country
    else:
         query = '?l='+letter+'&g=' + gender_selected
    url = url_root + query
    return(url)

def give_me_data(gender_selected, letters_list,name_file):
    '''
    - Store each scrapped variable in a list that will serve later as a dataframe column
    - For each letter the scrapping process goes:
        - read_murder_browser in order to get group of profiles (gender and letter) url
        - Read html
        - Read content id and block class
        - Read each single variable with read_details and store them in their list
    - Build dataframe and store it as .csv file
    '''

    df = pd.DataFrame()
    print('Searching for results considering letters', letters_list)
    classif_l,condena_l,loc_l,subclass_l,victims_l,date_l,deten_l,victimprof_l = [],[],[],[],[],[],[],[]

    for t in range(0, len(letters_list)):
        url = read_murder_browser(gender_selected,letters_list[t],None)
        print('🌐 URL: ',url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all(id="content")
        job_elems = results[0].find_all('li', class_='block')

        classif,condena,loc,subclass,victims,date,deten,victimprof=read_details(job_elems)
        classif_l.append(classif)
        condena_l.append(condena)
        loc_l.append(loc)
        subclass_l.append(subclass)
        victims_l.append(victims)
        date_l.append(date)
        deten_l.append(deten)
        victimprof_l.append(victimprof)

    df['Class'] = list(itertools.chain.from_iterable(classif_l))
    df['Subclass'] = list(itertools.chain.from_iterable(subclass_l))
    df['Condena'] = list(itertools.chain.from_iterable(condena_l))
    df['Location'] = list(itertools.chain.from_iterable(loc_l))
    df['Victims'] = list(itertools.chain.from_iterable(victims_l))
    df['Date murder'] = list(itertools.chain.from_iterable(date_l))
    df['Date Detention'] = list(itertools.chain.from_iterable(deten_l))
    df['Victim Profile'] = list(itertools.chain.from_iterable(victimprof_l))

    #print(df)

    df.to_csv('./Data/'+ name_file + '.csv', index=False, encoding='utf-8')

    print('-------------------------')
    print('🙃 Data have been stored in {}'.format(name_file + '.csv'))
    print('-------------------------')


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

    n = int(input('Number of letters for searching: '))
    while n not in range(0,27):
        print('Enter a number between  1 and 26  or set to 0 to get all')
        n = int(input('Number of letters for searching: '))

    letters_list = list(string.ascii_lowercase)
    if n != 0:
        letters_list = random.sample(letters_list, n)

    if gender_selected == 'mujer':
        name_file = 'Data_Woman'
    else:
        name_file = 'Data_Man'

    return(gender_selected, letters_list ,name_file)


def main():

    '''
    Select Gender to scrapp profile data.
    '''

    gender_selected, letters_list, name_file = take_args()

    give_me_data(gender_selected, letters_list,name_file)


if __name__ == "__main__":
    main()



