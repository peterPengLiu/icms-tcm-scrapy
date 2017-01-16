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
    sourcePage = browser.page_source

    result = {}

    # beautiful soup parse
    if sourcePage == '':
        return result

    bs4 = BeautifulSoup(sourcePage, 'html.parser')
    if bs4 == None:
        print('The bs4 object is none!')
        return result
    # print(bs4)
    # Parse the website
    # title
    titleItem = bs4.find('h1', {'id':'title'})
    titleStr = ''
    if titleItem:
        titleStr = titleItem.get_text()
        print('tile: ' + titleStr)
        print(repr(titleStr))
        print(type(titleStr))

    # abstract
    abstractItem = bs4.find('section', {'id':'abstract'})
    abstractStr = ''
    if abstractItem:
        abstractStr = abstractItem.get_text().replace('\n',' ').strip()
        print(repr(abstractStr))
        print(type(abstractStr))
        # abstractStr = abstractItem.get_text().encode('utf-8').strip().replace('\n',' ')
        # print('abstract: ', abstractStr)

    # classification
    classificationItem = bs4.find('section', {'id':'classifications'})
    classificationStr = ''
    if classificationItem:
        classificationStr = classificationItem.get_text().strip().replace('\n',' ')
        # print('classifications: ', classificationStr)

    # description
    descriptionItem = bs4.find('section', {'id':'description'})
    descriptionStr = ''
    if descriptionItem:
        descriptionStr = descriptionItem.get_text().strip().replace('\n',' ')
        # print('description: ', descriptionStr)

    # claims
    claimsItem = bs4.find('section', {'id':'claims'})
    claimsStr = ''
    if claimsItem:
        claimsStr = claimsItem.get_text().strip().replace('\n',' ')
        # print('claims: ', claimsStr)


    # footer of website
    footerItem = bs4.find('div', {'class':'footer'})
    citedByStr = ''
    similarDocumentStr = ''
    if footerItem:
        # print('footer h3 len:', len(footerItem.h3))

        footerDivList = footerItem.find_all('div', {'class':'responsive-table'})
        # print('footer table len:', len(footerDivList))

        # if footerDivList and len(footerDivList) >= 2:

            # # footer list [0] is the cite by table
            # citedByTable = footerDivList[0].find('div', {'class':'table'})
            # if citedByTable:
            #     # cited by table header
            #     citedByThead = citedByTable.find('div', {'class':'thead'})
            #     citedBySpans = citedByThead.find('span', {'class':'th'})
            #     citedByColumnLen = len(citedBySpans)
            #     print('cited by column len:', str(citedByColumnLen))
            #     citedByColumnStrList = []
            #     for citedBySpansItem in citedBySpans:
            #         citedByColumnStrList.append(citedBySpansItem.get_text().strip().replace('\n',''))
            #
            #     # cited by table body
            #     citedByTbodyStrList = []
            #     citedByTbody = citedByTable.find('div', {'class':'tbody'})
            #     citedByTbodyList = citedByTbody.find('div', {'class':'tr'})
            #     for citedbyTbodyItem in citedByTbodyList:
            #         citedByTbodyItemStr = ''
            #         citedByTbodySpans = citedbyTbodyItem.find('span', {'class':'td'})
            #         if len(citedByTbodySpans) != citedByColumnLen:
            #             continue
            #         for i in range(citedByColumnLen):
            #             citedByTbodyItemStr += citedByColumnStrList[i] + ':' + citedByTbodySpans[i].get_text().strip().replace('\n','')
            #         citedByTbodyStrList.append(citedByTbodyItemStr)
            #
            #     print('cited body len:' + str(len(citedByTbodyStrList)))

            # footer list [1] is the similar document table
            # similarDocumentTable = footerDivList[1]



        # cited by
        citedByItem = footerItem.find('h3', {'id':'citedBy'})

        if citedByItem:
            citedByStr = citedByItem.get_text().strip().replace('\n', ' ')

            # cited by table = footerDivList[0]
            if footerDivList and len(footerDivList) >= 2:
                citedByStr += footerDivList[0].get_text().strip().replace('\n', ' ')
        # print('cited by :', citedByStr)

        # similar documents
        similarDocumentItem = footerItem.find('h3', {'id':'similarDocuments'})
        if similarDocumentItem:
            similarDocumentStr = similarDocumentItem.get_text().strip().replace('\n',' ')
            # similar document table
            if footerDivList and len(footerDivList)>= 2:
                similarDocumentStr += footerDivList[1].get_text().strip().replace('\n', ' ')
        # print('similar documents:', similarDocumentStr)




    # cited by tables
    citeByList = []


    # similar documents tables

    # knowledge card
    knowledgeCardItem = bs4.find('section', {'class':'knowledge-card'})
    knowledgeCardStr = ''
    knowledgeCardHeaderStr = ''
    knowledgeCardDlStr = ''
    if knowledgeCardItem:
        knowledgeCardStr = knowledgeCardItem.get_text().strip().replace('\n',' ')
        # print('knowledge card: ', knowledgeCardStr)
        # the header of knowledge card
        knowledgeCardHeader = knowledgeCardItem.find('header', {'class':'patent-result'})

        if knowledgeCardHeader:
            knowledgeCardHeaderStr = knowledgeCardHeader.get_text().strip().replace('\n', ' ')
            # print('knowledge card header:', knowledgeCardHeaderStr)

        # dl item
        knowledgeCardDls = knowledgeCardItem.find_all('dl')

        if knowledgeCardDls:
            # print('knowledge card len:', len(knowledgeCardDls))
            for dlItem in knowledgeCardDls:
                knowledgeCardDlStr += dlItem.get_text().strip().replace('\n', '')

    # print('knowledge card dl:', knowledgeCardDlStr)

    # format the parse result
    result = {'title':titleStr,'abstract':abstractStr,'classifications':classificationStr,'description':descriptionStr,
              'claims':claimsStr,'citedBy':citedByStr,'similarDocuments':similarDocumentStr,'knowledgeCardHeader':knowledgeCardHeaderStr,
              'knowledgeCardDls':knowledgeCardDlStr}

    return result



