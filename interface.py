import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from pathlib import Path
import pegar_urls   
import reclamacoes
import sys
import os
from PIL import Image, ImageTk  # Adicionado para visualização de imagens

# Garante que o Python encontra graficos.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import graficos

class InterfaceReclamacoes:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Reclamações")
        self.root.geometry("500x450")  # Aumentado para acomodar novos botões
        self.root.configure(bg="#f0f0f0")
        
        self.reclam_dir = Path("reclamacoes")
        self.reclam_dir.mkdir(exist_ok=True)
        self.arquivo_saida = self.reclam_dir / "dados.txt"
        self.graficos_dir = Path("graficos")
        
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), padding=8)
        style.map("TButton", background=[("active", "#45a049")], foreground=[("active", "white")])

        main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(expand=True)

        title_label = tk.Label(main_frame, text="Gerenciador de Reclamações", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=(0, 10))

        # Botões em ordem lógica
        buttons = [
            ("🔗 Pegar URLs", self.pegar_urls),
            ("📝 Pegar Reclamações", self.pegar_reclamacoes),
            ("📊 Gerar Gráficos", self.gerar_graficos),
            ("🖼 Abrir Histograma", lambda: self.abrir_grafico("histograma_numero_palavras.png")),
            ("📈 Abrir Top Palavras", lambda: self.abrir_grafico("top_20_barras.png")),
            ("📂 Abrir Reclamações", self.abrir_reclamacoes)
        ]

        for text, command in buttons:
            btn = ttk.Button(main_frame, text=text, command=command, width=25)
            btn.pack(pady=5)

        tk.Label(main_frame, text="Feito por Cesar Augusto B", font=("Arial", 8), bg="#f0f0f0", fg="#666").pack(pady=(10, 0))

    def pegar_urls(self):
        try:
            pegar_urls.obter_urls()
            messagebox.showinfo("Sucesso", "URLs coletadas!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha: {e}", parent=self.root)

    def pegar_reclamacoes(self):
        try:
            reclamacoes.extrair_e_analisar_reclamacoes()
            messagebox.showinfo("Sucesso", "Reclamações salvas!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha: {e}", parent=self.root)

    def gerar_graficos(self):
        sucesso, msg = graficos.gerar_graficos()
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self.root)
        else:
            messagebox.showerror("Erro", msg, parent=self.root)

    def abrir_reclamacoes(self):
        try:
            if self.arquivo_saida.exists():
                webbrowser.open(str(self.arquivo_saida))
            else:
                messagebox.showwarning("Aviso", "Arquivo não encontrado!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha: {e}", parent=self.root)

    def abrir_grafico(self, nome_arquivo):
        try:
            caminho = self.graficos_dir / nome_arquivo
            if caminho.exists():
                # Abre em uma nova janela
                janela_grafico = tk.Toplevel(self.root)
                janela_grafico.title(f"Visualizar: {nome_arquivo}")
                
                # Carrega a imagem
                img = Image.open(caminho)
                img = img.resize((600, 400), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                
                # Mostra a imagem
                label = tk.Label(janela_grafico, image=img_tk)
                label.image = img_tk  # Mantém referência
                label.pack()
                
                # Botão para fechar
                tk.Button(janela_grafico, text="Fechar", command=janela_grafico.destroy).pack(pady=5)
            else:
                messagebox.showwarning("Aviso", f"Arquivo {nome_arquivo} não encontrado!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao abrir gráfico: {e}", parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceReclamacoes(root)
    root.mainloop()
