from pathlib import Path


### Base setting

BASE_PATH = Path(__file__).parent.parent

# BOT_TOKEN = env("BOT_TOKEN")
BOT_TOKEN = '2133806684:AAF_lM2IO5f9z5NJiLHRVTXG0y68cG2KjSA'
BASE_URL = '5.144.122.193:8080'                                          # Webhook domain
WEBHOOK_PATH = f'/tg/webhooks/bot/{BOT_TOKEN}'
WEBHOOK_URL = f'{BASE_URL}{WEBHOOK_PATH}'


admins = [
    333082547,
]

ip = {
    'db':    '',
    'redis': '',
}


### Connections

mysql_info = {
    'host':     ip['db'],
    'user':     '',
    'password': '',
    'db':       '',
    'maxsize':  5,
    'port':     3306,
}

redis = {
    'host':     ip['redis'],
    'password': ''
}


### Logging

LOGS_BASE_PATH = str(Path(__file__).parent.parent / 'logs')