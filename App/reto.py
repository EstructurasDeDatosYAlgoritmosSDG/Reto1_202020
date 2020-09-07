"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv
from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt
from Sorting import selectionsort as ss
from Sorting import insertionsort as ins
from Sorting import shellsort as shs


from time import process_time 



def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de películas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un género")
    print("6- Crear ranking")
    print("0- Salir")




def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1

#hola 

def loadCSVFile (file, tipo_lista, cmpfunction=None, sep=";"):
    """
    Carga un archivo csv a una lista
    Args:
        file
            Archivo csv del cual se importaran los datos
        sep = ";"
            Separador utilizado para determinar cada objeto dentro del archivo
        Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None  
    """
    if tipo_lista == 1:
        lst = lt.newList("ARRAY_LIST") #Usando implementacion arraylist
    elif tipo_lista == 2:
        lst = lt.newList("SINGLE_LINKED") #Usando implementacion single linked
    #lst = lt.newList() #Usando implementacion linkedlist
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            for row in spamreader: 
                lt.addLast(lst,row)
    except:
        print("Hubo un error con la carga del archivo")
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución",t1_stop-t1_start,"segundos")
    
    return lst
def less(element1, element2):
    if int(element1['id']) < int(element2['id']):
        return True
    return False

def greater(element1, element2):
    if int(element1['id']) > int(element2['id']):
        return True
    return False


def cmpVoteAverage_less (movie1, movie2):
    return (float(movie1['vote_average']) > float(movie2['vote_average']))

def cmpVoteAverage_greater (movie1, movie2):
    return (float(movie1['vote_average']) < float(movie2['vote_average']))


def cmpVoteCount_less(movie1, movie2):
    return (float(movie1['vote_count']) > float(movie2['vote_count']))


def cmpVoteCount_greater(movie1, movie2):
    return (float(movie1['vote_count']) < float(movie2['vote_count']))

def conocerDirector(criteria, column, lst1, lst2):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    
    moviesCasting = lst2
    moviesDetails = lst1
    i = 1
    tamanio_casting = lt.size(moviesCasting)
    peliculasDirigidas = []
    suma = 0
    ids = []
    while i <= tamanio_casting:
        pelicula = lt.getElement(moviesCasting, i)
        director = pelicula['director_name']
        id_pelicula = pelicula['id']
        if director == criteria:
            j = 1
            tamanio_details = lt.size(moviesDetails)
            ids.append(id_pelicula)
        i += 1
    while j <= tamanio_details:
            p = lt.getElement(moviesDetails, j)
            id_p = p['\ufeffid']
            nombre_pelicula = p['original_title']
            voto = p['vote_average']
            if id_p in ids:
                peliculasDirigidas.append(nombre_pelicula)
                suma += float(voto)
            j += 1
    promedio = suma / len(peliculasDirigidas)
    return peliculasDirigidas,len(peliculasDirigidas), round(promedio, 2)



def conocerRanking(cant_peliculas, cmpfunction, tipo_ordenamiento: int, orden: int, movielist: list) -> list:
    """
    Retorna una lista con cierta cantidad de elementos ordenados por el criterio
    """
    if cmpfunction == 1:
        if orden == 1:
            cmpfunction = cmpVoteAverage_less
        else:
            cmpfunction = cmpVoteAverage_greater
    elif cmpfunction == 2:
        if orden == 1:
            cmpfunction = cmpVoteCount_less
        else:
            cmpfunction = cmpVoteCount_greater
    if tipo_ordenamiento == 1:
        ss.selectionSort(movielist, cmpfunction)
    elif tipo_ordenamiento == 2:
        ins.insertionSort(movielist, cmpfunction)
    else:
         shs.shellSort(movielist, cmpfunction)
    sublista = lt.subList(movielist, 1, cant_peliculas)
    i = 1
    nombres_peliculas = []
    while i <= cant_peliculas:
        elemento = lt.getElement(sublista, i)
        nombres_peliculas.append(elemento['original_title'])
        i += 1
    return nombres_peliculas

