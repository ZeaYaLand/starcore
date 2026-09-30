from dataclasses import dataclass

from game.economy import EconomyService
from game.inventory import Inventory


@dataclass(frozen=True)
class TradeOffer:
    offer_id: str
    seller_id: str
    item_id: str
    quantity: int
    price: int
    currency: str = "credits"


class TradingService:
    def __init__(self, economy: EconomyService | None = None):
        self.economy = economy or EconomyService()
        self.offers: dict[str, TradeOffer] = {}
        self._next_id = 1

    def create_offer(self, seller_id: str, inventory: Inventory, item_id: str, quantity: int, price: int, currency: str = "credits") -> TradeOffer:
        if not seller_id or quantity <= 0 or price < 0 or currency not in {"credits", "crystals"}:
            raise ValueError("invalid trade offer")
        if not inventory.remove_item(item_id, quantity):
            raise ValueError("insufficient item quantity")
        offer = TradeOffer(f"offer_{self._next_id}", seller_id, item_id, quantity, price, currency)
        self._next_id += 1
        self.offers[offer.offer_id] = offer
        return offer

    def cancel_offer(self, seller_id: str, inventory: Inventory, offer_id: str) -> bool:
        offer = self.offers.get(offer_id)
        if offer is None or offer.seller_id != seller_id:
            return False
        inventory.add_item(offer.item_id, offer.quantity)
        del self.offers[offer_id]
        return True

    def buy_offer(self, buyer_id: str, buyer: Inventory, offer_id: str) -> bool:
        if not buyer_id:
            return False
        offer = self.offers.get(offer_id)
        if offer is None or offer.seller_id == buyer_id:
            return False
        if offer.currency == "credits":
            if not buyer.spend_credits(offer.price):
                return False
        elif offer.currency == "crystals":
            if buyer.crystals < offer.price:
                return False
            buyer.crystals -= offer.price
        else:
            return False
        buyer.add_item(offer.item_id, offer.quantity)
        del self.offers[offer_id]
        return True

    def list_offers(self) -> tuple[TradeOffer, ...]:
        return tuple(self.offers.values())
