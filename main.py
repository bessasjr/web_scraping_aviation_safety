#%%time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.options import ChromiumOptions
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import math


lista = []
lista1 = []


for y in range(2019, 2020):
    print('Ano: ', end='')
    print(y,end=', ')

    options = ChromiumOptions()
    options.add_argument('--headless')
    navegador = webdriver.Chrome(options=options)
    navegador.maximize_window()
    navegador.get(f'https://aviation-safety.net/wikibase/dblist.php?Year={y}')


    quantidade_paginas = navegador.find_element(by=By.TAG_NAME, value='span')
    quantidade_paginas1 = quantidade_paginas.text.split(' ')[0]
    quantidade_paginas2 = int(quantidade_paginas1) / 100
    q = math.ceil(quantidade_paginas2)
    print('Ocorrências:', quantidade_paginas1, end=', ')
    print('Páginas:', q)

    page_content = navegador.page_source
    site = BeautifulSoup(page_content, 'html.parser')
    elementos = site.findAll('tr', attrs={'class':['list','listmain']})

    count = 0
    for a in range(1, q+1, 1):
    
        count = count + 1
   
        sleep(4)
        for elemento in elementos:
            a = elemento.text.splitlines()
            img = 'https:'+str(elemento.img)[10:-3]
            if 'cdn' in img:
                b = img
            else:
                pass
            for i in a[1:9]:
                lista.append(i)            
            lista.append(b)
            lista1.append(lista[:])
            lista.clear()

        #lista1
        navegador.get(f'https://aviation-safety.net/wikibase/dblist.php?Year={y}&sorteer=datekey&page={count+1}')
        page_content = navegador.page_source
        site = BeautifulSoup(page_content, 'html.parser')
        elementos = site.findAll('tr', attrs={'class':['list','listmain']})
    

df = pd.DataFrame(lista1, columns=['Date', 'Air_craft_type', 'Registration', 'Operator', 'Fatilites', 'Location', 'Vazio', 'Aircraft_damage', 'Country'])
df.shape