def conocerActor(nombre_actor: str, lst1: list, lst2: list) -> tuple:
    moviesCasting = lst2
    moviesDetails = lst1
    i = 1
    tamanio_casting = lt.size(moviesCasting)
    participacionPeliculas = []
    directores = {}
    suma = 0
    ids = []
    while i <= tamanio_casting:
        pelicula = lt.getElement(moviesCasting, i)
        director = pelicula['director_name']
        actor_1 = pelicula['actor1_name']
        actor_2 = pelicula['actor2_name']
        actor_3 = pelicula['actor3_name']
        actor_4 = pelicula['actor4_name']
        actor_5 = pelicula['actor5_name']
        nombres_actores = [actor_1,actor_2,actor_3,actor_4,actor_5]
        id_pelicula = pelicula['id']
        if nombre_actor in nombres_actores:
            ids.append(id_pelicula)
            tamanio_details = lt.size(moviesDetails)
            if director not in directores:
                directores[director] = 0
            directores[director] += 1
        i += 1
    j = 1
    while j <= tamanio_details:
            p = lt.getElement(moviesDetails, j)
            id_p = p['\ufeffid']
            nombre_pelicula = p['original_title']
            voto = p['vote_average']
            if id_p in ids:
                participacionPeliculas.append(nombre_pelicula)
                suma += float(voto)
            j += 1
    mayor = 0
    director_mejor = ''
    for d in directores:
        colaboraciones = directores[d]
        if colaboraciones > mayor:
            mayor = colaboraciones
            director_mejor = d
    promedio = suma / len(participacionPeliculas)
    return participacionPeliculas,len(participacionPeliculas), round(promedio, 2), director_mejor

def entenderGenero(genero: str, lst: list, tipo_lista: int) -> tuple:
    genero = genero.lower()
    if tipo_lista == 1:
        tipo_lista = 'ARRAY_LIST'
    else:
        tipo_lista = 'SINGLE_LINKED'
    nombres_peliculas = []
    peliculasGenero = lt.newList(tipo_lista, less)
    i = 1
    tamanio_details = lt.size(lst)
    suma = 0
    while i <= tamanio_details:
        pelicula = lt.getElement(lst, i)
        genre = pelicula['genres']
        genre = genre.lower()
        vote_count = pelicula['vote_count']
        nombre_pelicula = pelicula['original_title']
        if genero in genre:
            lt.addLast(peliculasGenero, pelicula)
            nombres_peliculas.append(nombre_pelicula)
            suma += int(vote_count)
        i += 1
    promedio = suma/len(nombres_peliculas)
    return nombres_peliculas, len(nombres_peliculas), round(promedio, 2), peliculasGenero

