import json
import os
import re
import time


def main():
    """Esta función lista todas las opciones del menú y las ejecuta en caso las
        sean elegidas"""

    print("""
    ------------------------------
     SISTEMA DE INVENTARIO FERCHI
    ------------------------------
    1. Registrar producto.
    2. Buscar producto.
    3. Actualizar stock.
    4. Eliminar producto.

    0. Salir.
        """
          )

    while True:
        opcion = input("Ingresa el número de la acción que deseas realizar: ")

        if re.fullmatch(r"\d+", opcion):
            opcion = int(opcion)
            break

        else:
            print("POR FAVOR, INGRESA UNA OPCIÓN VÁLIDA.")

    if opcion == 1:
        registrar_producto()

    elif opcion == 2:
        buscar_productos()

    elif opcion == 3:
        actualizar_stock()

    elif opcion == 4:
        eliminar_producto()

    elif opcion == 0:
        limpiar_terminal()
        exit()

    else:
        limpiar_terminal()
        print("POR FAVOR, INGRESA UNA OPCIÓN VÁLIDA. RECUERDA NO INCLUIR ESPACIOS.")
        main()


def registrar_producto():
    """Crea un diccionario con los atributos ingresados y los adiciona en la lista inventario"""

    limpiar_terminal()

    titulo = validar_valor("TÍTULO")

    autor = validar_valor("AUTOR")

    categoria = validar_valor("CATEGORÍA")
    limpiar_terminal()

    while True:
        precio = input("""
INGRESA EL PRECIO DEL PRODUCTO
(o escriba 0 para volver al menú principal): """)
        if precio == "0":
            limpiar_terminal()
            main()

        elif re.fullmatch(r"\d+(\.\d+)?", precio):
            precio = float(precio)

            limpiar_terminal()

            break
        else:
            print("\nNO SE PERMITEN LETRAS NI CARACTERES ESPECIALES.")

    while True:
        stock = input("""
INGRESA EL STOCK INICIAL DEL PRODUCTO
(o escriba 0 para volver al menú principal): """)
        if stock == "0":
            limpiar_terminal()
            main()

        elif re.fullmatch(r"^\d+$", stock):
            stock = int(stock)

            nombre_id = max(d["id"] for d in inventario)
            nombre_id += 1

            limpiar_terminal()

            break
        else:
            print("\nNO SE PERMITEN LETRAS NI CARACTERES ESPECIALES.")

    diccionario = {"id": nombre_id, "titulo": titulo, "autor": autor,
                   "categoria": categoria, "precio": precio, "stock": stock}

    inventario.append(diccionario)

    actualizar_archivo_inventario(
        r"libreria_inventario.json", inventario)
    limpiar_terminal()
    opcion = input("""
El libro se ingresó correctamente. 

presione 0 para volver al menú principal o enter para salir: """)
    if opcion == "0":
        limpiar_terminal()
        main()


def buscar_productos():
    limpiar_terminal()
    print("""
    ------------------------------
            MENÚ DE BÚSQUEDA
    ------------------------------
    1. Buscar por título          
    2. Buscar por autor
    3. Buscar por categoría      
    4. Búsqueda general

    0. Volver al menú principal"""
          )

    while True:

        opcion = input("""
Ingresa el número de la acción que deseas realizar: """)

        if opcion == "0":
            limpiar_terminal()
            main()
        if re.fullmatch(r"\d+", opcion):
            opcion = int(opcion)
            break

        else:
            print("""
POR FAVOR, INGRESA UNA OPCIÓN VÁLIDA.""")

    if opcion == 1:
        limpiar_terminal()
        titulo = input("Ingrese la palabra o frase del título a buscar: ")
        while True:
            if titulo == "0":
                limpiar_terminal()
                main()
                break
            elif titulo == "1":
                buscar_productos()
                break
            elif buscar_coincidencias(titulo, "titulo", inventario):
                break
            else:
                opcion = input("""
No se encontraron resultados coincidentes.
(Presiones 1 para volver a buscar o 0 para regresar al menú principal): """)
                if opcion == "1":
                    buscar_productos()
                elif opcion == "0":
                    main()

    elif opcion == 2:
        limpiar_terminal()
        autor = input("Ingrese nombre o/y apellido del autor a buscar: ")
        while True:
            if autor == "0":
                limpiar_terminal()
                main()
                break
            elif autor == "1":
                buscar_productos()
                break
            elif buscar_coincidencias(autor, "autor", inventario):
                break
            else:
                opcion = input("""
No se encontraron resultados coincidentes.
(Presiones 1 para volver a buscar o 0 para regresar al menú principal): """)
                if opcion == "1":
                    buscar_productos()
                elif opcion == "0":
                    main()

    elif opcion == 3:
        limpiar_terminal()
        categoria = input(
            "Ingrese la palabra o frase de la categoría a buscar: ")
        while True:
            if categoria == "0":
                limpiar_terminal()
                main()
                break
            elif categoria == "1":
                buscar_productos()
                break
            elif buscar_coincidencias(categoria, "categoria", inventario):
                break
            else:
                opcion = input("""
No se encontraron resultados coincidentes.
(Presiones 1 para volver a buscar o 0 para regresar al menú principal): """)
                if opcion == "1":
                    buscar_productos()
                elif opcion == "0":
                    main()

    elif opcion == 4:
        limpiar_terminal()
        todas_categorias = ["titulo", "autor", "categoria"]
        valor = input("Ingrese el término de la búsqueda: ")

        while True:
            if valor == "0":
                limpiar_terminal()
                main()
                break
            elif valor == "1":
                buscar_productos()
                break

            elif buscar_coincidencias(valor, todas_categorias, inventario):
                break
            else:
                opcion = input("""
No se encontraron resultados coincidentes.
(Presiones 1 para volver a buscar o 0 para regresar al menú principal): """)
                if opcion == "1":
                    limpiar_terminal()
                    buscar_productos()
                elif opcion == "0":
                    limpiar_terminal()
                    main()

    eleccion = input("""
                   
1. Buscar de nuevo.                                  
0. Vover a menú principal. 
                         
Ingrese una opción: """)
    if eleccion == "1":
        buscar_productos()
    elif eleccion == "0":
        main()


