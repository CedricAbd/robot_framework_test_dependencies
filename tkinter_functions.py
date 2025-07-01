import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

APPLICATION_TITLE = "Robot Framework test dependencies viewer"
TYPE_COLORS = {
    "root": "skyblue",
    "resource": "orange",
    "library": "lightgreen",
    "variable": "lightcoral"
}

def launch_gui(graph: nx.DiGraph) -> None:
    """
    Creates and starts the graphic application.

    Args:
        graph (nx.DiGraph): Graph to display
    """
    # Creates the Tkinter window.
    root = tk.Tk()
    root.title(APPLICATION_TITLE)
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w}x{h}+0+0")
    # Creates a paned window (with resizable panes).
    paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)
    # Creates a frame to display the graph.
    graph_frame = ttk.Frame(paned_window)
    paned_window.add(graph_frame, weight=4)
    # Creates a frame to list dependencies.
    tree_frame = ttk.Frame(paned_window)
    paned_window.add(tree_frame, weight=1)
    # Creates the graph and its toolbar.
    fig, ax = plt.subplots()
    pos = graphviz_layout(graph, prog="dot")
    labels = {node: f"{node}\n({graph.nodes[node].get('type', '')})" for node in graph.nodes}
    node_colors = [TYPE_COLORS.get(graph.nodes[n].get("type", ""), "gray") for n in graph.nodes]
    nx.draw_networkx(
        graph,
        pos,
        ax=ax,
        labels=labels,
        node_color=node_colors,
        node_size=900,
        font_size=8,
        arrows=True
    )
    ax.axis("off")
    fig.tight_layout(pad=0)
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    toolbar = NavigationToolbar2Tk(canvas, graph_frame)
    toolbar.update()
    toolbar.pack(side=tk.TOP, fill=tk.X)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Creates a tree view.
    tree_view = ttk.Treeview(tree_frame, columns=("File", "Type"), show="headings")
    tree_view.heading("File", text="File")
    tree_view.heading("Type", text="Type")
    tree_view.column("File", anchor="w", width=250)
    tree_view.column("Type", anchor="center", width=80)
    tree_view.pack(fill=tk.BOTH, expand=True)

    # Inserts dependency rows.
    for node in graph.nodes:
        tree_view.insert("", tk.END, values=(node, graph.nodes[node].get("type", "unknown")))

    # Creates export button.
    ttk.Button(
        tree_frame,
        text="Export dependencies",
        command=lambda: export_dependencies(root, tree_view)
    ).pack(fill=tk.X, pady=5, padx=5)

    # Starts application loop.
    root.mainloop()

def export_dependencies(root: tk.Tk, tree: ttk.Treeview) -> None:
    """
    Opens a save dialog and writes dependencies in a file.

    Args:
        root (tk.Tk): Tkinter application
        tree (ttk.Treeview): Tree to export
    """
    file_path = filedialog.asksaveasfilename(
        parent=root,
        title="Save dependencies as",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
    )
    if not file_path:
        return
    try:
        dependencies = [tree.item(item_id, "values")[0] for item_id in tree.get_children("")]
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(dependencies))
        messagebox.showinfo("Export:", f"Dependencies saved to:\n{file_path}", parent=root)
    except Exception as e:
        messagebox.showerror("Error:", f"Unable to save file:\n{e}", parent=root)
