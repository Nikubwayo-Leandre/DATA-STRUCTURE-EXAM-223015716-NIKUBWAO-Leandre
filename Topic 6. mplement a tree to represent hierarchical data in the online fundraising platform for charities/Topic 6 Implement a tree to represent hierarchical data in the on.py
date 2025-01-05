from tkinter import *
from tkinter import ttk


# Tree Node Class
class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


# Tkinter GUI for Tree Management
class HierarchicalTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hierarchical Data - Online Fundraising Platform")
        self.root.geometry("800x600")

        # Root node of the tree
        self.tree_root = TreeNode("Charities")

        # Set up UI
        self.setup_ui()

    def setup_ui(self):
        # Frame for user input
        input_frame = Frame(self.root, padx=10, pady=10)
        input_frame.pack(fill=X)

        Label(input_frame, text="Parent Node").grid(row=0, column=0, padx=10, pady=5)
        self.parent_node_var = StringVar()
        Entry(input_frame, textvariable=self.parent_node_var).grid(row=0, column=1, padx=10, pady=5)

        Label(input_frame, text="New Node").grid(row=1, column=0, padx=10, pady=5)
        self.new_node_var = StringVar()
        Entry(input_frame, textvariable=self.new_node_var).grid(row=1, column=1, padx=10, pady=5)

        Button(input_frame, text="Add Node", command=self.add_node).grid(row=2, column=0, padx=10, pady=10)
        Button(input_frame, text="Display Tree", command=self.display_tree).grid(row=2, column=1, padx=10, pady=10)

        # Frame for tree display
        tree_frame = Frame(self.root, padx=10, pady=10)
        tree_frame.pack(fill=BOTH, expand=True)

        Label(tree_frame, text="Tree Hierarchy", font=("Arial", 16)).pack(pady=10)

        self.tree_view = ttk.Treeview(tree_frame, columns=("Node"), show="tree", height=20)
        self.tree_view.pack(fill=BOTH, expand=True)

    def find_node(self, current_node, node_name):
        """Recursively search for a node by name."""
        if current_node.name == node_name:
            return current_node
        for child in current_node.children:
            found_node = self.find_node(child, node_name)
            if found_node:
                return found_node
        return None

    def add_node(self):
        """Add a new node to the tree."""
        parent_name = self.parent_node_var.get()
        new_node_name = self.new_node_var.get()

        if not parent_name or not new_node_name:
            self.show_popup("Error", "Parent and New Node names are required.")
            return

        # Find parent node
        parent_node = self.find_node(self.tree_root, parent_name)
        if parent_node:
            # Add new node
            parent_node.add_child(TreeNode(new_node_name))
            self.show_popup("Success", f"Added node '{new_node_name}' under '{parent_name}'.")
            self.parent_node_var.set("")
            self.new_node_var.set("")
        else:
            self.show_popup("Error", f"Parent node '{parent_name}' not found.")

    def display_tree(self):
        """Display the tree hierarchy in the GUI."""
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        self.add_tree_to_view(self.tree_root)

    def add_tree_to_view(self, node, parent=""):
        """Recursively add nodes to the tree view."""
        item_id = self.tree_view.insert(parent, "end", text=node.name)
        for child in node.children:
            self.add_tree_to_view(child, item_id)

    def show_popup(self, title, message):
        """Display a popup message."""
        popup = Toplevel(self.root)
        popup.title(title)
        Label(popup, text=message, font=("times new roman", 14)).pack(padx=20, pady=20)
        Button(popup, text="OK", command=popup.destroy).pack(pady=10)


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = HierarchicalTreeApp(root)
    root.mainloop()
