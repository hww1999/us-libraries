import re
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import csv

headers = {''}

def scrape(filename, url, idx):
    
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    res = res.text

    p_strong = '<strong>.*?</strong>'
    try:
        p_name = '<span itemprop="legalName">\r\n.*?</span>'
        legal_name = re.findall(p_name, res, re.S)[0].replace('\r\n','')
        legal_name = legal_name.split('>')[1].split('<')[0]
    except IndexError:
        return
    
    try:
        p_region = '<span itemprop="addressRegion">\r\n.*?<'
        region = re.findall(p_region, res, re.S)
        region = region[0].replace('\r\n','').split('>')[1].split('<')[0]
    except IndexError:
        region = None

    try:
        p_streetAddress = '<span itemprop="streetAddress">\r\n.*?<'
        streetAddress = re.findall(p_streetAddress, res, re.S)
        streetAddress = streetAddress[0].replace('\r\n','').split('>')[1].split('<')[0]
    except IndexError:
        streetAddress = None

    try:
        p_addressLocality = '<span itemprop="addressLocality">\r\n.*?<'
        addressLocality = re.findall(p_addressLocality, res, re.S)
        addressLocality = addressLocality[0].replace('\r\n','').split('>')[1].split('<')[0]
    except IndexError:
        addressLocality = None

    try:
        p_postalCode = '<span itemprop="postalCode" >\r\n .*?<'
        postalCode = re.findall(p_postalCode, res, re.S)
        postalCode = postalCode[0].replace('\r\n','').split('>')[1].split('<')[0]
    except IndexError:
        postalCode = None

    try:
        p_country = '<span itemprop="addressCountry">\r\n.*?<'
        addressCountry = re.findall(p_country, res, re.S)
        addressCountry = addressCountry[0].replace('\r\n','').split('>')[1].split('<')[0]
    except IndexError:
        addressCountry = None

    try:
        p_county = 'County=.*?</strong>'
        county = re.findall(p_county, res, re.S)
        county = re.findall(p_strong, county[0], re.S)[0]
        county = re.sub('<.*?>','',county) #.replace('<strong>','').replace('</strong>','')
    except IndexError:
        county = None

    try:
        p_tele = '<span itemprop="telephone">.*?</span>'
        tele = re.findall(p_tele, res, re.S)[0].replace('\r\n','').split('>')[1].split('<')[0]
    except IndexError:
        tele = None 

    try:
        p_academic = 'Academic Level.*?</p>'
        aca = re.findall(p_academic, res, re.S)
        aca_info = re.findall(p_strong, aca[0], re.S) 
        aca_info = ';'.join(aca_info)
        aca_info = re.sub('<.*?>','',aca_info)
    except IndexError:
        aca_info = None

    try:
        p_structure = 'Organizational structure:.*?</p>'
        structure = re.findall(p_structure, res, re.S)
        structure_info = re.findall(p_strong, structure[0], re.S) 
        structure_info = ';'.join(structure_info)
        structure_info = re.sub('<.*?>','',structure_info)
    except IndexError:
        structure_info = None

    try:
        p_details = '<span itemprop="description">.*?</span>'
        details = re.findall(p_details, res, re.S)[0].replace('\r\n','')
        details = re.sub('<.*?>', '', details)
        details = re.sub(r'\([^)]*\)', '', details)
        details = re.sub(' +', ' ', details)
    except IndexError:
        details = None
    if details:
        try:
            p_vol = 'contains .*? volumes'
            volume = re.findall(p_vol, details, re.S)[0].split()[1]
        except:
            volume = None
        try:
            p_cir = 'circulates .*? items'
            circulation = re.findall(p_cir, details, re.S)[0].split()[1]
        except:
            circulation = None
        try:
            p_fte = 'population of .*? FTE'
            fte = re.findall(p_fte, details, re.S)[0].split()[2]
        except:
            fte = None

    rs.append({'Libraries.org ID': str(idx),
               'Legal Name': legal_name,
               'Country': addressCountry,
               'County': county,
               'Region': region,
               'Postal Code': postalCode,
               'Street Address': streetAddress,
               'Address Locality': addressLocality,
               'Telephone': tele,
               'Acacemic Level': aca_info,
               'Organizational structure': structure_info,
               'Volumes Contained': volume,
               'Circulations Per Year': circulation,
               'Full-time Equivalent (FTE) Enrollment': fte,
               'Details': details})
    

def export(libraries, filename):

    file = open(filename+'.csv', 'w', newline ='', encoding="utf-8")
    with file:
        header = ['Libraries.org ID', 'Legal Name', 'Country', 'County', 'Region', 'Postal Code', 
                  'Street Address', 'Address Locality', 'Telephone', 'Acacemic Level',
                  'Organizational structure', 'Volumes Contained', 'Circulations Per Year', 
                  'Full-time Equivalent (FTE) Enrollment', 'Details']
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        for library in libraries:
            writer.writerow(library)  

def update(libraries, filename):

    file = open(filename+'.csv', 'a', newline ='', encoding="utf-8")
    with file:
        header = ['Libraries.org ID', 'Legal Name', 'Country', 'County', 'Region', 'Postal Code', 
                  'Street Address', 'Address Locality', 'Telephone', 'Acacemic Level',
                  'Organizational structure', 'Volumes Contained', 'Circulations Per Year', 
                  'Full-time Equivalent (FTE) Enrollment', 'Details']
        writer = csv.DictWriter(file, fieldnames = header)
        # writer.writeheader()
        for library in libraries:
            writer.writerow(library)          


if __name__ == '__main__':
    rs = []

    # for i in range(1,100): # 250000
        
    #     test_url = 'https://librarytechnology.org/library/' + str(i)
    #     try:
    #         scrape('library', test_url, i)
    #     except IndexError:
    #         print(str(i) + ': IndexError')
    #         pass
    # export(rs, 'US Libraries')

    for i in range(211500, 212000):
        rs = []
        test_url = 'https://librarytechnology.org/library/' + str(i)
        try:
            scrape('library', test_url, i)
        except IndexError:
            print(str(i) + ': IndexError')
            pass
        # export(rs, 'US Libraries')
    update(rs, 'US Libraries')
        