def main(argv):
    # output file

    # print(str(argv))
    inputFile = str(argv)
    if inputFile == '':
        logging.warning('CSV file should not be null!')
        return
    # output file
    outputfile = inputFile.replace('.csv','.txt')

    # write outputfile
    with open(outputfile, 'w') as outfile:
        # Read the CSV file from the search result
        csvDataList = []
        with open(inputFile, 'r') as f:
            for i in range(2):
                f.__next__()

            csvReader = csv.reader(f)
            for row in csvReader:
                if len(row) != 9:
                    continue
                jsonData = {}

                jsonData = {'id': row[0], 'title': row[1], 'assignee': row[2], 'author': row[3], 'prioritydate': row[4],
                            'creationDate': row[5], 'publicationDate': row[6], 'grantDate': row[7],
                            'resultLink': row[8]}
                csvDataList.append(jsonData)

        # print(len(csvDataList))
        # Based on the result link in csv file, parse the website.
        if len(csvDataList) == 0:
            logging.warning('No result found!')
            return
        # get the website based on the url in csv file
        browser = webdriver.Firefox()

        index = 0
        for csvItem in csvDataList:
            if csvItem['resultLink'] == '' or csvItem['resultLink'] == None:
                continue

            resultLink = str(csvItem['resultLink'])
            parseResult = parse(browser, resultLink)

            csvItem['parseResult'] = parseResult

            outfile.write(json.dumps(csvItem))

            print(str(index))
            index += 1

        browser.close()

    return




if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.warning('Not enough parameters!')
        logging.warning('Such as: python3 google_patents_scrapy.py csv_file.csv')
    else:
        main(sys.argv[1])
        print('---End---')
