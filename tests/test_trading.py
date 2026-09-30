import pytest

from game.inventory import Inventory
from game.trading import TradingService


def test_create_and_buy_offer():
    service = TradingService()
    seller = Inventory()
    seller.add_item("ore", 2)
    buyer = Inventory(credits=100)
    offer = service.create_offer("seller", seller, "ore", 2, 40)
    assert seller.items == {}
    assert service.buy_offer("buyer", buyer, offer.offer_id) is True
    assert buyer.items["ore"] == 2
    assert buyer.credits == 60
    assert service.list_offers() == ()


def test_cancel_offer_returns_items():
    service = TradingService()
    inventory = Inventory()
    inventory.add_item("ore", 2)
    offer = service.create_offer("seller", inventory, "ore", 1, 10)
    assert service.cancel_offer("seller", inventory, offer.offer_id) is True
    assert inventory.items["ore"] == 2


def test_offer_requires_items_and_valid_values():
    service = TradingService()
    inventory = Inventory()
    with pytest.raises(ValueError):
        service.create_offer("seller", inventory, "ore", 1, 10)
    inventory.add_item("ore")
    with pytest.raises(ValueError):
        service.create_offer("seller", inventory, "ore", 0, 10)


def test_buyer_cannot_buy_without_funds():
    service = TradingService()
    seller = Inventory()
    seller.add_item("ore")
    buyer = Inventory(credits=1)
    offer = service.create_offer("seller", seller, "ore", 1, 10)
    assert service.buy_offer("buyer", buyer, offer.offer_id) is False
    assert offer.offer_id in {item.offer_id for item in service.list_offers()}
