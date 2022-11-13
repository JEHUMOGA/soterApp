import json

print("hola")

with open('roots/empleados.json') as file:
    data = json.load(file)
    print('Tamaño:', data['tamano'])
    print('precio:', data['precio'])
    print('toppongs:', data['toppings'])
    print('cliente:', data['cliente'])
    print('')


'''
"tamano": "mediana",
	"precio": 15.67,
	"toppings": ["champinones", "queso extra", "pepperoni", "albahaca"],
	"cliente": {
		"nombre": "Jane Doe",
		"telefono": "455-344-234",
		"correo": "janedoe@email.com"
	}
'''