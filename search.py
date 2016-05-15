from collections import OrderedDict
from lxml import etree as ET
from xml.dom import minidom
import codecs
import re
import csv
import logging
import time



from lucene import QueryParser , IndexSearcher, IndexReader, StandardAnalyzer,EnglishAnalyzer, \
        TermPositionVector, SimpleFSDirectory, File, MoreLikeThis, \
            VERSION, initVM, Version
import sys
import lucene
class query_search:
    def __init__(self,query_number,query_text):
        self.query_number = query_number
        self.query_text = query_text

class resultado_query:
    def __init__(self,query_number,query_results):
        self.query_number = query_number
        self.query_results = query_results

FIELD_CONTENTS = "abstract"
FIELD_PATH = "recordnum"

#QUERY_STRING = "infection"

STORE_DIR = "lucene_index"



arquivos = ['db/cfquery.xml']
querys = []
resultados = []
# parte de ler o xml usando o dtd
f = codecs.open('db/cfcquery-2.dtd')
dtd = ET.DTD(f)



for entrada in arquivos:
        root = ET.parse(entrada)
        if (dtd.validate(root)):

            xmldoc = minidom.parse(entrada)
            itemlist = xmldoc.getElementsByTagName('QUERY')
            for s in itemlist:
                querynum = s.getElementsByTagName('QueryNumber')
                querynum = int(querynum[0].firstChild.nodeValue)
                querytextnode = s.getElementsByTagName('QueryText')
                querytext = querytextnode[0].firstChild.nodeValue
                #querytext = querytext.upper()
                #querytext = re.sub('[^A-Z\ \']+', " ", querytext)
                #row_consulta.append(querynum_querytext(querynum,querytext))
                querys.append(query_search(querynum,querytext))

        else:
            logging.info(entrada + " xml file didn't pass on dtd validation")

            print(dtd.error_log.filter_from_errors())


if __name__ == '__main__':
    initVM()
    print 'lucene', VERSION

    # Get handle to index directory
    directory = SimpleFSDirectory(File(STORE_DIR))

    # Creates a searcher searching the provided index.
    ireader  = IndexReader.open(directory, True)

    # Implements search over a single IndexReader.
    # Use a single instance and use it across queries
    # to improve performance.
    searcher = IndexSearcher(ireader)

    # Get the analyzer
    analyzer = EnglishAnalyzer(Version.LUCENE_CURRENT)

    for query in querys:
        query_number =  query.query_number
        # Constructs a query parser. We specify what field to search into.
        query.query_text = query.query_text.replace('?','')
        query.query_text = query.query_text.replace('*','')
        queryParser = QueryParser(Version.LUCENE_CURRENT,
                                  FIELD_CONTENTS, analyzer)

        # Create the query
        query = queryParser.parse(query.query_text)

        # Run the query and get top 50 results
        topDocs = searcher.search(query,50000)

        # Get top hits
        scoreDocs = topDocs.scoreDocs

        r = resultado_query(query_number,scoreDocs)
        resultados.append(r)
        #print "%s total matching documents." % len(scoreDocs)
        #for scoreDoc in scoreDocs:
        #    doc = searcher.doc(scoreDoc.doc)
        #    print doc.get(FIELD_PATH)

    with open('comparar_resultados/resultados_da_busca/resultados.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in resultados:
            resultados_da_row = []
            for resultado_da_query in row.query_results:
                doc = searcher.doc(resultado_da_query.doc)
                resultados_da_row.append(int(doc.get(FIELD_PATH)))
            spamwriter.writerow([row.query_number,resultados_da_row])

