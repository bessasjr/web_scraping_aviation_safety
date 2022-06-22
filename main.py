from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.options import ChromiumOptions
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import math
import numpy as np


lista_anos = list(range(1919, 2022))

lista_ocorrencias = []
lista_paginas = []

lista0 = []
lista1 = []
lista2 = []


print('\033[1mESCOLHA O PERÍODO\033[m')
print()

while True:
    inicial = input('Qual o ano inicial? (entre 1919 e 2021) => ')
    if inicial == '' or inicial.isalpha() or int(inicial) not in lista_anos[:]:
        print('\033[1;31mSELECIONE UM ANO VÁLIDO\n\033[m')
    else:
        break
        
print()

while True:
    final = input('Qual o ano final? (entre 1919 e 2021) => ')
    if final == '' or final.isalpha() or int(final) not in lista_anos[:]:
        print('\033[1;31mSELECIONE UM ANO VÁLIDO\n\033[m')
    elif int(final) < int(inicial):
        print('\033[1;31mO ANO INICIAL NÃO PODE SER POSTERIOR AO ANO FINAL\n\033[m')
    else:
        break
        
print()


for y in range(int(inicial), int(final)+1):
    print('Ano: ', end='')
    print(y,end=', ')

    options = ChromiumOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    navegador = webdriver.Chrome(options=options)
    navegador.get(f'https://aviation-safety.net/database/dblist.php?Year={y}')

    count = 0

    quantidade_paginas = navegador.find_element(by=By.TAG_NAME, value='span'[1])
    if quantidade_paginas.text != '':
        quantidade_paginas1 = quantidade_paginas.text.split(' ')[0]
        quantidade_paginas2 = int(quantidade_paginas1) / 100
        q = math.ceil(quantidade_paginas2)
        print('Ocorrências:', quantidade_paginas1, end=', ')
        print('Páginas:', q)
        lista_ocorrencias.append(int(quantidade_paginas1))
        lista_paginas.append(int(q))
    else:
        q = 1
        
    page_content = navegador.page_source
    site = BeautifulSoup(page_content, 'html.parser')
    elementos = site.findAll('td', attrs={'class':['list','listdata']})

    count = 0
    for a in range(1, q+1, 1):
        
        count = count + 1
   
        sleep(4)    
        for elemento in elementos:
            a = elemento.text.splitlines()
            if a == [] or a == '':
                a = 'NaN'
            lista0.append(a[0])
            img = 'https:'+str(elemento.img)[10:-3]
            if 'country' in img:
                a = img.split('="')[1]
                lista1.append(a)
 

        for i in range(0, len(lista0), 9):
            lista2.append(lista0[i:i+9])
            
        lista0.clear()

        navegador.get(f'https://aviation-safety.net/database/dblist.php?Year={y}&lang=&page={count+1}')
        page_content = navegador.page_source
        site = BeautifulSoup(page_content, 'html.parser')
        elementos = site.findAll('td', attrs={'class':['list','listdata']})
        

print('\nTotal de Ocorrências:', np.sum(lista_ocorrencias), end=', ')
print('Total de Páginas:', np.sum(lista_paginas), '\n')

    
df = pd.DataFrame(lista2, columns=['Date', 'Air_craft_type', 'Registration', 'Operator', 'Fatilites', 'Location', 'Vazio', 'Vazio', 'Category'])

df['Country'] = lista1[:]

df = df[['Date', 'Air_craft_type', 'Registration', 'Operator', 'Fatilites', 'Location', 'Country', 'Category']]

df.Fatilites.replace('N', '', inplace=True)
df.Location.replace('N', '', inplace=True)

df.to_csv('dataframe.csv')
