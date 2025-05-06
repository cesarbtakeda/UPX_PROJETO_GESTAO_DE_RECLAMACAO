import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from pathlib import Path
import pegar_urls   
import reclamacoes  

class InterfaceReclamacoes:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Reclamações")
        self.root.geometry("450x300")
        self.root.configure(bg="#f0f0f0")
        
        self.reclam_dir = Path("reclamacoes")
        self.reclam_dir.mkdir(exist_ok=True)
        self.arquivo_saida = self.reclam_dir / "reclamacoes.txt"
        
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.map("TButton",
                  background=[("active", "#4CAF50"), ("!active", "#2196F3")],
                  foreground=[("active", "black"), ("!active", "black")])

        main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(expand=True)

        title_label = tk.Label(main_frame, text="Gerenciador de Reclamações",
                              font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=(0, 20))

        self.btn_pegar_urls = ttk.Button(main_frame, text="🔗 Pegar URLs", command=self.pegar_urls, width=20)
        self.btn_pegar_urls.pack(pady=10)

        self.btn_pegar_reclamacoes = ttk.Button(main_frame, text="📝 Pegar Reclamações", command=self.pegar_reclamacoes, width=20)
        self.btn_pegar_reclamacoes.pack(pady=10)

        self.btn_abrir_reclamacoes = ttk.Button(main_frame, text="📂 Abrir Reclamações", command=self.abrir_reclamacoes, width=20)
        self.btn_abrir_reclamacoes.pack(pady=10)

        footer_label = tk.Label(main_frame, text="Feito com ❤️ por xAI", font=("Helvetica", 8), bg="#f0f0f0", fg="#666")
        footer_label.pack(pady=(20, 0))

    def pegar_urls(self):
        try:
            pegar_urls.obter_urls()  # Só executa o script pegar_urls.py
            messagebox.showinfo("Sucesso", "URLs obtidas com sucesso!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao pegar URLs: {e}", parent=self.root)

    def pegar_reclamacoes(self):
        try:
            reclamacoes.extrair_e_analisar_reclamacoes()  # Só executa o script reclamacoes.py
            messagebox.showinfo("Sucesso", "Reclamações extraídas e salvas!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao pegar reclamações: {e}", parent=self.root)

    def abrir_reclamacoes(self):
        try:
            if self.arquivo_saida.exists():
                webbrowser.open(str(self.arquivo_saida))  # Só abre o arquivo
            else:
                messagebox.showwarning("Aviso", "Nenhum arquivo de reclamações encontrado!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir reclamações: {e}", parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceReclamacoes(root)
    root.mainloop()
