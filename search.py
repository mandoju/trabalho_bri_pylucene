from collections import OrderedDict
from lxml import etree as ET
from xml.dom import minidom
import codecs
import re
import csv
import logging
import time



from lucene import QueryParser , IndexSearcher, IndexReader, StandardAnalyzer, \
        TermPositionVector, SimpleFSDirectory, File, MoreLikeThis, \
            VERSION, initVM, Version
import sys
import lucene

class query_search:
    def __init__(self,query_number,query_text):
        self.query_number = query_number
        self.query_text = query_text



FIELD_CONTENTS = "abstract"
FIELD_PATH = "recordnum"

#QUERY_STRING = "infection"

STORE_DIR = "/home/jorge/lucene_index"



arquivos = ['db/cfquery.xml']
querys = []
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
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    for query in querys:
        # Constructs a query parser. We specify what field to search into.
        queryParser = QueryParser(Version.LUCENE_CURRENT,
                                  FIELD_CONTENTS, analyzer)

        # Create the query
        query = queryParser.parse(query.query_text)

        # Run the query and get top 50 results
        topDocs = searcher.search(query, 50)

        # Get top hits
        scoreDocs = topDocs.scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print doc.get(FIELD_PATH)