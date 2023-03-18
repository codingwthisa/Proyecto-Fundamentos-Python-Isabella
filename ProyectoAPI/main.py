from api import get_data
from ui import get_user_input

def main():
    # Pedir al usuario los valores que desea buscar
    departamento, municipio, cultivo, cantidad = get_user_input()

    # Obtener los datos de la API
    data = get_data(departamento, municipio, cultivo, cantidad)

if __name__ == '__main__':
    main()



