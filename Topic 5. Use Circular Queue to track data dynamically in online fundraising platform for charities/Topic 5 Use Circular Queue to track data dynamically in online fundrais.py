from tkinter import *
from tkinter import ttk


# Circular Queue Class
class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = -1
        self.rear = -1
        self.size = 0

    def enqueue(self, order_id, donor_name, amount):
        if self.is_full():
            return False
        if self.front == -1:  # First element being added
            self.front = 0
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = (order_id, donor_name, amount)
        self.size += 1
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        removed_item = self.queue[self.front]
        if self.front == self.rear:  # Only one element
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return removed_item

    def is_full(self):
        return self.size == self.capacity

    def is_empty(self):
        return self.size == 0

    def display(self):
        items = []
        if self.is_empty():
            return items
        index = self.front
        for _ in range(self.size):
            items.append(self.queue[index])
            index = (index + 1) % self.capacity
        return items


# Tkinter GUI
class FundraisingQueueApp:
    def __init__(self, root, capacity):
        self.root = root
        self.root.title("Circular Queue - Online Fundraising Platform")
        self.root.geometry("800x600")

        self.queue = CircularQueue(capacity)
        self.setup_ui()

    def setup_ui(self):
        # Queue Management Section
        queue_frame = LabelFrame(self.root, text="Queue Management", padx=10, pady=10)
        queue_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        Label(queue_frame, text="Order ID").grid(row=0, column=0, padx=10, pady=5)
        self.order_id_var = IntVar()
        Entry(queue_frame, textvariable=self.order_id_var).grid(row=0, column=1, padx=10, pady=5)

        Label(queue_frame, text="Donor Name").grid(row=1, column=0, padx=10, pady=5)
        self.donor_name_var = StringVar()
        Entry(queue_frame, textvariable=self.donor_name_var).grid(row=1, column=1, padx=10, pady=5)

        Label(queue_frame, text="Amount").grid(row=2, column=0, padx=10, pady=5)
        self.amount_var = DoubleVar()
        Entry(queue_frame, textvariable=self.amount_var).grid(row=2, column=1, padx=10, pady=5)

        Button(queue_frame, text="Enqueue", command=self.enqueue).grid(row=3, column=0, padx=10, pady=10)
        Button(queue_frame, text="Dequeue", command=self.dequeue).grid(row=3, column=1, padx=10, pady=10)

        self.queue_tree = ttk.Treeview(queue_frame, columns=("ID", "Donor Name", "Amount"), show="headings", height=10)
        self.queue_tree.grid(row=4, column=0, columnspan=3, pady=10)
        self.queue_tree.heading("ID", text="Order ID")
        self.queue_tree.heading("Donor Name", text="Donor Name")
        self.queue_tree.heading("Amount", text="Amount")

        self.refresh_queue_table()

    def refresh_queue_table(self):
        # Clear table and refresh with current queue data
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)
        for order in self.queue.display():
            self.queue_tree.insert("", "end", values=order)

    def enqueue(self):
        order_id = self.order_id_var.get()
        donor_name = self.donor_name_var.get()
        amount = self.amount_var.get()

        if self.queue.enqueue(order_id, donor_name, amount):
            self.refresh_queue_table()
            self.show_popup("Success", "Order added to the queue.")
        else:
            self.show_popup("Error", "Queue is full.")

        self.order_id_var.set("")
        self.donor_name_var.set("")
        self.amount_var.set("")

    def dequeue(self):
        removed_item = self.queue.dequeue()
        if removed_item:
            self.refresh_queue_table()
            self.show_popup("Success", f"Dequeued Order:\nID: {removed_item[0]}\nDonor: {removed_item[1]}\nAmount: ${removed_item[2]}")
        else:
            self.show_popup("Error", "Queue is empty.")

    def show_popup(self, title, message):
        popup = Toplevel(self.root)
        popup.title(title)
        Label(popup, text=message, font=("times new roman", 14)).pack(padx=20, pady=20)
        Button(popup, text="OK", command=popup.destroy).pack(pady=10)


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = FundraisingQueueApp(root, capacity=5)  # Set the capacity of the circular queue
    root.mainloop()
