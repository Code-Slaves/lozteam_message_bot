import requests
import json 
import time
from bs4 import BeautifulSoup

def get_notifications(token):

    url = "https://api.zelenka.guru/notifications"
    headers = {'Authorization': 'Bearer ' + token}
    params = {"scope": "read"}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:  
        # Если уведомления прочитаны
        new_notifications = [notif for notif in response.json()['notifications'] if notif['notification_is_unread']]
        return new_notifications


        # обработка списка уведомлений
    else:
        print("Ошибка при получении уведомлений:", response.status_code)




def clean_text(text): 
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()




def view_notif(token):
    url = "https://api.zelenka.guru/notifications/read"
    headers = {'Authorization': 'Bearer ' + token}


    payload = {"notification_is_unread": True}

    response = requests.post(url, headers=headers)
    response.raise_for_status()

