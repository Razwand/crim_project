# Criminalia Scrapping 

# About

This tool scraps data from web https://criminalia.es/ in order to obtain:

- Image data classified between men and women
- Text data 

## Scrapping Images

This module scrapps images from all the listed profiles. 
Images can be downloaded choosing between man/woman profiles andthe folder where they will be stored.Folders will be separated by gender (woman/man)

## Scrapping Text

Scrapps data from all the listed profiles. 
This data is returned as a .csv file with the following variables:

|Class| Murder, Serial Killer, Homicide, etc.
|Subclass| Parricide, etc.
|Sentence| Death penalty, years of prison, etc. To be processed.
|Location| State/Country
|Victims| Number of victims
|Date|Date of the crime
|Detention| Date of the detention
|Victim Profile| Male/Female, age and other details to be processed