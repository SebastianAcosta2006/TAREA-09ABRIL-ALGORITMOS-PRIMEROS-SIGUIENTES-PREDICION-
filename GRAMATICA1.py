"""
EJERCICIO 1 PRESENTACION 6
algoritmos para primeros siguientes y prediccion
primera gramatica de la presentacion 6
  S -> A uno B C
  S -> S dos
  A -> B C D
  A -> A tres
  A -> ε
  B -> D cuatro C tres
  B -> ε
  C -> cinco D B
  C -> ε
  D -> seis
  D -> ε
"""
from typing import Dict, List, Set, Tuple
# el simobolo para cadena vacia y fin de cadena
EPSILON = "ε"
EOF = "$"

# Representación de la gramática
def build_grammar() -> Tuple[str, List[str], List[str], Dict[str, List[List[str]]]]:
    axioma = "S"
    no_terminales = ["S", "A", "B", "C", "D"]
    terminales = ["uno", "dos", "tres", "cuatro", "cinco", "seis"]
    producciones: Dict[str, List[List[str]]] = {
        "S": [
            ["A", "uno", "B", "C"],
            ["S", "dos"],
        ],
        "A": [
            ["B", "C", "D"],
            ["A", "tres"],
            [EPSILON],
        ],
        "B": [
            ["D", "cuatro", "C", "tres"],
            [EPSILON],
        ],
        "C": [
            ["cinco", "D", "B"],
            [EPSILON],
        ],
        "D": [
            ["seis"],
            [EPSILON],
        ],
    }

    return axioma, no_terminales, terminales, producciones


# Utilidades

def es_terminal(simbolo: str, no_terminales: List[str]) -> bool:
    return simbolo not in no_terminales and simbolo != EPSILON


def es_no_terminal(simbolo: str, no_terminales: List[str]) -> bool:
    return simbolo in no_terminales


# PRIMEROS

def calcular_primeros(
    no_terminales: List[str],
    producciones: Dict[str, List[List[str]]],
) -> Dict[str, Set[str]]:
    primeros: Dict[str, Set[str]] = {nt: set() for nt in no_terminales}

    cambio = True
    while cambio:
        cambio = False
        for nt, alternativas in producciones.items():
            for alternativa in alternativas:
                antes = len(primeros[nt])

                if alternativa == [EPSILON]:
                    # Producción vacía: agrega ε directamente
                    primeros[nt].add(EPSILON)
                else:
                    # Recorre los símbolos de la alternativa
                    todos_anulables = True
                    for simbolo in alternativa:
                        if es_terminal(simbolo, no_terminales):
                            # Terminal: agrega el terminal y para
                            primeros[nt].add(simbolo)
                            todos_anulables = False
                            break
                        else:
                            # No-terminal: agrega PRIMERO(simbolo) \ {ε}
                            primeros[nt] |= primeros[simbolo] - {EPSILON}
                            if EPSILON not in primeros[simbolo]:
                                # Si no puede derivar ε, para
                                todos_anulables = False
                                break
                    if todos_anulables:
                        primeros[nt].add(EPSILON)

                if len(primeros[nt]) > antes:
                    cambio = True

    return primeros


def primero_de_cadena(
    cadena: List[str],
    primeros: Dict[str, Set[str]],
    no_terminales: List[str],
) -> Set[str]:
    resultado: Set[str] = set()
    todos_anulables = True

    for simbolo in cadena:
        if simbolo == EPSILON:
            break
        if es_terminal(simbolo, no_terminales):
            resultado.add(simbolo)
            todos_anulables = False
            break
        else:
            resultado |= primeros[simbolo] - {EPSILON}
            if EPSILON not in primeros[simbolo]:
                todos_anulables = False
                break

    if todos_anulables:
        resultado.add(EPSILON)

    return resultado


