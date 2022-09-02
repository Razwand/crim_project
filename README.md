# 🕵 Criminalia Scrapping with BeautifulSoup 🥣	

# About

This tool scraps data from web https://criminalia.es/ in order to obtain:

- Image data of the scrapped profiles
- Text data of the scrapped profiles

## 👤 Scrapping Images

This module scrapps images from all the listed profiles. 
Profile Images and Data can be downloaded choosing between man/woman profiles and the folder where they will be stored.
Also, in order to perform a smaller search, there's an option to perform a search considering just a few random letters (corresponding to surname search).

### Sample




### Usage

## 🖋 Scrapping Text

Scrapps data from the profiles. This data can be searched with filter man/woman and in order to perform a smaller search, 
there's an option to perform a search considering just a few random letters (corresponding to surname search).
This data is returned as a .csv file with the following variables:

| Feature             | Values                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Class | Murder, Serial Killer, Homicide, etc.|
| Subclass | Parricide, etc. |
| Sentence | Death penalty, years of prison, etc. To be processed. |
| Location| State/Country |
| Victims| Number of victims |
|Date|Date of the crime|
|Detention|Date of the detention|
|Victim Profile| Male/Female, age and other details to be processed|

### Sample
![Alt text]('./imgs/profile.PNG' "Optional title")




### Usage