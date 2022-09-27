# 🕵 Criminalia Scrapping with BeautifulSoup 🥣	

# About

This tool scraps data from the website https://criminalia.es/ in order to obtain:

- Image data of the scrapped profiles
- Text data of the scrapped profiles

![Flow](https://github.com/Razwand/scrapping_data_criminalia/blob/main/images/flow_search.PNG)

## Requirements
- A suitable conda environment named scrap can be created and activated with:

```console
conda env create -f environment_scrap.yml
conda activate scrap
```

## 👤 Scrapping Images

This module scraps images from all the listed profiles. 
Profile Images and Data can be downloaded choosing between man/woman profiles and the number of profiles to be processed.

### How to

In the following scenario, the user is searching for 37 men, storing results in a folder named ./output_image/. If the number of profiles to be processed exceeds the total number of profiles, a message will show a message. The maximum number of available profiles will be returned in this case.

```console
scrapping_criminalia>python scrap_web.py
>>Gender (M/W): M
>>Number of profiles to scrap: 37
>>MODE (IMG/TEXT): IMG
```


![Result_1](https://github.com/Razwand/scrapping_data_criminalia/blob/main/images/result_scrap_img.PNG)


## 🖋 Scrapping Text

Scraps data from the profiles. This data can be searched with filter man/woman and the number of profiles to be processed.
This data is returned as a .csv in ./output_text/ folder with the following variables:

| Feature             | Values                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Class | Murder, Serial Killer, Homicide, etc.|
| Subclass | Parricide, etc. |
| Sentence | Death penalty, years of prison, etc. * |
| Location| State/Country |
| Victims| Number of victims |
|Date|Date of the crime|
|Detention|Date of the detention|
|Victim Profile| Male/Female, age and other details *|

```diff
- To be processed (More fields could be obtained)
```

### How to

In the following scenario, the user is searching for 5 men. If the number of profiles to be processed exceeds the total number of profiles, a message will show a message. The maximum number of available profiles will be returned in this case.

```console
scrapping_criminalia>python scrap_web.py
>>Gender (M/W): M
>>Number of profiles to scrap: 5
>>MODE (IMG/TEXT): TEXT
```

![Result_2](https://github.com/Razwand/scraping_data_criminalia/blob/main/images/table.PNG)
