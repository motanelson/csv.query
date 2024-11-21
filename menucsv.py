import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import csv


class QueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Query Executor")
        self.root.configure(bg="black")

        # Menu principal
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Caixa de texto para exibir resultados
        self.result_text = tk.Text(root, bg="black", fg="white", wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Botão para carregar o arquivo .query
        self.load_button = tk.Button(
            root,
            text="Load .query File",
            bg="black",
            fg="white",
            command=self.load_query_file
        )
        self.load_button.pack(pady=10)

        # Botão para salvar os resultados
        self.save_button = tk.Button(
            root,
            text="Save Results",
            bg="black",
            fg="white",
            command=self.save_results
        )
        self.save_button.pack(pady=10)

    def load_query_file(self):
        query_path = filedialog.askopenfilename(filetypes=[("Query Files", "*.query")])
        if not query_path:
            return

        try:
            with open(query_path, "r") as file:
                reader = csv.reader(file)
                queries = list(reader)

            # Limpa os menus existentes
            self.menu_bar.delete(0, tk.END)

            for row in queries:
                if len(row) != 4:
                    continue

                menu_name, csv_file, query_column, result_columns = row
                query_column = query_column.strip()
                result_columns = list(map(int, result_columns.split()))

                # Cria um menu e associa a ação ao submenu
                menu = tk.Menu(self.menu_bar, tearoff=0)
                self.menu_bar.add_cascade(label=menu_name, menu=menu)
                menu.add_command(
                    label=f"Search in {csv_file}",
                    command=lambda cf=csv_file, qc=query_column, rc=result_columns: self.execute_query(cf, qc, rc)
                )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load .query file: {e}")

    def execute_query(self, csv_file, query_column, result_columns):
        # Perguntar o valor para a query
        search_value = simpledialog.askstring("Input", f"Enter value for '{query_column}':")
        if not search_value:
            return
        
        
        # Procurar no arquivo CSV
        try:
        
            with open(csv_file, "r") as file:
                reader =file.read()
                reader=reader.split("\n")
                results = []
                
                for row in reader:
                    rows=row.split(",")
                    
                    lensrow=len(row)
                    query_columns=int(query_column)
                    
                    try:
                        
                        if query_columns<=lensrow  and rows[query_columns].find(search_value)>-1 :
                            # Captura apenas as colunas desejadas
                            fl=""
                            for r in result_columns:
                                rr=""
                                rr=rows[int(r)]
                                
                                #int(r)
                                if r==0:
                                   
                                    fl=fl+rr
                                    
                                else:
                                    fl=fl+","+rr
                            print(fl)
                            results.append(fl)
                    except Exception as e:
                         pass
  
                if not results:
                    messagebox.showinfo("No Results", "No matching rows found.")
                else:
                    # Exibir os resultados na caixa de texto
                    self.result_text.delete(1.0, tk.END)
                    result="\n".join(results)
                    self.result_text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute query: {e}")

    def save_results(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not save_path:
            return

        try:
            with open(save_path, "w") as file:
                file.write(self.result_text.get(1.0, tk.END))
            messagebox.showinfo("Success", "Results saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = QueryApp(root)
    root.mainloop()

