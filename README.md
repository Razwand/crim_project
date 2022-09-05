# 🕵 Criminalia Scrapping with BeautifulSoup 🥣	

# About

This tool scraps data from web https://criminalia.es/ in order to obtain:

- Image data of the scrapped profiles
- Text data of the scrapped profiles

![Flow](https://github.com/Razwand/scrapping_data_criminalia/blob/main/images/flow_search.PNG)

## 👤 Scrapping Images

This module scrapps images from all the listed profiles. 
Profile Images and Data can be downloaded choosing between man/woman profiles and the folder where they will be stored.
Also, in order to perform a smaller search, there's an option to perform a search considering just a few random letters (corresponding to surname search).
### How to

In the following scenario user is searching for men, storing results in folder ./Data/ and the searching procedure will consider one random
letter from the search page (corresponding to all profiles with surname begining with that letter).

```console
scrapping_criminalia>python scrap_img.py
>>Gender (M/W): M
>>Folder to store images: ./Data/
>>Number of letters for searching: 1
```


![Result_1](https://github.com/Razwand/scrapping_data_criminalia/blob/main/images/result_scrap_img.PNG)


## 🖋 Scrapping Text

Scrapps data from the profiles. This data can be searched with filter man/woman and in order to perform a smaller search, 
there's an option to perform a search considering just a few random letters (corresponding to surname search).
This data is returned as a .csv file with the following variables:

| Feature             | Values                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Class | Murder, Serial Killer, Homicide, etc.|
| Subclass | Parricide, etc. |
| Sentence | Death penalty, years of prison, etc. |
| Location| State/Country |
| Victims| Number of victims |
|Date|Date of the crime|
|Detention|Date of the detention|
|Victim Profile| Male/Female, age and other details to be processed|

### How to

In the following scenario user is searching for men and the searching procedure will consider one random
letter from the search page (corresponding to all profiles with surname begining with that letter).

```console
scrapping_criminalia>python scrap_text.py
>>Gender (M/W): M
>>Number of letters for searching: 1
```
![Result_2](https://github.com/Razwand/scraping_data_criminalia/blob/main/images/table.PNG)
## Dependencies

- All libraries used are stored in requirements.txt

```console
pip install -r requirements.txt
```
