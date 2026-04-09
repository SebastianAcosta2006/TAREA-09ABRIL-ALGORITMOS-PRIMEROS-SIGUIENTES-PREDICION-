"""
primeros siguientes y prediccion
"""

from typing import Dict, List, Set, Tuple

# constantes para simbolos especiales
VACIO = "ε"
FIN_CADENA = "$"

class AnalizadorGramatical:
    def __init__(self):
        self.axioma = "S"
        self.no_terminales = ["S", "A", "B", "C", "D"]
        self.terminales = ["uno", "dos", "tres", "cuatro", "cinco", "seis"]
        
        self.reglas: Dict[str, List[List[str]]] = {
            "S": [
                ["A", "B", "uno"],
            ],
            "A": [
                ["dos", "B"],
                [VACIO],
            ],
            "B": [
                ["C", "D"],
                ["tres"],
                [VACIO],
            ],
            "C": [
                ["cuatro", "A", "B"],
                ["cinco"],
            ],
            "D": [
                ["seis"],
                [VACIO],
            ],
        }
        
        self.primeros: Dict[str, Set[str]] = {nt: set() for nt in self.no_terminales}
        self.siguientes: Dict[str, Set[str]] = {nt: set() for nt in self.no_terminales}

    def es_no_terminal(self, simbolo: str) -> bool:
        return simbolo in self.no_terminales

    def obtener_primero_secuencia(self, secuencia: List[str]) -> Set[str]:
        """Calcula el conjunto PRIMERO para una lista de símbolos (una producción)."""
        resultado = set()
        puede_ser_vacio = True
        
        for simbolo in secuencia:
            if simbolo == VACIO:
                break
            
            if not self.es_no_terminal(simbolo):
            
                resultado.add(simbolo)
                puede_ser_vacio = False
                break
            else:
               
                conjunto_nt = self.primeros[simbolo]
                resultado.update(conjunto_nt - {VACIO})
                
                if VACIO not in conjunto_nt:
                    puede_ser_vacio = False
                    break
        
        if puede_ser_vacio:
            resultado.add(VACIO)
            
        return resultado

    def calcular_todos_los_primeros(self):
        """Itera hasta que los conjuntos PRIMEROS dejen de cambiar."""
        while True:
            cambio_detectado = False
            for nt, alternativas in self.reglas.items():
                tamanio_inicial = len(self.primeros[nt])
                
                for der in alternativas:
                  
                    self.primeros[nt].update(self.obtener_primero_secuencia(der))
                
                if len(self.primeros[nt]) > tamanio_inicial:
                    cambio_detectado = True
            
            if not cambio_detectado:
                break

    def calcular_todos_los_siguientes(self):
        """Itera hasta que los conjuntos SIGUIENTES se estabilicen."""
        self.siguientes[self.axioma].add(FIN_CADENA)
        
        continuar = True
        while continuar:
            continuar = False
            for cabeza, producciones in self.reglas.items():
                for cuerpo in producciones:
                    for i, simbolo in enumerate(cuerpo):
                        if self.es_no_terminal(simbolo):
                            tamanio_previo = len(self.siguientes[simbolo])
                            
                           
                            resto = cuerpo[i + 1:]
                            
                            if not resto:
                                
                                self.siguientes[simbolo].update(self.siguientes[cabeza])
                            else:
                               
                                primeros_del_resto = self.obtener_primero_secuencia(resto)
                                self.siguientes[simbolo].update(primeros_del_resto - {VACIO})
                                
                                
                                if VACIO in primeros_del_resto:
                                    self.siguientes[simbolo].update(self.siguientes[cabeza])
                            
                            if len(self.siguientes[simbolo]) > tamanio_previo:
                                continuar = True

    def generar_predicciones(self) -> Dict[str, List[Set[str]]]:
        """Calcula PRED(A -> alfa) basándose en PRIMEROS y SIGUIENTES ya calculados."""
        mapa_prediccion = {nt: [] for nt in self.no_terminales}
        for nt, alts in self.reglas.items():
            for der in alts:
                prim_der = self.obtener_primero_secuencia(der)
                p_set = prim_der - {VACIO}
                
                if VACIO in prim_der:
                    p_set.update(self.siguientes[nt])
                
                mapa_prediccion[nt].append(p_set)
        return mapa_prediccion



def formatear(conjunto: Set[str]) -> str:
   
    prioridad = {VACIO: "0", FIN_CADENA: "1"}
    ordenados = sorted(list(conjunto), key=lambda x: prioridad.get(x, "2" + x))
    return "{ " + ", ".join(ordenados) + " }"

def ejecutar_programa():
    app = AnalizadorGramatical()
    
    print("\n--- REGLAS DE LA GRAMÁTICA ---")
    conteo = 1
    for nt, alts in app.reglas.items():
        for a in alts:
            print(f"  ({conteo:2d}) {nt} -> {' '.join(a)}")
            conteo += 1

    
    app.calcular_todos_los_primeros()
    app.calcular_todos_los_siguientes()
    predicciones = app.generar_predicciones()

    print("\n--- CONJUNTOS PRIMEROS ---")
    for nt in app.no_terminales:
        print(f"  PRIMERO({nt:1}) = {formatear(app.primeros[nt])}")

    print("\n--- CONJUNTOS SIGUIENTES ---")
    for nt in app.no_terminales:
        print(f"  SIGUIENTE({nt:1}) = {formatear(app.siguientes[nt])}")

    print("\n--- CONJUNTOS DE PREDICCIÓN ---")
    regla_id = 1
    for nt in app.no_terminales:
        for i, der in enumerate(app.reglas[nt]):
            cuerpo_str = " ".join(der)
            print(f"  [{regla_id:2d}] {nt} -> {cuerpo_str:<22} PRED = {formatear(predicciones[nt][i])}")
            regla_id += 1

if __name__ == "__main__":
    ejecutar_programa()
