import requests
from bs4 import BeautifulSoup
import urllib
import string
from os import path


def read_sub_page(url_m, path_folder_img):

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
    
    for i in range(1,len(job_el)):
        name_murder = job_el[i].find('div', class_='name')
        more = name_murder.find_all('a', class_='more')
        url_murder = more[0].get('href')
        read_sub_page(url_murder, path_folder_img)


def read_murder_browser(gender_selected,letter,country):

    url_root = 'https://criminalia.es/resultados-de-la-busqueda/'

    if letter is None:
         query = '?g=' + gender_selected + '&c='+ country
    else:
         query = '?l='+letter+'&g=' + gender_selected

    url = url_root + query

    return(url)

def main():
    
    gender_selected = input('Gender (hombre o mujer): ')
    while gender_selected not in ['hombre','mujer']:
        print('Please select valid gender')
        gender_selected = input('Gender (hombre o mujer): ')

    path_folder_img = input('Folder to store images: ')
    while path.exists(path_folder_img) is False:
        print('Select valid path')
        path_folder_img = input('Folder to store images: ')  
    print('Images will be stored in: {}'.format(path_folder_img))

    letters_list = list(string.ascii_lowercase)
    for t in range(0, len(letters_list)):
        url = read_murder_browser(gender_selected,letters_list[t], None)
        print('URL ',url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all(id="content")
        job_elems = results[0].find_all('li', class_='block')
        read_details(job_elems,path_folder_img)

if __name__ == "__main__":
    main()



