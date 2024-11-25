import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class FinewatersSpider(CrawlSpider):
    name = "finewaters"
    allowed_domains = ["finewaters.com"]
    start_urls = ["https://finewaters.com/bottled-waters-of-the-world"]

    # Ensure that rules is a tuple or list
    rules = (
        Rule(
            LinkExtractor(allow=(r"bottled-waters-of-the-world",), deny=(r"all-bottled-water-brands-alphabetical",)), 
            callback="parse_item"
        ),
    )

    def parse_item(self, response):
        title = response.xpath('//*[@id="g-mainbar"]/div/div/div/div/div/div/div/div[1]/h1/text()').get()
        rows = response.css('table tbody tr')
        my_dict ={}
        for row in rows:
            columns = row.css('td::text').getall()
           # try:
            for i in range(0, len(columns), 2):
                if len(columns) > i+1:
                    key = columns[i].replace('\xa0','')
                    value = columns[i+1].replace('\xa0','')
                    # if key == '\xa0':
                    #     key = key.replace('\xa0','')
                    # elif value == '\xa0':
                    #     value = value.replace('\xa0','')
                    my_dict[key] = value
           # print(my_dict)
            #except:

            # for x in columns:
            #     print(x)
            #print(columns)
        #print(my_dict)
        yield {
            'name': title,
            'balance': my_dict.get('Balance'),
            'minerality': my_dict.get('Minerality'),
            'hardness': my_dict.get('Hardness'),
            'carbonation': my_dict.get('Carbonation'),
            'tds': my_dict.get('TDS'),
            'ph': my_dict.get('ph factor'),
            'calcium': my_dict.get('Calcium'),
            'magnesium': my_dict.get('Magnesium'),
            'bicarbonate': my_dict.get('Bicarbonate'),
            'sulfate': my_dict.get('Sulfate')
        }