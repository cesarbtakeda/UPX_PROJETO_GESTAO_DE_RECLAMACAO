import os
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

# Termos a serem removidos do texto
TERMOS_DESNECESSARIOS = [
    "Número do pedido", "*****", "Compartilhe", "Publicidade", "Droga Raia",
    "Reputação da empresa:", "BOM", "7.8", "/ 10", "Compare", "Ver página da empresa",
    "Está com problemas com", "?", "Reclamar", "‌", "No app do Reclame AQUI você analisa sites suspeitos com mais facilidade!",
    "Análise:"
]

def baixar_pagina(url, output_path):
    """Função otimizada para Kali Linux com wget"""
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    
    cmd = [
        'wget',
        '--quiet',
        '--show-progress',
        '--no-check-certificate',
        '-L',
        '-O', str(output_path),
        '--header', f'User-Agent: {user_agent}',
        url
    ]
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Erro ao baixar {url}: {e}\n")
        return False
    except Exception as e:
        print(f"\n[!] Erro inesperado: {e}\n")
        return False

def tratar_reclamacao(texto):
    """Limpa o texto das reclamações"""
    if not texto:
        return ""
        
    # Remove termos indesejados
    for termo in TERMOS_DESNECESSARIOS:
        texto = texto.replace(termo, "")
    
    # Remove múltiplos espaços e quebras de linha
    return " ".join(texto.split())

def selecionar_arquivo():
    """Seleciona automaticamente ou pede ao usuário qual arquivo usar"""
    txt_files = list(Path(".").glob("*.txt"))
    
    if not txt_files:
        print("\n[!] Nenhum arquivo .txt encontrado na pasta atual!")
        return None
        
    if len(txt_files) == 1:
        return txt_files[0]
        
    print("\nArquivos .txt encontrados:")
    for i, arquivo in enumerate(txt_files, 1):
        print(f"{i} - {arquivo.name}")
    
    while True:
        try:
            opcao = int(input("\nSelecione o número do arquivo com as URLs: "))
            if 1 <= opcao <= len(txt_files):
                return txt_files[opcao-1]
            print("[!] Opção inválida!")
        except ValueError:
            print("[!] Digite apenas números!")

def extrair_e_analisar_reclamacoes():
    """Função que será chamada pela interface gráfica"""
    main()  # Chama a função principal que já existe
    return True

def main():
    print("\n=== EXTRAIR RECLAMAÇÕES - RECLAME AQUI ===")
    
    # Seleciona arquivo com URLs
    arquivo_urls = selecionar_arquivo()
    if not arquivo_urls:
        return
        
    # Lê URLs
    try:
        with open(arquivo_urls, 'r', encoding='utf-8') as f:
            urls = [linha.strip() for linha in f if linha.strip()]
    except Exception as e:
        print(f"\n[!] Erro ao ler arquivo: {e}\n")
        return
    
    if not urls:
        print("\n[!] Nenhuma URL válida encontrada no arquivo!\n")
        return
    
    # Prepara diretórios
    html_dir = Path("html_files")
    reclam_dir = Path("reclamacoes")
    html_dir.mkdir(exist_ok=True)
    reclam_dir.mkdir(exist_ok=True)
    
    output_file = reclam_dir / "reclamacoes.txt"
    
    print(f"\n► Processando {len(urls)} URLs...\n")
    
    reclamacoes = []
    for i, url in enumerate(urls, 1):
        print(f"Baixando URL {i}/{len(urls)}...")
        html_file = html_dir / f"pagina_{i}.html"
        
        if baixar_pagina(url, html_file):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    
                    # Extrai reclamações
                    divs = soup.find_all("div", {"data-testid": "complaint-content-container"})
                    for div in divs:
                        texto = tratar_reclamacao(div.get_text())
                        if texto:
                            reclamacoes.append(texto)
                            
            except Exception as e:
                print(f"[!] Erro ao processar {html_file.name}: {e}")
    
    # Salva resultados
    if reclamacoes:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n;\n".join(reclamacoes))
        print(f"\n✔ Concluído! Reclamações salvas em: {output_file}\n")
    else:
        print("\n[!] Nenhuma reclamação foi encontrada!\n")

if __name__ == "__main__":
    main()