def crearRankingGenero(genero: str, cant_peliculas: int, lst: list, orden: int, cmpfunction: int, tipo_lista: int, tipo_ordenamiento: int) -> tuple:
    cmpfunction1 = ''
    if tipo_lista == 1:
        tipo_lista = 'ARRAY_LIST'
    else:
        tipo_lista = 'SINGLE_LINKED'
    if cmpfunction == 1:
        cmpfunction1 = 'vote_average'
        if orden == 1:
            cmpfunction = cmpVoteAverage_less
        else:
            cmpfunction = cmpVoteAverage_greater
    else:
        cmpfunction1 = 'vote_count'
        if orden == 1:
            cmpfunction = cmpVoteCount_less
        else:
            cmpfunction = cmpVoteCount_greater
    if orden == 1:
        orden = less
    else:
        orden = greater
    lista_peliculas_genero = entenderGenero(genero, lst, tipo_lista)[3]
    if tipo_ordenamiento == 1:
        ss.selectionSort(lista_peliculas_genero, cmpfunction)
    elif tipo_ordenamiento == 2:
        ins.insertionSort(lista_peliculas_genero, cmpfunction)
    elif tipo_ordenamiento == 3:
         shs.shellSort(lista_peliculas_genero, cmpfunction)
    sublista = lt.subList(lista_peliculas_genero, 1, cant_peliculas)
    nombres_peliculas = []
    suma = 0
    i = 1
    while i <= int(sublista['size']):
        pelicula = lt.getElement(sublista, i)
        nombre_pelicula = pelicula['original_title']
        nombres_peliculas.append(nombre_pelicula)
        criterio = pelicula[cmpfunction1]
        suma += float(criterio)
        i += 1
    promedio = suma / int(sublista['size'])
    return nombres_peliculas, round(promedio, 2)


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    lista1 = lt.newList()   # se require usar lista definida
    lista2 = lt.newList() 

    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1: cargar peliculas
                lista1 = loadCSVFile("Data/theMoviesdb/AllMoviesDetailsCleaned.csv",1) #llamar funcion cargar datos SmallMoviesDetailsCleaned
                print("Datos cargados, ",lista1['size']," elementos cargados")
                lista2 = loadCSVFile("Data/theMoviesdb/AllMoviesCastingRaw.csv", 1) #llamar funcion cargar datos MoviesCastingRaw-small
                print("Datos cargados, ",lista2['size']," elementos cargados")
            elif int(inputs[0])==2: #opcion 2: conocer ranking
                if lista1==None or lista1['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    cant_peliculas =int(input('¿Cuántas películas quieres ver?: \n'))
                    orden = int(input('¿Quieres una lista (1) Ascendente o (2) Descendente?:\n'))
                    criteria = int(input('¿Quieres por (1) Calificación promedio o (2) Número de votos?: \n'))
                    t1_start = process_time() #tiempo inicial
                    counter=conocerRanking(cant_peliculas, criteria, 3, orden, lista1) #filtrar una columna por criterio
                    if criteria == 1:
                        criteria = 'calificación promedio'
                    elif criteria == 2:
                        criteria = 'número de votos'

                    if orden == 1:
                        orden = 'ascendentemente'
                    else:
                        orden = 'descendentemente'  
                    
                    print("La lista de películas ordenada", orden, 'por el criterio de', criteria, 'son:')
                    for peliculas in counter:
                        print(peliculas)
                    t1_stop = process_time() #tiempo final
                    print("Tiempo de ejecución",t1_stop-t1_start,"segundos")
                        
            elif int(inputs[0])==3: #opcion 3
                if lista2==None or lista2['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    criteria =input('Ingrese el nombre del director: \n')
                    column = 'vote_average'
                    t1_start = process_time() #tiempo inicial
                    counter=conocerDirector(criteria,column,lista1, lista2)
                    print("La lista de todas las películas dirigidas por" + criteria + "es:")
                    for i in counter[0]:
                        print(i)
                    print("El total de películas dirigidas por " + criteria + " es: " + str(counter[1]))
                    print("El promedio de la calificación de sus películas es de: " + str(counter[2]))
                    t1_stop = process_time() #tiempo final
                    print("Tiempo de ejecución",t1_stop-t1_start,"segundos")


            elif int(inputs[0])==4: #opcion 4
                if lista2==None or lista2['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    nombre_actor = input('Ingrese el nombre del actor: \n')
                    t1_start = process_time() #tiempo inicial
                    counter = conocerActor(nombre_actor, lista1, lista2)
                    print('Las películas en las que', nombre_actor, 'ha participado son:')
                    for pelicula in counter[0]:
                        print(pelicula)
                    print('El total de películas en las que el actor ha participado es de:', counter[1])
                    print('El promedio de la calificación de las películas en las que el actor ha participado es de:', counter[2])
                    print('El nombre del director con el que ha hecho más colaboraciones es:', counter[3])
                    t1_stop = process_time() #tiempo final
                    print("Tiempo de ejecución",t1_stop-t1_start,"segundos")

            elif int(inputs[0])==5: #opcion 5
                if lista1==None or lista1['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    genero = input('Ingrese el género de películas que quiere entender: \n')
                    genero = genero.lower()
                    t1_start = process_time() #tiempo inicial
                    counter = entenderGenero(genero, lista1, 1)
                    print('La lista de todas las películas asociadas a', genero,'son:')
                    for pelicula in counter[0]:
                        print(pelicula)
                    print('El número de las películas asociadas a', genero,'es:', counter[1])
                    print('El promedio de votos del género', genero,'es de:', counter[2])
                    t1_stop = process_time() #tiempo final
                    print("Tiempo de ejecución",t1_stop-t1_start,"segundos")

            elif int(inputs[0])==6: #opcion 6
                if lista1==None or lista1['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    genero = input('Ingrese el género de película del cual desea un ranking: \n')
                    cant_peliculas =int(input('¿Cuantas películas quieres ver?: \n'))
                    orden = int(input('¿Quieres una lista (1) Ascendente o (2) Descendente?: \n'))
                    criteria = int(input('¿Quieres por (1) Calificación promedio o (2) Número de votos?: \n'))

                    t1_start = process_time() #tiempo inicial
                    counter=crearRankingGenero(genero, cant_peliculas, lista1, orden, criteria, 1, 3) #filtrar una columna por criterio  
                    if criteria == 1:
                        criteria = 'calificación promedio'
                    else:
                        criteria = 'número de votos'

                    if orden == 1:
                        orden = 'ascendentemente'
                    else:
                        orden = 'descendentemente'
                    
                    print("La lista de películas del género", genero, 'ordenada', orden, 'por el criterio de', criteria, 'son:')
                    for peliculas in counter[0]:
                        print(peliculas)
                    print('El promedio de', criteria, 'de las películas del género', genero, 'es de:', counter[1])
                    t1_stop = process_time() #tiempo final
                    print("Tiempo de ejecución",t1_stop-t1_start,"segundos")

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()