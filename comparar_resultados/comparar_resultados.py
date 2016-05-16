from __future__ import division
import csv
import numpy as np
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from math import log


def precisao(array_resultado,array_esperado):

    verdadeiro_positivo = 0
    falso_positivo = 0
    for resultado in array_resultado:
        if resultado in array_esperado:
            verdadeiro_positivo += 1
        else:
            falso_positivo += 1

    resultado_final = verdadeiro_positivo / (verdadeiro_positivo + falso_positivo)
    return resultado_final

def recall(array_resultado,array_esperado):

    verdadeiro_positivo = 0
    falso_positivo = 0
    for resultado in array_resultado:
        if resultado in array_esperado:
            verdadeiro_positivo += 1
        else:
            falso_positivo += 1

    resultado = verdadeiro_positivo / len(array_esperado)
    return resultado

def f1(precisao_input,recall_input):

    return 2 * ((precisao_input*recall_input)/(precisao_input+recall_input))

def media(array):
    if(len(array) == 0):
        return 0
    return sum(array)/len(array)

class resultado:
    def __init__(self,posicao,resultados):
        self.posicao = posicao
        self.resultados = resultados

def comparar():


    resultados_esperados = []
    resultados_obtidos = []

    array_esperados = []
    array_resultados = []

    #carregando consultas
    with open("resultados_da_busca/esperados.csv") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            resultados_esperados.append(resultado(row[0],eval(row[1])))

    with open("resultados_da_busca/resultados.csv") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            resultados_obtidos.append(resultado(row[0], eval(row[1])))


    for re in resultados_esperados:
        array = []
        for r in re.resultados:
            array.append(r[0])
        array_esperados.append(array)
        #array_esperados.append(re.resultados[0])

    for re in resultados_obtidos:
        array = []
        for r in re.resultados:
            array.append(r[1])
        array_resultados.append(array)
        #array_resultados.append(re.resultados[0])

    #teste = array_resultados[0]

    #print(teste)
    #print(array_esperados[0])
    #print(dcg(array_resultados[0],len(array_resultados[0]),0))
    #precision_score(teste,array_esperados[0], average='macro')

    #calculando precision@10
    quantidade_de_resultados = len(array_resultados)

    array_de_precisao_10 = []
    array_de_precisao = []
    array_de_recall = []
    array_de_recall_10 = []
    array_de_f1 = []
    array_de_dcg = []
    array_de_ndcg = []

    array_para_grafico_00 = []
    array_para_grafico_01 = []
    array_para_grafico_02 = []
    array_para_grafico_03 = []
    array_para_grafico_04 = []
    array_para_grafico_05 = []
    array_para_grafico_06 = []
    array_para_grafico_07 = []
    array_para_grafico_08 = []
    array_para_grafico_09 = []
    array_para_grafico_10 = []

    for i in range(0,quantidade_de_resultados):
        precisao_atual_10 = precisao(array_resultados[i][:10],array_esperados[i])
        precisao_atual = precisao(array_resultados[i],array_esperados[i])
        recall_atual = recall(array_resultados[i], array_esperados[i])
        recall_atual_10 = recall(array_resultados[i][:10], array_esperados[i])
        f1_atual = f1(precisao_atual,recall_atual)

        if(recall_atual > 0 and recall_atual < 0.05):
            array_para_grafico_00.append(precisao_atual)
        if (recall_atual > 0.05 and recall_atual < 0.15):
            array_para_grafico_01.append(precisao_atual)
        if (recall_atual > 0.15 and recall_atual < 0.25):
            array_para_grafico_02.append(precisao_atual)
        if (recall_atual > 0.25 and recall_atual < 0.35):
            array_para_grafico_03.append(precisao_atual)
        if (recall_atual > 0.35 and recall_atual < 0.45):
            array_para_grafico_04.append(precisao_atual)
        if (recall_atual > 0.45 and recall_atual < 0.55):
            array_para_grafico_05.append(precisao_atual)
        if (recall_atual > 0.55 and recall_atual < 0.65):
            array_para_grafico_06.append(precisao_atual)
        if (recall_atual > 0.65 and recall_atual < 0.75):
            array_para_grafico_07.append(precisao_atual)
        if (recall_atual > 0.75 and recall_atual < 0.85):
            array_para_grafico_08.append(precisao_atual)
        if (recall_atual > 0.85 and recall_atual < 0.95):
            array_para_grafico_09.append(precisao_atual)
        if (recall_atual > 0.95):
            array_para_grafico_10.append(precisao_atual)


        array_de_precisao_10.append(precisao_atual_10)
        array_de_precisao.append(precisao_atual)
        array_de_recall_10.append(recall_atual)
        array_de_recall.append(recall_atual_10)
        array_de_f1.append(f1_atual)

    array_para_grafico_00 = media(array_para_grafico_00)
    array_para_grafico_01 = media(array_para_grafico_01)
    array_para_grafico_02 = media(array_para_grafico_02)
    array_para_grafico_03 = media(array_para_grafico_03)
    array_para_grafico_04 = media(array_para_grafico_04)
    array_para_grafico_05 = media(array_para_grafico_05)
    array_para_grafico_06 = media(array_para_grafico_06)
    array_para_grafico_07 = media(array_para_grafico_07)
    array_para_grafico_08 = media(array_para_grafico_08)
    array_para_grafico_09 = media(array_para_grafico_09)
    array_para_grafico_10 = media(array_para_grafico_10)



    print("MAP com precision@10 :" + str(media(array_de_precisao_10)))
    print("MAP com todos os resultados: " + str(media(array_de_precisao)))
    #print(media(array_de_recall))
    #print(media(array_de_recall_10))
    print("Media do F1 : " + str(media(array_de_f1)))
    #print(sum(array_de_recall)/len(array_de_recall))


    with open("resultados_da_comparacao/11pontos-stemmer.csv", 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([0, array_para_grafico_00])
        spamwriter.writerow([0.1, array_para_grafico_01])
        spamwriter.writerow([0.2, array_para_grafico_02])
        spamwriter.writerow([0.3, array_para_grafico_03])
        spamwriter.writerow([0.4, array_para_grafico_04])
        spamwriter.writerow([0.5, array_para_grafico_05])
        spamwriter.writerow([0.6, array_para_grafico_06])
        spamwriter.writerow([0.7, array_para_grafico_07])
        spamwriter.writerow([0.8, array_para_grafico_08])
        spamwriter.writerow([0.9, array_para_grafico_09])
        spamwriter.writerow([1.0, array_para_grafico_10])





    #print(precision_score(array_resultados[0][:len(array_esperados[0])], array_esperados[0]))
comparar();