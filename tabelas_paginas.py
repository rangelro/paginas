import random
import time

def converter_tamanho(tamanho_str):

    # Remove espaços em branco antes e depois
    tamanho_str = str(tamanho_str).strip().upper()
    
    # Se estiver vazio, retorna 0
    if not tamanho_str:
        return 0

    # Dicionário de unidades para conversão
    unidades = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
    
    # Separa números das letras ("4GB" -> "4" e "GB")
    numero_str = ""
    unidade_str = ""
    
    for char in tamanho_str:
        if char.isdigit() or char == '.':
            numero_str += char
        else:
            unidade_str += char
    
    unidade_str = unidade_str.strip()
    
    # Tenta converter o número
    try:
        if not numero_str:
            # Caso o usuário digite algo sem número, ignora ou retorna 0
            return 0
        valor = float(numero_str)
    except ValueError:
        return 0
        
    # Multiplica pela unidade correspondente
    if unidade_str in unidades:
        return int(valor * unidades[unidade_str])
    
    # Se não tiver unidade, assume bytes
    return int(valor)

def formatar_bytes(tamanho):
    # Formata os bytes em uma string legível
    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamanho < 1024.0:
            return f"{tamanho:.2f} {unidade}"
        tamanho /= 1024.0
    return f"{tamanho:.2f} PB"