def actualizar_stock():
    """Esta actualiza el stock de un diccionario de la lista y actualizar el archivo"""
    limpiar_terminal()
    futuro_stock = 0

    id_libro = input("""
INGRESE EL ID DEL LIBRO. SI AÚN NO LO SABE CONSULTE LA OPCION DE BÚSQUEDA.
(o escriba 0 para volver al menú principal): """)

    while True:

        if id_libro == "0":
            limpiar_terminal()
            main()
            return

        elif re.fullmatch(r"^\d+$", id_libro):
            id_libro = int(id_libro)
            i, item = buscar_id(id_libro, inventario)

            if item is None:
                print("El ID no existe")
                time.sleep(2)
                actualizar_stock()

            print(f"{item['titulo']} tiene actualmente {item['stock']}")
            futuro_stock = input("Ingrese nuevo Stock: ")
            item["stock"] = futuro_stock

            actualizar_archivo_inventario(
                r"libreria_inventario.json", inventario)

            eleccion = input("""  
EL STOCK SE MODIFICÓ CORRECTAMENTE.
               
1. Buscar de nuevo.                                  
0. Modificar otro stock. 
                         
Ingrese una opción: """)

            if eleccion == "1":
                actualizar_stock()
            elif eleccion == "0":
                main()

            break

        else:
            print("ID NO EXISTENTE")

            time.sleep(2)

            actualizar_stock()


def eliminar_producto():
    """Esta función elimina un diccionario de la lista y actualizar el archivo"""
    limpiar_terminal()
    while True:
        id_libro = input("""
INGRESE EL ID DEL LIBRO HA ELIMINAR. SI AÚN NO LO SABE CONSULTE LA OPCION DE BÚSQUEDA.
(o escriba 0 para volver al menú principal): """)

        if id_libro == "0":
            limpiar_terminal()
            main()
            return

        elif re.fullmatch(r"^\d+$", id_libro):
            id_libro = int(id_libro)
            i, item = buscar_id(id_libro, inventario)

            if item is None:
                print("El ID no existe")
                time.sleep(2)
                eliminar_producto()

            del inventario[i]

            actualizar_archivo_inventario(
                r"libreria_inventario.json", inventario)

            eleccion = input("""  
EL LIBRO SE ELIMINÓ CORRECTAMENTE.
               
1. Eliminar otro libro.                                  
0. Vover a menú principal. 
                         
Ingrese una opción: """)

            if eleccion == "1":
                eliminar_producto()
            elif eleccion == "0":
                main()

            break

        else:
            print("ID NO EXISTENTE")

            time.sleep(2)

            eliminar_producto()


def buscar_id(libro_id, inventario):

    for i, item in enumerate(inventario):

        if libro_id == item["id"]:
            return i, item

    return None, None


def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def regresar_al_menu(opcion):
    # Retorna el menú principal

    if opcion == "0":
        main()


def cargar_inventario_desde_archivo(ruta_archivo):
    """
    Carga diccionarios desde un archivo en una lista y la devuelve.
    Suponemos que el archivo tiene un diccionario por línea.
    Devuelve una lista de diccionarios.
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as lector_archivo:
        inventario = json.load(lector_archivo)

    return inventario


def actualizar_archivo_inventario(ruta_archivo, inventario):
    """
    Actualiza la lista de diccionarios del archivo que contiene todo el
    inventario. Actuando como una base de datos. 

    """
    with open(ruta_archivo, 'w', encoding='utf-8') as file:
        json.dump(inventario, file, indent=4)


inventario = cargar_inventario_desde_archivo(
    r"libreria_inventario.json")


def validar_valor(campo):
    limpiar_terminal()

    while True:

        valor = input(f"""
INGRESA {campo} DEL PRODUCTO
(o escriba 0 para volver al menú principal): """)
        if valor == "0":
            limpiar_terminal()
            main()

        elif valor.strip() == "":

            print("POR FAVOR INGRESA UN VALOR.")

        elif re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", valor):
            break
        print("NO SE PERMITEN NÚMEROS, VACÍOS, NI CARACTERES ESPECIALES.")
    return valor


def buscar_coincidencias(texto_buscado, tipo, inventario):
    lista_coincidencias = []
    for i, item in enumerate(inventario):

        if texto_buscado == "0":
            main()

        if isinstance(tipo, list):
            for campo in tipo:
                if texto_buscado.upper() in item[campo].upper():
                    lista_coincidencias.append(item)
                    break

        elif texto_buscado.upper() in item[f"{tipo}"].upper():
            lista_coincidencias.append(item)
    if lista_coincidencias:
        print("""

------------------------------------------------------------------------------------------------
|  ID  |            TÍTULO           |         AUTOR        |   CATEGORÍA   |  PRECIO  | STOCK |
------------------------------------------------------------------------------------------------""")

        for libro in lista_coincidencias:
            print(f"| {libro['id']:<5}"
                  f"| {libro['titulo']:<28}"
                  f"| {libro['autor']:<21}| {libro['categoria']:<14}"
                  f"| {libro['precio']:<9}| {libro['stock']:<6}|")

    return lista_coincidencias


main()
