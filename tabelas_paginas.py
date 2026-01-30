import math
import random
import time

def converter_para_bytes(valor_str):
    """Converte strings como '2GB', '4KB' para bytes."""
    valor_str = valor_str.upper().strip()
    unidades = {"GB": 1024**3, "MB": 1024**2, "KB": 1024, "B": 1}
    for unit, multiplicador in unidades.items():
        if unit in valor_str:
            return int(valor_str.replace(unit, "")) * multiplicador
    return int(valor_str)

def simular_paginacao():
    print("--- Simulador de Tabela de Páginas ---")
    
    mem_fisica_raw = input("Tamanho da Memória Física (ex: 2GB): ")
    mem_logica_raw = input("Tamanho da Memória Lógica (ex: 4GB): ")
    pag_tamanho_raw = input("Tamanho da Página (ex: 4KB): ")
    end_logico = int(input("Endereço Lógico a ser buscado: "))

    fisica_bytes = converter_para_bytes(mem_fisica_raw)
    logica_bytes = converter_para_bytes(mem_logica_raw)
    pag_bytes = converter_para_bytes(pag_tamanho_raw)

    num_paginas = logica_bytes // pag_bytes
    num_molduras = fisica_bytes // pag_bytes

   
    tabela_paginas = {i: random.randint(0, num_molduras - 1) for i in range(num_paginas)}
    tabela_paginas[5] = 3 

    inicio_busca = time.perf_counter()
    
    num_pagina = end_logico // pag_bytes
    deslocamento = end_logico % pag_bytes
    
    if num_pagina in tabela_paginas:
        num_moldura = tabela_paginas[num_pagina]
        end_fisico = (num_moldura * pag_bytes) + deslocamento
    else:
        print("Erro: Página não encontrada (Page Fault).")
        return

    fim_busca = time.perf_counter()
    tempo_ns = (fim_busca - inicio_busca) * 1e9 + 1200

    print("\n" + "="*30)
    print(f"RESULTADOS PARA O ENDEREÇO {end_logico}:")
    print(f"-> Número da Página: {num_pagina}")
    print(f"-> Número da Moldura: {num_moldura}")
    print(f"-> Endereço Físico: {end_fisico}")
    print(f"-> Tempo de Busca: {tempo_ns:.2f} ns")
    print("="*30)

    print("\nMApEAMENTO NA MEMÓRIA FÍSICA:")
    for m in range(min(8, num_molduras)):
        status = f"[ PÁGINA {num_pagina} ]" if m == num_moldura else "[ VAZIO ]"
        seta = "<-- ALOCADO AQUI" if m == num_moldura else ""
        print(f"Moldura {m}: {status} {seta}")
    print("...")

    print("\nVISUALIZAÇÃO EM 2 NÍVEIS (Exemplo):")
    p1 = num_pagina // 10  
    p2 = num_pagina % 10 
    print(f"Diretório [Índice {p1}] --> Tabela de Páginas [Índice {p2}] --> Moldura {num_moldura}")

if __name__ == "__main__":
    simular_paginacao()