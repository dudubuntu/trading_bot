from .umoney import UmoneySystem
from .card import CardSystem
from .config import *


payment_systems = {
    "Юмани": UmoneySystem,
    "Карта": CardSystem,
}