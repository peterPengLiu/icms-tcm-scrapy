# coding:utf-8
import sys
import logging
import csv
import json
from selenium import webdriver
from bs4 import BeautifulSoup


# Parse website based on the result link
def parse(browser, resultLink):
    browser.get(resultLink)
    # source page
    sourcePage = browser.get_text()


    return {}



def main(argv):
    # print(str(argv))
    inputFile = str(argv)
    if inputFile == '':
        logging.warning('CSV file should not be null!')
        return
    # Read the CSV file
    csvDataList = []
    with open(inputFile, 'r') as f:
        for i in range(2):
            f.__next__()

        csvReader = csv.reader(f)
        for row in csvReader:
            if len(row) != 9:
                continue
            jsonData = {}

            jsonData = {'id':row[0],'title':row[1],'assignee':row[2],'author':row[3],'prioritydate':row[4],
                        'creationDate':row[5],'publicationDate':row[6],'grantDate':row[7],'resultLink':row[8]}
            csvDataList.append(jsonData)

    print(len(csvDataList))
    # Based on the result link in csv file, parse the website.
    if len(csvDataList) == 0:
        logging.warning('No result found!')
        return

    browser = webdriver.Firefox()


    for csvItem in csvDataList:
        if csvItem['resultLink'] == '' or csvItem['resultLink'] == None:
            continue

        resultLink = str(csvItem['resultLink'])
        parseResult = parse(browser, resultLink)

        csvItem['parseResult'] = parseResult

        print(len(csvItem))

        exit()

    browser.close()

    return




if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.warning('Not enough parameters!')
        logging.warning('Such as: python3 google_patents_scrapy.py csv_file.csv')
    else:
        main(sys.argv[1])
        print('---End---')
