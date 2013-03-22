'''
Created on 21/03/2013

Verificacion de CUIT/CUIL (generico)

El CUIL/CUIT consta de 11 numeros. Los 10 primeros (2+8) constituyen el
codigo de identificacion y el ultimo, el digito de verificacion. Para
obtener esta verificacion se procede de la siguiente forma:
A cada digito del codigo se lo multiplica por los siguientes numeros:
5,4,3,2,7,6,5,4,3,2 y cada valor obtenido se suma para obtener una
expresion (que llamaremos "valor 1").
A este valor 1 se le saca el resto de la division entera a 11. Se
obtiene de esta forma un numero del 0 al 10 que llamamos "valor 2"
Sacamos la diferencia entre 11 y el "valor 2", y obtenemos un valor
comprendido entre 1 y 11 (llamemosle "valor 3").
Si "valor 3" = 11, el codigo verificador es 9. En otro caso el digito
verificador sera el digito obtenido.

@author: sebastiang
'''


def main():
    """La funcion principal del programa, le hace preguntas al usuario
    y llama a funciones dependiendo de lo ingresado"""
    entrada = None
    while True:
        mensaje = "ingrese '1' para calcular cuil/cuit, "
        mensaje += "'2' para verificar o 'q' para salir:"
        entrada = raw_input(mensaje)
        print '*' * len(mensaje)
        if entrada == "q":
            break
        elif entrada == "1":
            respuesta = tomar_datos()
            if len(respuesta) == 1:
                respuesta = "Su codigo es: " + respuesta
        elif entrada == "2":
            cuil = raw_input("ingrese su CUIL:")
            respuesta = verificar_cuil(cuil, "verificar")
        else:
            continue
        print respuesta
        print "*" * len(mensaje)
    print "salu2"


def captar_errores(cuil, opcion):
    """Verifica si el ingreso son numeros y
    el correcto ingreso del CUIL o Numero+DNI"""
    try:
        int(cuil)
    except ValueError:
        return "incorrecto, tienen que ser numeros"
    if opcion == "verificar":
        if len(cuil) != 11:
            return "incorrecto, tiene que tener 11 digitos"
    if opcion == "devolver":
        if len(cuil) != 10:
            return "incorrecto, tiene que tener 10 digitos"
    return False


def devolver_codigo(cuil, opcion):
    """Calcula la ultima cifra (codigo) a partir de los diez
    numeros dados. Verifica si se le pasaron 10 u 11 numeros y
    luego calcula el codigo con los primeros 10 de la lista."""
    respuesta = captar_errores(cuil, opcion)
    if respuesta:
        return respuesta

    verificacion = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    valor_1 = 0
    i = 0

    while i < len(verificacion):
        valor_1 += int(cuil[i]) * verificacion[i]
        i += 1
    valor_2 = valor_1 % 11
    codigo = 11 - valor_2
    if codigo == 11:
        codigo = 0
    elif codigo == 10:
        codigo = 9
    return str(codigo)


def verificar_cuil(cuil, opcion):
    """Verifica si a los primeros 10 numeros del cuil pasado
    les corresponde el ultimo numero (codigo)"""
    respuesta = devolver_codigo(cuil, opcion)
    if len(respuesta) == 1:
        if cuil.endswith(respuesta):
            return "cuil correcto, felicitaciones!"
        else:
            return "cuil incorrecto!"
    return respuesta


def tomar_datos():
    """Toma los datos del usuario y forma la string del cuil,
    devuelve el codigo o la respuesta dek error"""
    mensaje = ("ingrese su el CUIL/CUIT es de: \n'm' para mujer \n")
    mensaje += ("'h' para hombre \n'e' para empresa")
    cuil = ""
    while not cuil:
        genero = raw_input(mensaje)
        if genero == 'm':
            cuil += "27"
        elif genero == 'h':
            cuil += "20"
        elif genero == 'e':
            cuil += "30"
        else:
            print "ingreso incorrecto \n", "*" * 20
    print cuil
    while True:
        dni = raw_input("ingrese su DNI:")
        if len(dni) != 8:
            print "DNI tiene que tener 8 cifras"
            print "*" * 20
        else:
            cuil += dni
            break
    print cuil
    return devolver_codigo(cuil, opcion="devolver")


if __name__ == "__main__":
    main()
