''' Derivador de Producto de Polinomios mediante reescritura
    Presentado por:
    -Deisy Viviana Lara Sisa
    -Julian David Nieto Rodriguez
    -Andres Giovanni Sastoque Gonzalez''' 

import tkinter as tk
from tkinter import messagebox

# ======== FUNCIONES PARA CALCULAR LA DERIVADA =========

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


def derivada_a_string(derivada):
    """ Convierte la lista de tuplas (coef, exp) que representa la
        derivada en una cadena en sintaxis Latex.

    Args:
        tupla (List[Tuple[int, int]]): Lista que representa la derivada de
                                        un polinomio

    Returns:
        String: derivada en formato Latex.
    """
    resultado = ""
    primer_termino = True
    for coef, exp in derivada:
        signo = "+" if coef > 0 else "-"
        coef_abs = abs(coef)

        if exp == 0:
            termino = f"{coef_abs}"
        elif exp == 1:
            termino = f"{coef_abs}x"
        else:
            termino = f"{coef_abs}x^{exp}"

        if primer_termino:
            resultado += f"{'-' if coef < 0 else ''}{termino}"
            primer_termino = False
        else:
            resultado += f" {signo} {termino}"

    resultado_latex = "$$" + resultado + "$$"

    return resultado_latex if resultado else "0"

# ======== FUNCIONES DE LA INTERFAZ =========

derivada_final = ""

def ejecutar_proceso():
    ''' Función principal que se activa al presionar el botón "Calcular Derivada", ejecuta los
        procesos requeridos para calcular la derivada de un producto de polinomios. '''

    global derivada_final
    
    #Recibe la expresion en formato Latex que el usuario ingresa en el campo de entrada(Entry)
    entrada = entrada_latex.get()
    
    try:
        #Extrae cada uno de los dos polinomios
        pol1, pol2 = extraer_polinomios_latex(entrada)
        texto_resultado.set(f"Polinomio 1: {pol1}\nPolinomio 2: {pol2}")

        #Pasa el polinomio a una tupla(coeficiente,exponente)
        tuplas1 = latex_a_tuplas(pol1)
        tuplas2 = latex_a_tuplas(pol2)
        texto_resultado.set(texto_resultado.get() + f"\n\nTuplas P1: {tuplas1}\nTuplas P2: {tuplas2}")

        #Realiza la multiplicacion de los polinomios para facilitar el calculo de la derivada
        producto = multiplicar_polinomios(tuplas1, tuplas2)
        texto_resultado.set(texto_resultado.get() + f"\n\nProducto: {producto}")

        #Calcula la derivada
        derivada = derivar_polinomio(producto)
        texto_resultado.set(texto_resultado.get() + f"\n\nDerivada (tuplas): {derivada}")

        #Convierte la derivada a una cadena
        derivada_str = derivada_a_string(derivada)
        derivada_final = derivada_str
        texto_resultado.set(texto_resultado.get() + f"\n\nDerivada final:\n{derivada_str}")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        texto_resultado.set("")

def copiar_derivada():
    ''' Copia la derivada al portapapeles para que el usuario la pueda utilizar en latex'''
    if derivada_final:
        ventana.clipboard_clear()
        ventana.clipboard_append(derivada_final)
        messagebox.showinfo("Copiado", "La derivada ha sido copiada al portapapeles.")
    else:
        messagebox.showwarning("Vacío", "No hay derivada para copiar.")

def resetear():
    ''' Reinicia la interfaz para que el usuario pueda ingresar un nuevo producto de polinomios
        sin cerrar la ventana'''
    
    entrada_latex.delete(0, tk.END)
    texto_resultado.set("")

# ======== INTERFAZ =========

color_fondo = "#1e3a5f"  # Azul oscuro
color_texto = "white"

#Crea la ventana principal
ventana = tk.Tk()
ventana.title("Derivada de Producto de Polinomios")
ventana.geometry("600x520")

#Color de fondo
ventana.configure(bg=color_fondo)  

tk.Label(ventana, text="Ingrese la expresión LaTeX:", font=("Arial", 12),
         bg=color_fondo, fg=color_texto).pack(pady=10)

entrada_latex = tk.Entry(ventana, width=50)
entrada_latex.pack(pady=5)

frame_botones = tk.Frame(ventana, bg=color_fondo)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Calcular Derivada", command=ejecutar_proceso,
          bg="#40658c", fg="white", activebackground="#305070").pack(side="left", padx=10)

tk.Button(frame_botones, text="Reset", command=resetear,
          bg="#40658c", fg="white", activebackground="#305070").pack(side="left", padx=10)

tk.Button(frame_botones, text="Copiar Derivada", command=copiar_derivada,
          bg="#40658c", fg="white", activebackground="#305070").pack(side="left", padx=10)

texto_resultado = tk.StringVar()
tk.Label(
    ventana,
    textvariable=texto_resultado,
    justify="center",               
    font=("Courier", 10, "bold"),   
    anchor="center",                
    bg=color_fondo,
    fg=color_texto
).pack(padx=20, pady=10, fill="both", expand=True)


ventana.mainloop()

