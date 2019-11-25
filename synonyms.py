import csv
import os
import json
import requests
import wptools

enWikipediaFormat = "https://en.wikipedia.org/w/api.php"
actionParse = "?action=parse"
page = "&page="
redirects = "&redirects=1"
propLink = "&prop=links" #can be used to check if synonyms exist for this species
propText = "&prop=wikitext"
formatJson = "&format=json"

#example: https://en.wikipedia.org/w/api.php?action=parse&page=Odocoileus_virginianus&redirects=1&prop=wikitext&format=jsonfm
#https://en.wikipedia.org/w/api.php?action=parse&page=Odocoileus_virginianus&redirects=1&prop=links&format=jsonfm

sni = 9 #scientific name index
cni = 10 #common name index
si = 11 #synonymns index

path = './csv/'

""" gets synonyms of a species with the scientific name sn in the row"""
def getSynonyms(row, sciname):
    retval = ""
    articleTitle = sciname

    #need to slugify name?
    req = enWikipediaFormat + actionParse + page + sciname + redirects + propText + formatJson
    response = requests.get(req)
    data = response.json()

    try:
        articleTitle = data['parse']['redirects'][0]['to']
    except KeyError:
        print("need to catch this error")

    #search for synonyms

    page1 = wptools.page(articleTitle)
    fela = page1.get_parse()
    print(fela)
    try:
        syn = page1.data['infobox']['synonyms']
        syns = syn.split('\n')

        for s in syns:
            temp = s.split('\'')
            retval = retval + temp[2] + ", "
            #print(temp[2])
        return retval
    except:
        return retval

for file in os.listdir(path):
    pf = path + file
    help = []
    with open(pf, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',') #assuming dialect parameter is 'excel'
        for row in csv_reader:
            print("row is " + str(row))
            if row[1] == "Park Name":
                sni = row.index("Scientific Name")
                cni = row.index("Common Names")
                si = row.index("Synonyms")
                print("test")
                continue

            scientificname = row[sni]
            print(scientificname)
            commonname = row[cni]
            syns = getSynonyms(row, scientificname)

            row[si] = syns

            print(row)

            help.append(row)

    with open (pf, 'a+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar = '\"', quoting=csv.QUOTE_MINIMAL)

        for row in help:
            print(row)
            csv_writer.writerow(row)