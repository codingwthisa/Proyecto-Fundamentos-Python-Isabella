def get_user_input():
    departamento = input("Ingrese el departamento a buscar: ")
    municipio = input("Ingrese el municipio a buscar: ")
    cultivo = input("Ingrese el cultivo a buscar: ")
    cantidad = int(input("Ingrese la cantidad de registros a consultar (máximo 2000): "))

    return departamento, municipio, cultivo, cantidad
