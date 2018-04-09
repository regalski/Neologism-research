#!/bin/bash
scrapy crawl badger -s LOG_LEVEL=INFO -s LOG_FILE=.log -s JOBDIR=crawls/badger-1
