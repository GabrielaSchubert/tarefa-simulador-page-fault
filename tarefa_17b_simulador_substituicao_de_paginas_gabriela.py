"""Tarefa 17b - simulador substituicao de paginas  - Gabriela.ipynb

Construa um simulador de algoritmos de substituição de páginas (capitulo 17). O simulador deve receber como entrada o tamanho da RAM (em quadros) e a sequência de referências a páginas de memória e gerar como saída o número de faltas de página geradas, para os algoritmos OPT, FIFO e LRU. Usar linguagem python.

Atencao: trabalho individual, trabalhos iguais serao considerados cola e receberao nota zero.

OBS: caso deseje ver o gráfico rode o código no google colab ou com matplotlib instalado.

"""

from collections import deque
import matplotlib.pyplot as plt

def fifo_trace(paginas, quadros, verbose=False):
    memoria = deque()
    faltas = 0
    steps = []
    for i, p in enumerate(paginas):
        hit = p in memoria
        if not hit:
            faltas += 1
            if len(memoria) < quadros:
                memoria.append(p)
            else:
                memoria.popleft()
                memoria.append(p)
        if verbose:
            steps.append((i, p, list(memoria), 'HIT' if hit else 'MISS'))
    return faltas, steps


def opt_trace(paginas, quadros, verbose=False):
    memoria = []
    faltas = 0
    steps = []
    n = len(paginas)
    for i, p in enumerate(paginas):
        hit = p in memoria
        if not hit:
            faltas += 1
            if len(memoria) < quadros:
                memoria.append(p)
            else:
                futuro = paginas[i+1:]
                farthest = None
                max_dist = -1
                for m in memoria:
                    if m in futuro:
                        dist = futuro.index(m)
                    else:
                        dist = float('inf')
                    if dist > max_dist:
                        max_dist = dist
                        farthest = m
                memoria.remove(farthest)
                memoria.append(p)
        if verbose:
            steps.append((i, p, list(memoria), 'HIT' if hit else 'MISS'))
    return faltas, steps


def lru_trace(paginas, quadros, verbose=False):
    memoria = []
    last_used = {}
    faltas = 0
    steps = []
    for i, p in enumerate(paginas):
        hit = p in memoria
        if not hit:
            faltas += 1
            if len(memoria) < quadros:
                memoria.append(p)
            else:
                lru_page = min(memoria, key=lambda x: last_used.get(x, -1))
                memoria.remove(lru_page)
                last_used.pop(lru_page, None)
                memoria.append(p)
        last_used[p] = i
        if verbose:
            steps.append((i, p, list(memoria), dict(last_used), 'HIT' if hit else 'MISS'))
    return faltas, steps


def parse_input_pages(s):
    if s.strip() == '':
        return []
    return list(map(int, s.split()))


def run_simulation(quadros, seq, verbose=False):

    fifo_res, fifo_steps = fifo_trace(seq, quadros, verbose)
    opt_res, opt_steps = opt_trace(seq, quadros, verbose)
    lru_res, lru_steps = lru_trace(seq, quadros, verbose)

    return {
        'FIFO': {'faltas': fifo_res, 'steps': fifo_steps},
        'OPT' : {'faltas': opt_res,  'steps': opt_steps},
        'LRU' : {'faltas': lru_res,  'steps': lru_steps},
        'quadros': quadros,
        'seq': seq
    }


def pretty_print_result(res, verbose=False):
    print("="*60)
    print("RESULTADOS DA SIMULAÇÃO")
    print(f"Tamanho da RAM (quadros): {res['quadros']}")
    print(f"Sequência de referências: {res['seq']}\n")
    for alg in ['FIFO','OPT','LRU']:
        print(f"{alg:4} -> Faltas de página: {res[alg]['faltas']}")
    print("="*60)

    if verbose:
        for alg in ['FIFO','OPT','LRU']:
            print(f"\n=== Trace: {alg} ===")
            steps = res[alg]['steps']
            for step in steps:
                if alg == 'LRU':
                    i, p, mem, last_used, status = step
                    print(f"i={i:2} page={p:2} -> {status} | memoria={mem} | last_used={last_used}")
                else:
                    i, p, mem, status = step
                    print(f"i={i:2} page={p:2} -> {status} | memoria={mem}")
            print("="*60)


def main():
    print("SIMULADOR DE SUBSTITUIÇÃO DE PÁGINAS (OPT, FIFO, LRU)")
    try:
        quadros = int(input("Informe o tamanho da RAM (número de quadros): ").strip())
    except Exception:
        print("Entrada inválida para quadros. Use inteiro positivo.")
        return

    seq_in = input("Informe a sequência de páginas (separe por espaço): ").strip()
    seq = parse_input_pages(seq_in)

    verb = input("Mostrar trace passo-a-passo? (s/n): ").strip().lower() in ['s','sim','y','yes']

    res = run_simulation(quadros, seq, verbose=verb)
    pretty_print_result(res, verbose=verb)
    return res


# Executa
resultado = main()


# GRÁFICO

if resultado is not None:
    seq = resultado['seq']

    xs = list(range(1, 8))
    fifo_vals, opt_vals, lru_vals = [], [], []

    for q in xs:
        r = run_simulation(q, seq)
        fifo_vals.append(r['FIFO']['faltas'])
        opt_vals.append(r['OPT']['faltas'])
        lru_vals.append(r['LRU']['faltas'])

    plt.figure(figsize=(10,6))
    plt.plot(xs, opt_vals, '-o', color='purple', label='OPT')
    plt.plot(xs, fifo_vals, '-*', color='green', label='FIFO')
    plt.plot(xs, lru_vals, '-x', color='blue', label='LRU')
    plt.xlabel("Número de quadros de RAM")
    plt.ylabel("Faltas de página")
    plt.title("Comparativo: string de referência (sem páginas iniciais)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.show()