import os

class CacheLine:
    def __init__(self, line_size):
        self.tag = None
        self.data = [0] * line_size
        self.LRU_counter = 0

class CacheSet:
    def __init__(self, associativity, line_size):
        self.lines = [CacheLine(line_size) for _ in range(associativity)]

    def access(self, tag):
        for line in self.lines:
            if line.tag == tag:  # Si encontramos el tag
                line.LRU_counter = max([l.LRU_counter for l in self.lines]) + 1
                return True  # Es un hit

        # Si no encontramos el tag, es un miss y reemplazamos el menos recientemente usado
        least_recently_used = min(self.lines, key=lambda x: x.LRU_counter)
        least_recently_used.tag = tag
        least_recently_used.LRU_counter = max([l.LRU_counter for l in self.lines]) + 1
        return False

class Cache:
    def __init__(self, size, line_size, associativity):
        self.size = size
        self.line_size = line_size
        self.associativity = associativity
        self.set_count = size // (line_size * associativity)
        self.sets = [CacheSet(associativity, line_size) for _ in range(self.set_count)]

    def access(self, address):
        address_bin = bin(int(address, 16))[2:].zfill(32)
        index_size = len(bin(self.set_count - 1)[2:])
        tag_size = 32 - index_size - len(bin(self.line_size - 1)[2:])

        tag = int(address_bin[:tag_size], 2)
        index = int(address_bin[tag_size:tag_size+index_size], 2)

        return self.sets[index].access(tag)

def main():
    while True:
        cache_size = int(input("Introduce el tamaño del caché (32 a 128 KB): ")) * 1024  # convertir a bytes
        line_size = int(input("Introduce el tamaño de línea del caché (32 a 128 bytes): "))
        associativity = int(input("Introduce la asociatividad (4 a 16 ways): "))

        cache = Cache(cache_size, line_size, associativity)

        hits, misses = 0, 0

        with open("trace.out", 'r') as file:
            for line in file:
                if not line.startswith('#'):  # Sólo procesar las líneas que comienzan con '#'
                    continue
                parts = line.strip().split()
                LS, address, IC = int(parts[1]), parts[2], int(parts[3])
                if cache.access(address):
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
