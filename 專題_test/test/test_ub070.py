from lxml import etree

tree = etree.parse('070_尚硅谷_爬虫_解析_xpath的基本使用.html')

li_list = tree.xpath('//ul//li[@id="l1"]/text()')

print(li_list)
print(len(li_list))