from collections import OrderedDict
from lxml import etree as ET
from xml.dom import minidom
import codecs
import nltk
import logging
import time
import re
import csv



import lucene

class documento:
    def __init__(self,recordnum,abstract):
         self.recordnum = recordnum
         self.abstract = abstract

#INDEX_DIR = "/home/jorge/lucene_index"
INDEX_DIR = "lucene_index"
arquivos = ['db/cf74.xml','db/cf75.xml','db/cf76.xml','db/cf77.xml','db/cf78.xml','db/cf79.xml']
documentos = []
# parte de ler o xml usando o dtd
f = codecs.open('db/cfc-2.dtd')
dtd = ET.DTD(f)

for entrada in arquivos:
        #print("printando a entrada " + entrada)
        logging.info("Reading " + entrada + " xml file")
        root = ET.parse(entrada)
        if(dtd.validate(root)):
            xmldoc = minidom.parse(entrada)
            itemlist = xmldoc.getElementsByTagName('RECORD')
            for s in itemlist:
                recordnum = s.getElementsByTagName('RECORDNUM')
                recordnum =  int(recordnum[0].firstChild.nodeValue)
                abstract = s.getElementsByTagName('ABSTRACT')
                if(len(abstract) > 0):
                    text_to_parse = abstract[0].firstChild.nodeValue
                else:
                    extract = s.getElementsByTagName('EXTRACT')
                    if(len(extract) > 0):
                        text_to_parse = extract[0].firstChild.nodeValue
                    else:
                        continue
                documentos.append(documento(recordnum,text_to_parse))
                #text_to_parse = text_to_parse.upper()
                #text_to_parse = re.sub('[^A-Z\ \']+', " ", text_to_parse)
                #text_words = text_to_parse.split()
                #print(s.attributes['RECORDNUM'].value)
        else:
            logging.info(entrada + " xml file didn't pass on dtd validation")

            #print(dtd.error_log.filter_from_errors())

# Initialize lucene and JVM
lucene.initVM()

print "lucene version is:", lucene.VERSION

# Get the analyzer
analyzer = lucene.EnglishAnalyzer(lucene.Version.LUCENE_CURRENT)

# Get index storage
store = lucene.SimpleFSDirectory(lucene.File(INDEX_DIR))

# Get index writer
writer = lucene.IndexWriter(store, analyzer, True, lucene.IndexWriter.MaxFieldLength.LIMITED)

for record in documentos:
    try:
        # create a document that would we added to the index
        doc = lucene.Document()

        # Add a field to this document
        field_recordnum = lucene.Field("recordnum", str(record.recordnum), lucene.Field.Store.YES, lucene.Field.Index.ANALYZED)
        field_abstract = lucene.Field("abstract", str(record.abstract), lucene.Field.Store.YES, lucene.Field.Index.ANALYZED)
        # Add this field to the document
        doc.add(field_recordnum)
        doc.add(field_abstract)

        # Add the document to the index
        writer.addDocument(doc)

    except Exception, e:
        print "Failed :", e
writer.close()
print "end"