import json
import os
import re


def main():
    """Esta función lista todas las opciones del menú y las ejecuta en caso las
        sean elegidas"""

    print("""
    ------------------------------
        SISTEMA DE INVENTARIO
    ------------------------------
    1. Registrar producto.
    2. Buscar producto.
    3. Actualizar stock.
    4. Eliminar producto.
    5. Reportes.

    0. Salir.
        """
          )

    opcion = input("Ingresa el número de la acción que deseas realizar: ")

    if opcion == "1":
        registrar_producto()

    elif opcion == "2":
        buscar_productos()

    elif opcion == "3":
        actualizar_stock()

    elif opcion == "4":
        eliminar_producto()

    elif opcion == "5":
        generar_reporte()

    elif opcion == "0":
        limpiar_terminal()

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

    while True:
        limpiar_terminal()
        precio = input("""
INGRESA EL PRECIO DEL PRODUCTO
(o escriba 0 para volver al menú principal): """)
        if precio == "0":
            limpiar_terminal()
            main()

        elif re.fullmatch(r"\d+(\.\d+)?", precio):
            precio = float(precio)

            break
        print("\nNO SE PERMITEN LETRAS NI CARACTERES ESPECIALES.")

    while True:
        limpiar_terminal()
        stock = input("""
¿CUÁNTOS PRODUCTOS DESEA REGISTRAR?
(o escriba 0 para volver al menú principal): """)

        if stock == "0":
            limpiar_terminal()
            main()

        elif re.fullmatch(r"\d+", stock):
            stock = int(stock)
            break

        print("NO SE PERMITEN LETRAS, CARACTERES ESPECIALES, NI DECIMALES.")

    diccionario = {"titulo": titulo, "autor": autor,
                   "categoria": categoria, "precio": precio, "stock": stock}

    inventario.append(diccionario)

    actualizar_archivo_inventario(
        r"C:\Users\SBOO\Desktop\libreria_inventario.json", inventario)
    limpiar_terminal()
    opcion = input("""
El libro se ingresó correctamente. 

presione 0 para volver al menú principal o enter para salir: """)
    if opcion == "0":
        limpiar_terminal()
        main()


def buscar_productos():
    print("""
    ------------------------------
            MENÚ DE BÚSQUEDA
    ------------------------------
    1. Buscar por título          
    2. Buscar por autor
    3. Buscar por categoría      
    3. Búsqueda general
          

    0. Volver al menú principal
        """
          )

    opcion = input("Ingresa el número de la acción que deseas realizar: ")


def actualizar_stock():
    limpiar_terminal()

    titulo_libro = input(
        """
    INGRESE EL TÍTULO DEL LIBRO PARA ACTUALIZAR EL STOCK: "
    (o escriba 0 para volver al menú principal)    """)

    if titulo_libro == "0":
        main()

    item, i = buscar_titulo(titulo_libro, inventario)

    if not item:

        actualizar_stock()

    print(f"{titulo_libro} tiene actualmente {item['stock']}")
    nuevo_stock = input("Ingrese nuevo Stock: ")

    item["stock"] = nuevo_stock
    inventario[i] = item

    actualizar_archivo_inventario(
        r"C:\Users\SBOO\Desktop\libreria_inventario.json", inventario)


#   print(f"Presione la tecla 'S' para salir. ")

def eliminar_producto():
    """Esta función elimina un diccionario de la lista y actualizar el archivo"""
    limpiar_terminal()

    libro_eliminado = input("""
    INGRESE EL TÍTULO DEL LIBRO HA ELIMINAR.
    (o escriba 0 para volver al menú principal): """)

    if libro_eliminado == "0":
        main()

    i, item = buscar_titulo(libro_eliminado, inventario)

    print(i, item)

    if not item:
        eliminar_producto()

    del inventario[item]

    actualizar_archivo_inventario(
        r"C:\Users\SBOO\Desktop\libreria_inventario.json", inventario)


def generar_reporte():

    pass


def buscar_titulo(titulo, inventario):

    for i, item in enumerate(inventario):

        if titulo == item["titulo"]:
            return item, i


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
    r"C:\Users\SBOO\Desktop\libreria_inventario.json")


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


def buscar_libro(valor,  inventario):

    for i, item in enumerate(inventario):

        if valor == item["titulo"]:
            return item, i

        if valor == item["autor"]:
            return item, i


main()


# print("""

# ---------------------------------------------------------------------------------------------
# |            TÍTULO           |         AUTOR         |    CATEGORÍA    |  PRECIO  |  STOCK |
# ---------------------------------------------------------------------------------------------""")

#    for libro in inventario:
#        print(f"| {libro['titulo']:<29}"
#              f"| {libro['autor']:<21}| {libro['categoria']:<16}"
#              f"| {libro['precio']:<9}| {libro['stock']:<7}|")
