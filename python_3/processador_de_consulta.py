import configparser
from collections import OrderedDict
from lxml import etree as ET
from xml.dom import minidom
import codecs
import re
import csv

import logging
import time

class querynum_querytext:

    def __init__(self,querynum,querytext):
        self.querynum = querynum
        self.querytext = querytext

class document_vote:
    def __init__(self,document,vote):
        self.document = document
        self.vote = vote

class querynum_parlist:

    def __init__(self,querynum):
        self.querynum = querynum
        self.querylist = []

class querynum_item_vote_list:

    def __init__(self, querynum,item_vote_list):
        self.querynum = querynum
        self.item_vote_list = item_vote_list


#classe para ler  múltiplos "LEIA" do arquivo de configuração
class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict,self).__setitem__(key, value)


def main():

    logging.info("Program started!")


    # lendo o arquivo com os leia ,consulta e esperados
    config = configparser.RawConfigParser(strict=False, dict_type=MultiOrderedDict)

    logging.info("Reading PC.CFG")


    config.read(['PC.CFG'])
    entradas = config.get("DEFAULT", "LEIA");
    consulta = config.get("DEFAULT", "CONSULTAS");
    esperado = config.get("DEFAULT", "ESPERADOS");

    f = codecs.open('db\cfcquery-2.dtd')
    dtd = ET.DTD(f)


    row_consulta = []
    row_esperados = []

    logging.info("Starting reading xml")

    begin_time = time.perf_counter()


    for entrada in entradas:
        root = ET.parse(entrada)
        if (dtd.validate(root)):
            logging.info("Reading " + entrada + " xml file")

            xmldoc = minidom.parse(entrada)
            itemlist = xmldoc.getElementsByTagName('QUERY')
            for s in itemlist:
                querynum = s.getElementsByTagName('QueryNumber')
                querynum = int(querynum[0].firstChild.nodeValue)
                querytextnode = s.getElementsByTagName('QueryText')
                querytext = querytextnode[0].firstChild.nodeValue
                querytext = querytext.upper()
                querytext = re.sub('[^A-Z\ \']+', " ", querytext)
                row_consulta.append(querynum_querytext(querynum,querytext))

                recordlist = s.getElementsByTagName('Records')
                for r in recordlist:
                    item_votes_list = []
                    itemlist = r.getElementsByTagName('Item')
                    for i in itemlist:
                        item_document = i.firstChild.nodeValue
                        score = i.getAttribute("score")
                        item_votes = 0
                        for s in range(len(score)):
                            if(score[s]) != '0':
                                item_votes += 1
                        item_votes_list.append(( int(item_document),item_votes))
                row_esperados.append(querynum_item_vote_list(querynum,item_votes_list))
                #row_esperados.append(querynum_parlist(querynum,))
        else:
            logging.info(entrada + " xml file didn't pass on dtd validation")

            print(dtd.error_log.filter_from_errors())

    end_time = time.perf_counter()
    total_time = end_time - begin_time

    logging.info("Inverted list made " + str(len(entradas) / total_time) + " documents per second")


    logging.info("writing on csv")

    with open(consulta[0], 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in row_consulta:
            spamwriter.writerow([row.querynum,row.querytext])

    with open(esperado[0], 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in row_esperados:
            spamwriter.writerow([row.querynum, row.item_vote_list])

    logging.info("Finished!")


#    with open(consulta[0], 'w', newline='') as csvfile:
#        spamwriter = csv.writer(csvfile, delimiter=';',
#                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
#        for row in row_esperados:
#            spamwriter.writerow([row.querynum, row.querytext])


logging.basicConfig(filename='log\processador_de_consulta.log', level=logging.INFO,
                    format='%(asctime)s\t%(levelname)s\t%(message)s')

main()