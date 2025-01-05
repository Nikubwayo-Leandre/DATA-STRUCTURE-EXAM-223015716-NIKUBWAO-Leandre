from tkinter import *
from tkinter import ttk


# Circular Linked List Node
class OrderNode:
    def __init__(self, order_id, donor_name, amount):
        self.order_id = order_id
        self.donor_name = donor_name
        self.amount = amount
        self.next = None


# Circular Linked List for Order Management
class CircularOrderList:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.tail = None

    def add_order(self, order_id, donor_name, amount):
        new_node = OrderNode(order_id, donor_name, amount)
        if self.size < self.capacity:
            if not self.tail:
                new_node.next = new_node
                self.tail = new_node
            else:
                new_node.next = self.tail.next
                self.tail.next = new_node
                self.tail = new_node
            self.size += 1
        else:
            # Replace the oldest order (the node after the tail)
            new_node.next = self.tail.next.next
            self.tail.next = new_node
            self.tail = new_node

    def display_orders(self):
        orders = []
        if not self.tail:
            return orders
        current = self.tail.next
        for _ in range(self.size):
            orders.append((current.order_id, current.donor_name, current.amount))
            current = current.next
        return orders

    def search_order(self, order_id):
        if not self.tail:
            return None
        current = self.tail.next
        for _ in range(self.size):
            if current.order_id == order_id:
                return current
            current = current.next
        return None

    def delete_order(self, order_id):
        if not self.tail:
            return False
        current = self.tail.next
        prev = self.tail
        for _ in range(self.size):
            if current.order_id == order_id:
                if self.size == 1:  # Only one node
                    self.tail = None
                else:
                    prev.next = current.next
                    if current == self.tail:
                        self.tail = prev
                self.size -= 1
                return True
            prev = current
            current = current.next
        return False


# Tkinter GUI
class FundraisingOrderApp:
    def __init__(self, root, capacity):
        self.root = root
        self.root.title("Order Management - Online Fundraising Platform")
        self.root.geometry("800x600")

        self.order_list = CircularOrderList(capacity)
        self.setup_ui()

    def setup_ui(self):
        # Order Section
        order_frame = LabelFrame(self.root, text="Order Management", padx=10, pady=10)
        order_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        Label(order_frame, text="Order ID", bg="blue", ).grid(row=0, column=0, padx=10, pady=5)
        self.order_id_var = IntVar()
        Entry(order_frame, textvariable=self.order_id_var).grid(row=0, column=1, padx=10, pady=5)

        Label(order_frame, text="Donor Name", bg="blue", ).grid(row=1, column=0, padx=10, pady=5)
        self.donor_name_var = StringVar()
        Entry(order_frame, textvariable=self.donor_name_var).grid(row=1, column=1, padx=10, pady=5)

        Label(order_frame, text="Amount", bg="blue", ).grid(row=2, column=0, padx=10, pady=5)
        self.amount_var = DoubleVar()
        Entry(order_frame, textvariable=self.amount_var).grid(row=2, column=1, padx=10, pady=5)

        Button(order_frame, text="Add Order", bg="red", command=self.add_order).grid(row=3, column=0, padx=10, pady=10)
        Button(order_frame, text="Search Order", bg="pink", command=self.search_order).grid(row=3, column=1, padx=10, pady=10)
        Button(order_frame, text="Delete Order", bg="yellow", command=self.delete_order).grid(row=3, column=2, padx=10, pady=10)

        self.order_tree = ttk.Treeview(order_frame, columns=("ID", "Donor Name", "Amount"), show="headings", height=10)
        self.order_tree.grid(row=4, column=0, columnspan=3, pady=10)
        self.order_tree.heading("ID", text="Order ID")
        self.order_tree.heading("Donor Name", text="Donor Name")
        self.order_tree.heading("Amount", text="Amount")

    def refresh_order_table(self):
        # Clear table and refresh with current data
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        for order in self.order_list.display_orders():
            self.order_tree.insert("", "end", values=order)

    def add_order(self):
        order_id = self.order_id_var.get()
        donor_name = self.donor_name_var.get()
        amount = self.amount_var.get()

        self.order_list.add_order(order_id, donor_name, amount)
        self.refresh_order_table()

        self.order_id_var.set("")
        self.donor_name_var.set("")
        self.amount_var.set("")

    def search_order(self):
        order_id = self.order_id_var.get()
        order = self.order_list.search_order(order_id)

        if order:
            self.show_popup("Order Found", f"ID: {order.order_id}\nDonor: {order.donor_name}\nAmount: ${order.amount}")
        else:
            self.show_popup("Error", "Order not found.")

    def delete_order(self):
        order_id = self.order_id_var.get()
        if self.order_list.delete_order(order_id):
            self.refresh_order_table()
            self.show_popup("Success", f"Order ID {order_id} deleted successfully.")
        else:
            self.show_popup("Error", "Order not found.")

    def show_popup(self, title, message):
        popup = Toplevel(self.root)
        popup.title(title)
        Label(popup, text=message, font=("times new roman", 14)).pack(padx=20, pady=20)
        Button(popup, text="OK", command=popup.destroy).pack(pady=10)


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = FundraisingOrderApp(root, capacity=5)  # Set capacity of circular linked list
    root.mainloop()
