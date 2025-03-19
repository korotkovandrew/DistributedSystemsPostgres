import tkinter as tk
from tkinter import ttk, messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"

def fetch_students_primary():
    try:
        response = requests.get(f"{BASE_URL}/students/primary")
        students = response.json()
        student_listbox.delete(0, tk.END)
        for student in students:
            student_listbox.insert(tk.END, f"{student['id']}: {student['имя']} {student['фамилия']} ({student['группа']})")
        source_label.config(text="Данные загружены из основной базы")
        root.title("Университет: Управление данными (Основная база)")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось получить список студентов из основной базы: {e}")

def fetch_students_replica():
    try:
        response = requests.get(f"{BASE_URL}/students/replica")
        students = response.json()
        student_listbox.delete(0, tk.END)
        for student in students:
            student_listbox.insert(tk.END, f"{student['id']}: {student['имя']} {student['фамилия']} ({student['группа']})")
        source_label.config(text="Данные загружены из реплики")
        root.title("Университет: Управление данными (Реплика)")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось получить список студентов из реплики: {e}")

def add_student():
    name = entry_name.get()
    surname = entry_surname.get()
    group = entry_group.get()
    if not name or not surname or not group:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return
    try:
        response = requests.post(f"{BASE_URL}/students", json={'имя': name, 'фамилия': surname, 'группа': group})
        if response.status_code == 201:
            messagebox.showinfo("Успех", "Студент добавлен в основную базу")
            fetch_students_primary()  # Обновляем список из основной базы после добавления
            # Очищаем поля ввода после успешного добавления
            entry_name.delete(0, tk.END)
            entry_surname.delete(0, tk.END)
            entry_group.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить студента")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при добавлении студента: {e}")

def delete_student():
    # Получаем индекс выбранной строки
    selected_index = student_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Предупреждение", "Выберите студента для удаления!")
        return

    # Получаем строку из списка
    selected_student = student_listbox.get(selected_index)
    # Извлекаем ID студента (первая часть строки до двоеточия)
    student_id = selected_student.split(":")[0]

    # Подтверждение удаления
    if not messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить студента с ID {student_id}?"):
        return

    try:
        # Отправляем запрос на удаление
        response = requests.delete(f"{BASE_URL}/students/{student_id}")
        if response.status_code == 200:
            messagebox.showinfo("Успех", f"Студент с ID {student_id} удален из основной базы")
            fetch_students_primary()  # Обновляем список после удаления
        else:
            messagebox.showerror("Ошибка", f"Не удалось удалить студента с ID {student_id}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении студента: {e}")

def show_context_menu(event):
    # Выделяем строку под курсором
    student_listbox.selection_clear(0, tk.END)
    student_listbox.selection_set(student_listbox.nearest(event.y))
    context_menu.post(event.x_root, event.y_root)

# Создаем главное окно
root = tk.Tk()
root.title("Университет: Управление данными")
root.geometry("700x500")  # Увеличиваем размер окна
root.configure(bg="#f0f0f0")

# Создаем фрейм для содержимого
tab_students = ttk.Frame(root)
tab_students.pack(fill="both", expand=True, padx=10, pady=10)

# Кнопки для загрузки данных
btn_fetch_primary = ttk.Button(tab_students, text="Загрузить из основной базы", command=fetch_students_primary)
btn_fetch_primary.pack(pady=5)

btn_fetch_replica = ttk.Button(tab_students, text="Загрузить из реплики", command=fetch_students_replica)
btn_fetch_replica.pack(pady=5)

# Метка для отображения источника данных
source_label = ttk.Label(tab_students, text="Данные не загружены", font=("Arial", 10, "italic"))
source_label.pack(pady=5)

# Список студентов
student_listbox = tk.Listbox(tab_students, height=15)  # Увеличиваем высоту списка
student_listbox.pack(fill="both", expand=True, padx=10, pady=5)

# Создаем контекстное меню
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Удалить", command=delete_student)

# Привязываем контекстное меню к списку (ПКМ)
student_listbox.bind("<Button-3>", show_context_menu)

# Фрейм для формы добавления студента
form_frame = ttk.LabelFrame(tab_students, text="Добавить нового студента", padding=10)
form_frame.pack(fill="x", padx=10, pady=10)

# Поле для имени
label_name = ttk.Label(form_frame, text="Имя:")
label_name.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_name = ttk.Entry(form_frame, width=30)  # Увеличиваем ширину поля
entry_name.grid(row=0, column=1, padx=5, pady=5)

# Поле для фамилии
label_surname = ttk.Label(form_frame, text="Фамилия:")
label_surname.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_surname = ttk.Entry(form_frame, width=30)
entry_surname.grid(row=1, column=1, padx=5, pady=5)

# Поле для группы
label_group = ttk.Label(form_frame, text="Группа:")
label_group.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_group = ttk.Entry(form_frame, width=30)
entry_group.grid(row=2, column=1, padx=5, pady=5)

# Кнопка добавления студента
btn_add_student = ttk.Button(form_frame, text="Добавить студента", command=add_student)
btn_add_student.grid(row=3, column=0, columnspan=2, pady=10)

# Запускаем приложение
root.mainloop()