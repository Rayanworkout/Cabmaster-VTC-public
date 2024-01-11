import requests


def telegram_message(message):
    requests.get(
        "https://api.telegram.org/bot1768068100:AAHVGEdeItHypLHBfqmMoqdqhX4KdgO08Gc/sendMessage?chat_id=901170303&text={}".format(message)
    )
    
with open('./cabmaster/report.txt', 'r') as f:
    text = "Test Coverage Report after push on main branch\n\n"
    text += f.read()
    telegram_message(text)
