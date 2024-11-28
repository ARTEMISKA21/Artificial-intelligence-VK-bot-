import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from mistralai import Mistral

api_key = "..."
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

TOKEN = '...'
GROUP_ID = '...'

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def send_message(peer_id, message):
    vk.messages.send(
        peer_id=peer_id,
        message=message,
        random_id=0
    )

def get_mistral_response(user_message):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": user_message,
            },
        ]
    )
    return chat_response.choices[0].message.content

def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            peer_id = event.peer_id
            user_message = event.text
            print(f"Получено сообщение от {peer_id}: {user_message}")

            response_message = get_mistral_response(user_message)

            send_message(peer_id, response_message)

if __name__ == "__main__":
    main()
