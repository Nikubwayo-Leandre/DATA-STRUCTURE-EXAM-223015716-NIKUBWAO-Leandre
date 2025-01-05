from tkinter import *
from tkinter import ttk, messagebox


class Charity:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority


class QuickSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Sort - Charity Priority Sorting")
        self.root.geometry("800x600")

        # Charity data list
        self.charities = []

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # Input Frame
        input_frame = Frame(self.root, padx=10, pady=10)
        input_frame.pack(fill=X)

        Label(input_frame, text="Charity Name").grid(row=0, column=0, padx=10, pady=5)
        self.name_var = StringVar()
        Entry(input_frame, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        Label(input_frame, text="Priority (Higher = Important)").grid(row=1, column=0, padx=10, pady=5)
        self.priority_var = IntVar()
        Entry(input_frame, textvariable=self.priority_var).grid(row=1, column=1, padx=10, pady=5)

        Button(input_frame, text="Add Charity", command=self.add_charity).grid(row=2, column=0, padx=10, pady=10)
        Button(input_frame, text="Sort Charities", command=self.sort_charities).grid(row=2, column=1, padx=10, pady=10)

        # Treeview for displaying charities
        self.tree = ttk.Treeview(self.root, columns=("Name", "Priority"), show="headings", height=20)
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.tree.heading("Name", text="Charity Name")
        self.tree.heading("Priority", text="Priority")

    def add_charity(self):
        """Add a charity to the list."""
        name = self.name_var.get()
        priority = self.priority_var.get()

        if not name or priority <= 0:
            messagebox.showerror("Invalid Input", "Please enter a valid charity name and a positive priority value.")
            return

        # Add to charity list
        self.charities.append(Charity(name, priority))
        self.refresh_tree()

        # Clear inputs
        self.name_var.set("")
        self.priority_var.set("")

    def sort_charities(self):
        """Sort charities based on priority using Quick Sort."""
        if len(self.charities) == 0:
            messagebox.showerror("No Data", "No charities to sort.")
            return

        self.quick_sort(self.charities, 0, len(self.charities) - 1)
        self.refresh_tree()
        messagebox.showinfo("Sorting Complete", "Charities have been sorted by priority.")

    def quick_sort(self, array, low, high):
        """Quick Sort Algorithm."""
        if low < high:
            pivot_index = self.partition(array, low, high)
            self.quick_sort(array, low, pivot_index - 1)
            self.quick_sort(array, pivot_index + 1, high)

    def partition(self, array, low, high):
        """Partition function for Quick Sort."""
        pivot = array[high].priority
        i = low - 1
        for j in range(low, high):
            if array[j].priority > pivot:  # Sorting by descending priority
                i += 1
                array[i], array[j] = array[j], array[i]
        array[i + 1], array[high] = array[high], array[i + 1]
        return i + 1

    def refresh_tree(self):
        """Refresh the tree view with the current charity list."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for charity in self.charities:
            self.tree.insert("", "end", values=(charity.name, charity.priority))


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = QuickSortApp(root)
    root.mainloop()
