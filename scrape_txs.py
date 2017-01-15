#!/usr/bin/python
from bs4 import BeautifulSoup
import cfscrape
from contract import *


class ContractCodeScraper:

    def __init__(self):
        self._db = ContractDatabase();
        self._scraper = cfscrape.create_scraper();
        self._pages = [];
        self._db.read();

    @property
    def db(self,value):
        self._db = value;

    @property
    def db(self):
        return self._db


    def fill_db(self):
        for contract in db:
            url = contract.url;
            page = self._scraper.get(url).content;

            return;
