import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import LunarItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class LunarSpider(scrapy.Spider):
	name = 'lunar'
	start_urls = ['https://lunar.app/en/blog/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="ServerSideMasonry__StyledServerSideMasonry-sc-1hc46tp-0 foVdUb"]/a[@class="InternalPageLink-acx5cl-0 ejbbZl"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//p[@class="index-module--date--2S-d0"]/text()').get()
		title = response.xpath('//h1[@class="index-module--title--mvcCi"]/text()').get()
		content = response.xpath('//h4[@class="index-module--manchet--37gxk"]//text()').getall() + response.xpath('//div[@class="index-module--sectionsWrapper--1bEQn"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=LunarItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
