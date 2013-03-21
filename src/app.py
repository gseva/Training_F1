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
    entrada = None
    while True:
        entrada = raw_input("ingrese '1' para calcular cuil/cuit, '2' para verificar o q para salir:")
        if entrada == "q":
            break
        if entrada == "1":
            cuil = raw_input("ingrese su numero seguido por su DNI:")
            respuesta = devolver_codigo(cuil, "devolver")
            if len(respuesta) == 1:
                print "Su codigo es: "
        if entrada == "2":
            cuil = raw_input("ingrese su CUIL:")
            respuesta = verificar_cuil(cuil, "verificar")
        print respuesta
        print "*" * len(respuesta)
    print "salu2"


def captar_errores(cuil, opcion):
    try:
        int(cuil)
    except ValueError:
        return "incorrecto, tienen que ser numeros"
    print cuil
    if opcion == "verificar":
        if len(cuil) != 11:
            return "incorrecto, tiene que tener 11 digitos"
    if opcion == "devolver":
        if len(cuil) != 10:
            return "incorrecto, tiene que tener 10 digitos"
    return False


def devolver_codigo(cuil, opcion):
    respuesta = captar_errores(cuil, opcion)
    if respuesta:
        return respuesta

    verificacion = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    valor_1 = 0
    i = 0

    while i < len(verificacion):
        valor_1 += int(cuil[i]) * verificacion[i]
        print "int(cuil[i]): ", int(cuil[i]), "verificacion[i]: ", \
                                verificacion[i], "valor_1: ", valor_1
        i += 1

    valor_2 = valor_1 % 11
    print "valor_2: ", valor_2
    valor_3 = 11 - valor_2
    print "valor_3: ", valor_3
    codigo = None

    if valor_3 == 11:
        codigo = 0
    elif valor_3 == 10:
        codigo = 9
    else:
        codigo = valor_3
    print "codigo: ", codigo, "len(codigo):", len(str(codigo))
    return str(codigo)


def verificar_cuil(cuil, opcion):
    respuesta = devolver_codigo(cuil, opcion)
    if len(respuesta) == 1:
        if cuil.endswith(respuesta):
            return "cuil correcto, felicitaciones!"
        else:
            return "cuil incorrecto!"
    return respuesta


if __name__ == "__main__":
    main()