def simular_paginacao():
    print("="*60)
    print("      TRABALHO 5 - SIMULADOR DE TABELA DE PÁGINAS")
    print("="*60)
    print("Pressione ENTER para usar os valores padrão ( do slide).")
    
    # --- ENTRADAS ---
    try:
        mf_in = input("1. Tamanho da Memória Física (Padrão 2GB): ").strip() or "2GB"
        ml_in = input("2. Tamanho da Memória Lógica (Padrão 4GB): ").strip() or "4GB"
        tp_in = input("3. Tamanho da Página (Padrão 4KB): ").strip() or "4KB"
        el_in = input("4. Endereço Lógico a buscar (Padrão 20500): ").strip() or "20500"
        
        # Converte inputs para inteiros
        mem_fisica = converter_tamanho(mf_in)
        mem_logica = converter_tamanho(ml_in)
        tam_pagina = converter_tamanho(tp_in)
        end_logico = int(el_in)

        # Validação básica
        if tam_pagina == 0:
            print("\n[ERRO] O tamanho da página não pode ser 0.")
            return

        # Verifica se o endereço lógico está dentro da memória lógica
    except Exception as e:
        print(f"\n[ERROCRÍTICO] Entrada inválida: {e}")
        return

    # --- CÁLCULOS LÓGICOS (MMU) ---
    # Pagina = Endereço / TamanhoPagina 
    num_pagina = end_logico // tam_pagina
    
    # Deslocamento = Endereço % TamanhoPagina 
    deslocamento = end_logico % tam_pagina
    
    # Total de páginas e molduras (frames de memória física disponíveis)
    total_paginas = mem_logica // tam_pagina
    total_molduras = mem_fisica // tam_pagina

    # Simulação da Tabela de Páginas (Mapeamento)

    # Se o endereço for 20500 e página 4KB, a página é a 5.
    # O exemplo diz que a Página 5 está na Moldura 3.
    if num_pagina == 5 and tam_pagina == 4096:
        moldura = 3
        nota_exemplo = "(Fixo pelo PDF)"
    else:
        # Se não, sorteia uma moldura válida aleatória
        if total_molduras > 0:
            moldura = random.randint(0, total_molduras - 1)
        # Caso a memória física seja 0 (invalida), define moldura como 0
        else:
            moldura = 0 
        nota_exemplo = "(Simulado)"

    # Cálculo do Endereço Físico
    # Endereço Físico = (Moldura * TamanhoPagina) + Deslocamento
    end_fisico = (moldura * tam_pagina) + deslocamento

    # --- CÁLCULOS DE 2 NÍVEIS ---
    # Simulação para arquitetura de 32 bits (10 bits PT1, 10 bits PT2)
    # A tabela de 1024 entradas
    entradas_nivel = 1024 
    indice_pt1 = num_pagina // entradas_nivel
    indice_pt2 = num_pagina % entradas_nivel


    # --- CÁLCULO DE TEMPO (TLB) ---
    # Hit: TLB + Memória | Miss: TLB + 2*Memória
    tempo_tlb = 20   # ns
    tempo_mem = 100  # ns
    
    # Sorteia se houve HIT ou MISS na TLB (cache)
    # Coloquei chance de 90% de hit pra simular localidade na TLB
    tlb_hit = random.random() < 0.90
    
    if tlb_hit:
        tempo_total = tempo_tlb + tempo_mem
        status_tlb = "TLB HIT (Rápido - Encontrado na Cache)"
    else:
        tempo_total = tempo_tlb + (2 * tempo_mem)
        status_tlb = "TLB MISS (Lento - Buscou na Tabela em RAM)"

    # --- SAÍDA DE DADOS (VISUALIZAÇÃO) ---
    print("\n" + "="*60)
    print(f"RESULTADOS DA TRADUÇÃO (MMU)")
    print("="*60)
    print(f"Configuração:")
    print(f" > Memória Lógica: {formatar_bytes(mem_logica)} ({total_paginas} páginas)")
    print(f" > Memória Física: {formatar_bytes(mem_fisica)} ({total_molduras} molduras)")
    print(f" > Tamanho Página: {formatar_bytes(tam_pagina)}")
    print("-" * 60)
    
    print(f"Endereço Lógico Fornecido: {end_logico}")
    print(f"1. Número da Página Virtual: {num_pagina}")
    print(f"2. Deslocamento (Offset):    {deslocamento}")
    print(f"3. Número da Moldura Física: {moldura} {nota_exemplo}")
    print(f"4. Endereço Físico Gerado:   {end_fisico}")
    print("-" * 60)
    print(f"Performance (Simulação):")
    print(f" > Status: {status_tlb}")
    print(f" > Tempo Total de Acesso: {tempo_total} ns")
    print("="*60)

    # --- VISUALIZAÇÃO GRÁFICA ASCII ---
    print("\n[ VISUALIZAÇÃO GRÁFICA DO MAPEAMENTO - 1 NÍVEL ]")
    print(f"      CPU (Gera Endereço Lógico)")
    print(f"       |")
    print(f"       v")
    print(f"  +---------+--------------+")
    print(f"  | PÁGINA  | DESLOCAMENTO |  -> [{num_pagina} | {deslocamento}]")
    print(f"  +---------+--------------+")
    print(f"       |          |")
    print(f"       v          | (copia)")
    print(f" [ Tabela de Páginas ]")
    print(f" ---------------------")
    print(f" |  Idx  |  Moldura  |")
    print(f" |  ...  |    ...    |")
    print(f" |  {num_pagina:03}  |    {moldura:03}    | <--- Mapeamento Localizado")
    print(f" |  ...  |    ...    |")
    print(f" ---------------------")
    print(f"            |")
    print(f"            v")
    print(f"  +---------+--------------+")
    print(f"  | MOLDURA | DESLOCAMENTO |  -> [{moldura} | {deslocamento}]")
    print(f"  +---------+--------------+")
    print(f"       |")
    print(f"       v")
    print(f" [ MEMÓRIA FÍSICA (RAM) ] -> Acesso ao endereço {end_fisico}")

    print("\n\n[ VISUALIZAÇÃO GRÁFICA - 2 NÍVEIS (Multinível) ]")
    print(f"Endereço Lógico dividido: [ PT1: {indice_pt1} | PT2: {indice_pt2} | Offset: {deslocamento} ]")
    print("       |")
    print("       v")
    print(f"[ Diretório Externo (PT1) ]")
    print(f"   | Entrada {indice_pt1} aponta para Tabela PT2... |")
    print("       |")
    print("       v")
    print(f"[ Tabela Interna (PT2) ]")
    print(f"   | Entrada {indice_pt2} contém a Moldura {moldura}...  |")
    print("       |")
    print("       v")
    print(f"[ Endereço Físico Final: {end_fisico} ]")
    print("\n")

if __name__ == "__main__":
    simular_paginacao()