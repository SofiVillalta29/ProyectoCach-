import os

class CacheLine:
    def __init__(self, line_size):
        self.tag = None #identifica si un dato está en la línea de caché, inicializado en cero
        self.data = [0] * line_size #los datos almacenados, comienzan en cero
        self.LRU_counter = 0 #contador para ver cuanto se usa un dato

class CacheSet:
    def __init__(self, associativity, line_size):
        self.lines = [CacheLine(line_size) for _ in range(associativity)] #Crea las líneas de caché de acuerdo a la asociatividad

    def access(self, tag):
        for line in self.lines:
            if line.tag == tag:  # Si encontramos el tag
                line.LRU_counter = max([l.LRU_counter for l in self.lines]) + 1 #recorre la lista de contadores LRU, agarra el valor maximo y le suma 1 asignándolo al más reciente
                return True  # Es un hit

        # Si no encontramos el tag, es un miss y reemplazamos el menos recientemente usado
        least_recently_used = min(self.lines, key=lambda x: x.LRU_counter)
        least_recently_used.tag = tag #se reemplaza el tag viejo por el tag nuevo
        least_recently_used.LRU_counter = max([l.LRU_counter for l in self.lines]) + 1
        return False

class Cache:
    def __init__(self, size, line_size, associativity):
        self.size = size
        self.line_size = line_size
        self.associativity = associativity
        self.set_count = size // (line_size * associativity) #calcula el número total de conjuntos de caché con datos de usario
        self.sets = [CacheSet(associativity, line_size) for _ in range(self.set_count)] #crea los conjuntos de caché

    def access(self, address):
        address_bin = bin(int(address, 16))[2:].zfill(32) #convierte la dirección hexaecimal del trace en entero y luego a binario de 32 bits
        index_size = len(bin(self.set_count - 1)[2:]) #declara el index como dirección de 32 bits
        tag_size = 32 - index_size - len(bin(self.line_size - 1)[2:]) #tamaño total menos offset menos index.

        tag = int(address_bin[:tag_size], 2) #después de calcular el tamaño se declara el tag con los bits de direccion requeridos para el tag
        index = int(address_bin[tag_size:tag_size+index_size], 2) #después de calcular el tamaño se declara el index con los bits de direccion requeridos para el index

        return self.sets[index].access(tag) #accede al conjunto de caché con índice calculado y llama al método access para ver si es hit o miss

def main():
    while True:
        cache_size = int(input("Introduce el tamaño del caché (32 a 128 KB): ")) * 1024  # convertir a bytes, valor ingresado por usuario para tamaño del caché
        line_size = int(input("Introduce el tamaño de línea del caché (32 a 128 bytes): ")) # valor ingresados por usuario para tamaño de línea
        associativity = int(input("Introduce la asociatividad (4 a 16 ways): ")) #valor ingresados por usuario para asociatividad

        cache = Cache(cache_size, line_size, associativity) #crea una instancia de la clase con los nuevos parámetros

        hits, misses = 0, 0 #inicaliza la cantidad de hits o misses

        with open("test.out", 'r') as file:
            for line in file:
                if line.startswith('#'):  # Sólo procesar las líneas que comienzan con '#'
                    parts = line.strip().split()
                    LS, address, IC = int(parts[1]), parts[2], int(parts[3])
                    if cache.access(address):  # Esta línea y las siguientes deben estar dentro del if
                        hits += 1
                    else:
                        misses += 1

        print(f"Hits: {hits}")
        print(f"Misses: {misses}")


        option = input("¿Quieres correr el programa de nuevo? (s/n): ")
        if option.lower() != 's':
            break

if __name__ == "__main__":
    main()
