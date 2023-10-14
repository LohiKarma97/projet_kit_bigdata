import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
from todolist.todolist import ToDoList
from todolist.Tache import Tache, TacheStatus

class TaskInputDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, default_values=None):
        self.default_values = default_values or {}
        super().__init__(parent)
    
    def body(self, master):
        # Attributes' labels and entries
        self.labels = ["Status", "Projet", "Horodatage", "Nom", "Description"]
        self.entries = {}

        for label in self.labels:
            tk.Label(master, text=label).pack(pady=5)
            self.entries[label] = tk.Entry(master)
            self.entries[label].pack(pady=5)
            # Check if the default value for this label exists
            if label in self.default_values:
                # Clear the existing content and insert the default value
                self.entries[label].delete(0, tk.END)
                self.entries[label].insert(0, self.default_values[label])
            elif label == "Status":
                self.entries[label].insert(0, "A_FAIRE")

        return self.entries["Nom"]  # initial focus

    def validate(self):
        name = self.entries["Nom"].get()
        description = self.entries["Description"].get()

        if not name or not description:
            messagebox.showerror("Error", "Name and Description cannot be empty!")
            return 0

        return 1

    def apply(self):
        self.result = {label: self.entries[label].get() for label in self.labels}


class ToDoListApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Beautiful To-Do List App")
        self.root.geometry('600x400')

        self.todolist = ToDoList()

        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=25)

        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("Status", "Projet", "Horodatage", "Nom", "Description")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Status", anchor=tk.W, width=80)
        self.tree.column("Projet", anchor=tk.W, width=100)
        self.tree.column("Horodatage", anchor=tk.W, width=100)
        self.tree.column("Nom", anchor=tk.W, width=100)
        self.tree.column("Description", anchor=tk.W, width=150)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Status", text="Status", anchor=tk.W)
        self.tree.heading("Projet", text="Projet", anchor=tk.W)
        self.tree.heading("Horodatage", text="Horodatage", anchor=tk.W)
        self.tree.heading("Nom", text="Nom", anchor=tk.W)
        self.tree.heading("Description", text="Description", anchor=tk.W)

        self.tree.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        # Create a frame for buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10, padx=10)

        # Add Task button
        add_button = ttk.Button(button_frame, text="Add Task", command=self.add_task)
        add_button.pack(side=tk.LEFT, padx=5)  # side=tk.LEFT ensures that buttons are packed side-by-side

        # Modify Task button
        modify_button = ttk.Button(button_frame, text="Modify Task", command=self.modify_task)
        modify_button.pack(side=tk.LEFT, padx=5)

        # Delete Task button
        delete_button = ttk.Button(button_frame, text="Delete Task", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, padx=5)


    def add_task(self):
        dialog = TaskInputDialog(self.root)
        data = dialog.result

        if data:  # This will be None if the user cancels the dialog
            try:
                status = TacheStatus[data["Status"]]
                projet = data["Projet"]
                horodatage = int(data["Horodatage"])
                name = data["Nom"]
                description = data["Description"]

                task = Tache(status, projet, horodatage, name, description)
                self.todolist.ajouter(task)

                # Inserting into Treeview
                self.tree.insert("", tk.END, values=(data["Status"], projet, horodatage, name, description))
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def modify_task(self):
        selected_item = self.tree.selection()

        if selected_item:  # Check if there's a selected task
            values = self.tree.item(selected_item)['values']

            # Map the values to their respective labels
            default_values = dict(zip(["Status", "Projet", "Horodatage","Nom", "Description"], values))

            # Open the dialog with the default values
            dialog = TaskInputDialog(self.root, default_values)
            data = dialog.result

            if data:  # If user didn't cancel the dialog
                try:
                    status = TacheStatus[data["Status"]]
                    projet = data["Projet"]
                    horodatage = int(data["Horodatage"])
                    name = data["Nom"]
                    description = data["Description"]

                    # Update the Tache object
                    #task = self.todolist.liste_taches[int(selected_item[0])]
                    index = self.tree.index(selected_item)
                    task = self.todolist.liste_taches[index]
                    task.status = status
                    task.projet = projet
                    task.horodatage = horodatage
                    task.Nom = name
                    task.Description = description

                    # Update the Treeview
                    self.tree.item(selected_item, values=(data["Status"], projet, horodatage,name, description))

                except Exception as e:
                    messagebox.showerror("Error", str(e))


    def delete_task(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showinfo("Information", "Please select a task to delete.")
            return

        # Confirm deletion
        answer = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected task?")
        if answer:
            # Remove from internal todolist
            index = self.tree.index(selected_item)
            del self.todolist.liste_taches[index]
            # Remove from Treeview
            self.tree.delete(selected_item)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