# algoritmo de siguientes
def calcular_siguientes(
    axioma: str,
    no_terminales: List[str],
    producciones: Dict[str, List[List[str]]],
    primeros: Dict[str, Set[str]],
) -> Dict[str, Set[str]]:
  
    siguientes: Dict[str, Set[str]] = {nt: set() for nt in no_terminales}
    siguientes[axioma].add(EOF)

    cambio = True
    while cambio:
        cambio = False
        for nt_izq, alternativas in producciones.items():
            for alternativa in alternativas:
                if alternativa == [EPSILON]:
                    continue
                for i, simbolo in enumerate(alternativa):
                    if not es_no_terminal(simbolo, no_terminales):
                        continue

                    antes = len(siguientes[simbolo])

                    # β = lo que sigue a 'simbolo' en esta alternativa
                    beta = alternativa[i + 1:]

                    if beta:
                        prim_beta = primero_de_cadena(beta, primeros, no_terminales)
                        # Agrega PRIMERO(β) \ {ε}
                        siguientes[simbolo] |= prim_beta - {EPSILON}
                        # Si β puede derivar ε, agrega SIGUIENTE(A)
                        if EPSILON in prim_beta:
                            siguientes[simbolo] |= siguientes[nt_izq]
                    else:
                        # X está al final de la producción
                        siguientes[simbolo] |= siguientes[nt_izq]

                    if len(siguientes[simbolo]) > antes:
                        cambio = True

    return siguientes


# algoritmo de prediccion

def calcular_prediccion(
    no_terminales: List[str],
    producciones: Dict[str, List[List[str]]],
    primeros: Dict[str, Set[str]],
    siguientes: Dict[str, Set[str]],
) -> Dict[str, Dict[int, Set[str]]]:
  
    prediccion: Dict[str, Dict[int, Set[str]]] = {}

    for nt, alternativas in producciones.items():
        prediccion[nt] = {}
        for idx, alternativa in enumerate(alternativas):
            prim = primero_de_cadena(alternativa, primeros, no_terminales)
            pred = prim - {EPSILON}
            if EPSILON in prim:
                pred |= siguientes[nt]
            prediccion[nt][idx] = pred

    return prediccion

def _fmt(conjunto: Set[str]) -> str:
    orden = {"ε": "0", "$": "1"}
    elementos = sorted(conjunto, key=lambda x: orden.get(x, "2" + x))
    return "{ " + ", ".join(elementos) + " }"

#resultados de primeros
def imprimir_primeros(
    no_terminales: List[str],
    primeros: Dict[str, Set[str]],
) -> None:
    print("CONJUNTOS PRIMEROS\n")
    for nt in no_terminales:
        print(f"  PRIMERO({nt}) = {_fmt(primeros[nt])}")

#resultados de siguientes
def imprimir_siguientes(
    no_terminales: List[str],
    siguientes: Dict[str, Set[str]],
) -> None:
    print("\nCONJUNTOS SIGUIENTES\n")
    for nt in no_terminales:
        print(f"  SIGUIENTE({nt}) = {_fmt(siguientes[nt])}")


def imprimir_prediccion(
    no_terminales: List[str],
    producciones: Dict[str, List[List[str]]],
    prediccion: Dict[str, Dict[int, Set[str]]],
) -> None:
    print("\nCONJUNTOS DE PREDICCIÓN")
    regla_global = 1
    for nt in no_terminales:
        for idx, alternativa in enumerate(producciones[nt]):
            lado_der = " ".join(alternativa)
            pred = prediccion[nt][idx]
            print(f"  [{regla_global:2d}] {nt} -> {lado_der:<25} PRED = {_fmt(pred)}")
            regla_global += 1




def main() -> None:
    axioma, no_terminales, terminales, producciones = build_grammar()

    print("\nGRAMÁTICA")
    regla_n = 1
    for nt, alternativas in producciones.items():
        for alt in alternativas:
            print(f"  [{regla_n:2d}] {nt} -> {' '.join(alt)}")
            regla_n += 1

    # algoritmo primeros
    primeros = calcular_primeros(no_terminales, producciones)
    print()
    imprimir_primeros(no_terminales, primeros)

    # algoritmo siguientes
    siguientes = calcular_siguientes(axioma, no_terminales, producciones, primeros)
    imprimir_siguientes(no_terminales, siguientes)

    # algoritmo prediccion
    prediccion = calcular_prediccion(
        no_terminales, producciones, primeros, siguientes
    )
    imprimir_prediccion(no_terminales, producciones, prediccion)

if __name__ == "__main__":
    main()
