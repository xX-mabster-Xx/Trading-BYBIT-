from abc import ABC, abstractmethod

from wallet import Wallet


class strategy(ABC):
    def __init__(self, wallet: Wallet):
        self.wallet = wallet