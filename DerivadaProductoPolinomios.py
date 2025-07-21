def extraer_polinomios_latex(expr):
    """ Extrae dos polinomios escritos como (polinomio1)(polinomio2) en LaTeX.
        Asume que los polinomios están entre paréntesis y no hay anidamientos.

    Args:
        expr (str): Expresión en LaTeX como "(2x^2 + 3x + 1)(x - 4)"

    Returns:
        Polinomio 1 y Polinomio 2
    """

    #Busca las posiciones de los parentesis
    primera_apertura = expr.index('(')
    primer_cierre = expr.index(')', primera_apertura)
    segunda_apertura = expr.index('(', primer_cierre)
    segundo_cierre = expr.index(')', segunda_apertura)

    #Extrae el contenido de cada polinomio
    polinomio1 = expr[primera_apertura + 1:primer_cierre]
    polinomio2 = expr[segunda_apertura + 1:segundo_cierre]

    return polinomio1, polinomio2

def latex_a_tuplas(latex_expr, variable='x'):

    """ Reescribe un polinomio en formato latex a la forma (coeficiente, exponente)

    Args:
        expr (str): Expresión en LaTeX como "2x^2 + 3x + 1"
        variable (str): La variable que se utiliza en el polinomio, por defecto "x"

    Returns:
        List[Tuple(int, int)]: resultado
    """

    #Se eliminan todos los espacios y se verifica que el primer termino tenga signo
    expr = latex_expr.replace(' ', '')
    if expr[0] not in '+-':
        expr = '+' + expr

    #Se extraen los terminos uno por uno
    terminos = []
    i = 0
    while i < len(expr):
        signo = expr[i]
        j = i + 1
        while j < len(expr) and expr[j] not in '+-':
            j += 1
        terminos.append(expr[i:j])
        i = j

    resultado = []

    #Se extrae el signo del termino y se elimina para analizarlo algebraicamente
    for termino in terminos:
        signo = 1
        if termino[0] == '-':
            signo = -1
        termino = termino[1:]

        #Determina el coeficiente y exponente de cada termino
        if variable in termino:
            partes = termino.split(variable)
            coef_str = partes[0]

            if coef_str == '':
                coef = 1
            else:
                coef = int(coef_str)

            if '^' in termino:
                exp_str = partes[1][1:]
                exponente = int(exp_str)
            else:
                exponente = 1

        #Establece el coeficiente y exponente si el termino es una constante
        else:
            coef = int(termino)
            exponente = 0

        #Aplica el signo al coeficiente del termino y lo guarda  en la lista resultado como (coeficiente, exponente)
        resultado.append((signo * coef, exponente))

    return resultado


def multiplicar_polinomios(polinomio1, polinomio2):
    """ Calcula el producto de dos polinomios.

    Args:
      polinomio1: Una lista de tuplas, donde cada tupla representa un término
                  del polinomio en la forma (coeficiente, exponente).
                  Ejemplo: [(2, 3), (5, 1), (-1, 0)] representa 2x^3 + 5x - 1.

      polinomio2: Similar a polinomio1.

    Returns:
      List[Tuple(int, int)]: resultado_lista
    """

    #Se crea un diccionario donde se almacenaran exponente:coeficiente
    resultado = {}

    #Se realiza la multiplicacion de los coeficientes y la suma de los exponentes de los polinomios
    for coeficiente1, exponente1 in polinomio1:
        for coeficiente2, exponente2 in polinomio2:
            coeficiente_nuevo = coeficiente1 * coeficiente2
            exponente_nuevo = exponente1 + exponente2

            #Si el exponente ya se encuentra en el diccionario, se suman los coeficientes
            if exponente_nuevo in resultado:
                resultado[exponente_nuevo] += coeficiente_nuevo

            #Si el exponente no se encuentra en el diccionario, se agrega al diccionario en forma exponente:coeficiente
            else:
                resultado[exponente_nuevo] = coeficiente_nuevo

    #Convertir el diccionario de resultados a una lista de tuplas
    resultado_lista = [(coef, exp) for exp, coef in resultado.items()]

    #Se ordena en funcion del exponente
    resultado_lista.sort(key=lambda item: item[1], reverse=True)

    return resultado_lista


def derivar_polinomio(tuplas):
    """ Calcula la derivada de un polinomio dado como lista de tuplas (coef, exp).

    Args:
        tuplas (List[Tuple[int, int]]): Lista que representa un polinomio.
            Ejemplo: [(2, 3), (5, 1), (-1, 0)] representa 2x^3 + 5x - 1

    Returns:
        List[Tuple[int, int]]: derivada.
    """
    derivada = []

    #Recorre cada termino para derivarlo
    for coef, exp in tuplas:
        if exp == 0:
            #Si el exponente es cero, el termino es una constante. La derivada de una constante es cero
            continue

        nuevo_coef = coef * exp
        nuevo_exp = exp - 1

        #Se guarda el resultado de la derivada como una tupla (coeficiente, exponente)
        derivada.append((nuevo_coef, nuevo_exp))

    return derivada

def main():
    """ Funcion principal que ejecuta los procesos requeridos para calcular la derivada
        de un producto de polinomios.

        Args:
            No recibe argumentos
        """
    #Recibe la expresion en formato Latex que el usuario ingresa
    latex= input("Ingrese la expresión a derivar en formato '(polinomio 1)(polinomio 2)': ")

    #Extrae cada uno de los dos polinomios
    polinomio1,polinomio2 = extraer_polinomios_latex(latex)

    #Pasa el polinomio a una tupla(coeficiente,exponente)
    tupPolinomio1 = latex_a_tuplas(polinomio1)
    tupPolinomio2 = latex_a_tuplas(polinomio2)

    #Realiza la multiplicacion de los polinomios para facilitar el calculo de la derivada
    mult= multiplicar_polinomios(tupPolinomio1,tupPolinomio2)

    #Calcula la derivada
    derivada=derivar_polinomio(mult)

    #Imprime el resultado
    print("La derivada del producto es:")
    primer_termino= 0
    for coeficiente, exponente in derivada:
      signo = "+" if coeficiente > 0 else "-"
      coef = abs(coeficiente)

      if exponente == 0:
        if primer_termino == 0:
          print(f"{coeficiente}", end=" ")
        else:
          print(signo,f"{coef}", end=" ")

      elif exponente == 1:
        if primer_termino == 0:
          print(f"{coeficiente}x", end=" ")
        else:
          print(signo,f"{coef}x", end=" ")

      else:
          if primer_termino == 0:
            print(f"{coeficiente}x^{exponente}", end=" ")
          else:
            print(signo,f"{coef}x^{exponente}", end=" ")

      primer_termino += 1

main()
