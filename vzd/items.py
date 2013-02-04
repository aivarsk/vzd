# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class VzdItem(Item):
    url = Field()
    city = Field()
    district = Field()
    street = Field()
    village = Field()
    space = Field()
    n_floors = Field()
    n_rooms = Field()
    land_area = Field()
    price = Field()
    note = Field()
    images = Field()
