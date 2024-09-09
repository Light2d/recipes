import requests
import requests
import time

# Заголовки запроса

# Данные черновика
draft_data = {
    "campaignDraftId": "",
    "fromEmail": "lighttt2d@gmail.com",  # Укажите свой адрес электронной почты
    "subject": "Your Subject Here",
    "message": "Your message content here",
    "messageType": "plain",  # Используйте "html" для HTML-сообщений, если требуется
    "emailAddresses": "lightpavelll@gmail.com",  # Если используется список
}

# Создание черновика кампании
draft_response = requests.post(
    'https://api.gmass.co/api/campaigndrafts?apikey=7ebec6dd-56e5-420a-aa8e-d8f59de571db',
    json=draft_data,
     headers={'Content-Type': 'application/json'}
)

if draft_response.status_code == 200:
        campaign_draft_id = draft_response.json().get('campaignDraftId')
       
        print("Черновик создан успешно:", campaign_draft_id)
        
        # Данные для отправки кампании
        campaign_data = {
           
        }

        # Отправка кампании через GMass
        response = requests.post(
            f'https://api.gmass.co/api/campaigns/{campaign_draft_id}?apikey=7ebec6dd-56e5-420a-aa8e-d8f59de571db',
            json=campaign_data,
            headers={'Content-Type': 'application/json'}
        )

        # Проверка ответа
        if response.status_code == 200:
            print("Кампания успешно отправлена")
        else:
            print(f"Не удалось отправить кампанию: {response.text}")
else:
    print(f"Не удалось создать черновик: {draft_response.text}")