import requests as req
import pandas as pd
import PySimpleGUI as sg
from pathlib import Path

def search_pic():
    ids = []
    likes = []
    views = []
    token = '********************************************************'
    path = Path(values['-USER FOLDER-'], 'BEST MEM.jpg')
    domain = values['-PUBL-'].split('/')[-1]
    for i in range(0,1001,100):
        params = {
        'domain':domain,
        'offset': i,
        'count':100,
        'extended':0,
        'v':5.131
              }
        r = req.get(f'https://api.vk.com/method/wall.get', params, headers={'Authorization': f'Bearer {token}'})
        stena = r.json()['response']['items']
        for u in stena:
            ids.append(u['id'])
            likes.append(u['likes']['count'])
            views.append(u['views']['count'])
    res_dict = {'id':[], 'pic_url':[]}
    for i in range(0,1001,100):
        params = {
        'domain':domain,
        'offset': i,
        'count':100,
        'extended':0,
        'v':5.131
                }
        r = req.get(f'https://api.vk.com/method/wall.get', params, headers={'Authorization': f'Bearer {token}'})
        stena = r.json()['response']['items']
        for u in stena:
            try:
                res_dict['id'].append(u['id'])
                res_dict['pic_url'].append(u['attachments'][0]['photo']['sizes'][-1]['url'])
            except:
                res_dict['pic_url'].append('None')
    df = pd.DataFrame({'ids':ids, 'likes':likes,'views':views})
    df.sort_values('likes', ascending=False, inplace=True)
    pic_link = res_dict['pic_url'][res_dict['id'].index(df.ids.iloc[0])]
    with open(path, 'wb') as file:
      file.write(req.get(pic_link).content)


sg.theme('DarkBlue15') # зафигачили тему всего окна
sg.set_options(font=('Arial Bold', 12)) # зафигачили шрифт всех текстов в окне

layout =[
    [sg.Image('Banana_cat_s.png'),
     sg.Image('vk_logo.png', expand_x=True),
     sg.Image('pig_fall_s.png')],
    [sg.Text('Введите URL паблика')],
    [sg.Input(key='-PUBL-')],
    [sg.Text('Выберите папку, куда скачается мем')],
    [sg.FolderBrowse(target='-USER FOLDER-', size=(15,1))],
    [sg.Input(key='-USER FOLDER-')],
    [sg.Button('Скачать', size=(10,2), font=('Arial Bold', 16), key='-OUT-')]
]
window = sg.Window('Удачной охоты за мемом!', layout, size=(600, 500), element_justification='c')

while True:
    event, values = window.read()
    if event == '-OUT-':
        if window['-PUBL-'].get() == '':
            sg.popup('Вы не ввели имя паблика')
        elif window['-USER FOLDER-'].get() == '':
            sg.popup('Вы не ввели папку назначения')
        else:
            res = search_pic()
            sg.popup('Вы получили свою порцию мема! Смейтесь!')
    if event == sg.WIN_CLOSED or event == 'Выход':
        break

window.close()