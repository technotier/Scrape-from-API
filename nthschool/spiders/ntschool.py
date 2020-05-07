# -*- coding: utf-8 -*-
import scrapy
import json

class NtschoolSpider(scrapy.Spider):
    name = 'ntschool'
    start_urls = ['https://directory.ntschools.net/#/schools']

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US, en;q = 0.9, bn;q = 0.8",
        "Referer": "https://directory.ntschools.net/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "X-Requested-With": "Fetch",
    }

    def parse(self, response):
        # url = 'https://directory.ntschools.net/api/System/GetAllSchools'
        # request = scrapy.Request(url, callback=self.parse_api, headers=self.headers)
        yield scrapy.Request(url='https://directory.ntschools.net/api/System/GetAllSchools', callback=self.parse_api, headers=self.headers)

    def parse_api(self, response):
      base_url = 'https://directory.ntschools.net/api/System/GetSchool?itSchoolCode='
      raw_data = response.body
      data = json.loads(raw_data.decode('utf-8'))
      for school in data:
        school_code = school['itSchoolCode']
        school_url = base_url + school_code
        # request = scrapy.Request(school_url, callback=self.parse_school, headers=self.headers)
        yield scrapy.Request(url=school_url, callback=self.parse_school, headers=self.headers)

    def parse_school(self, response):
      raw_data = response.body
      data = json.loads(raw_data.decode('utf-8'))
      yield {
        "Name": data['name'],
        "Physical Address": data['physicalAddress']['displayAddress'],
        "Postal Address": data['postalAddress']['displayAddress'],
        "Email": data['mail'],
        "Phone": data['telephoneNumber']
      }
