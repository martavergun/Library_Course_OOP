import tkinter as tk
from tkinter import ttk, messagebox
from library_interface import LibraryInterface


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Домашня бібліотека")
        self.root.state("zoomed")

        self.library = LibraryInterface()


        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(4, weight=1)

        # Завантаження книг із файлу при запуску
        try:
            self.library.load_books_from_file("books.txt")
        except Exception as e:
            messagebox.showerror("Помилка", f"Невдалось відкрити файл: {e}")

        # Поля вводу для книги

        self.root.columnconfigure(0, weight=1)  # Ліва частина
        self.root.columnconfigure(1, weight=3)  # Порожня частина для зміщення
        self.root.columnconfigure(2, weight=4)  # Центрована частина
        self.root.columnconfigure(3, weight=1)  # Права частина

        # Поля вводу для книги
        input_frame = tk.Frame(root)
        input_frame.grid(row=0, column=2, columnspan=1, pady=10, sticky="ew")  # Розміщення у центрі

        self.title_label = tk.Label(input_frame, text="Назва:", font=("Arial", 12))
        self.title_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.author_label = tk.Label(input_frame, text="Автор:", font=("Arial", 12))
        self.author_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.year_label = tk.Label(input_frame, text="Рік видання:", font=("Arial", 12))
        self.year_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.genre_label = tk.Label(input_frame, text="Жанр:", font=("Arial", 12))
        self.genre_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.tags_label = tk.Label(input_frame, text="Теги (через кому):", font=("Arial", 12))
        self.tags_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.status_label = tk.Label(input_frame, text="Статус:", font=("Arial", 12))
        self.status_combobox = ttk.Combobox(
            input_frame,
            values=["Непрочитана", "В процесі", "Прочитана"],
            state="readonly",
            font=("Arial", 12)
        )
        self.status_combobox.set("Непрочитана")

        self.format_label = tk.Label(input_frame, text="Формат:", font=("Arial", 12))
        self.format_combobox = ttk.Combobox(
            input_frame,
            values=["Паперова", "Електронна"],
            state="readonly",
            font=("Arial", 12)
        )
        self.format_combobox.set("Паперова")  # Значення за замовчуванням

        self.title_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.title_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.author_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.author_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.year_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.year_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.genre_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.genre_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.tags_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.tags_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self.status_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.status_combobox.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        self.format_label.grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.format_combobox.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        # Фільтрування за статусом та форматом
        filter_frame = tk.LabelFrame(root, text="Фільтрувати", font=("Arial", 12), padx=10, pady=10)
        filter_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")

        # Формат
        self.filter_format_label = tk.Label(filter_frame, text="Формат:", font=("Arial", 12))
        self.filter_format_combobox = ttk.Combobox(
            filter_frame,
            values=["Паперова", "Електронна"],
            state="readonly",
            font=("Arial", 12)
        )
        self.filter_format_combobox.set("Паперова")

        self.filter_by_format_button = tk.Button(
            filter_frame,
            text="Застосувати",
            command=self.filter_books_by_format,
            font=("Arial", 12),
            bg="#FFFFE0"
        )

        # Статус
        self.filter_status_label = tk.Label(filter_frame, text="За статусом:", font=("Arial", 12))
        self.filter_status_combobox = ttk.Combobox(
            filter_frame,
            values=["Непрочитана", "В процесі", "Прочитана"],
            state="readonly",
            font=("Arial", 12)
        )
        self.filter_status_combobox.set("Непрочитана")

        self.filter_button = tk.Button(
            filter_frame,
            text="Застосувати",
            command=self.filter_books_by_status,
            font=("Arial", 12),
            bg="#FFFFE0"
        )

        # Розташування у фреймі в один рядок
        self.filter_format_label.pack(side="left", padx=5, pady=5)
        self.filter_format_combobox.pack(side="left", padx=5, pady=5)
        self.filter_by_format_button.pack(side="left", padx=5, pady=5)

        self.filter_status_label.pack(side="left", padx=5, pady=5)
        self.filter_status_combobox.pack(side="left", padx=5, pady=5)
        self.filter_button.pack(side="left", padx=5, pady=5)

        # Кнопки дій
        button_frame = tk.LabelFrame(root, text="Дії", font=("Arial", 12), padx=10, pady=10)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

        self.add_button = tk.Button(button_frame, text="Додати книгу", command=self.add_book, font=("Arial", 12), width=15, bg="#FFFFE0")
        self.delete_button = tk.Button(button_frame, text="Видалити книгу", command=self.delete_book, font=("Arial", 12),
                                       width=15,bg="#FFFFE0")
        self.refresh_button = tk.Button(button_frame, text="Оновити", command=self.load_books_to_table,
                                        font=("Arial", 12), width=15, bg="#FFFFE0")
        self.sort_button = tk.Button(button_frame, text="Сортувати за автором", command=self.sort_books_by_author,
                                     font=("Arial", 12), width=20, bg="#FFFFE0")

        self.add_button.pack(side="left", padx=5)
        self.delete_button.pack(side="left", padx=5)
        self.refresh_button.pack(side="right", padx=5)
        self.sort_button.pack(side="left", padx=5)

        self.edit_status_button = tk.Button(
            button_frame,
            text="Змінити статус",
            command=self.edit_book_status,
            font=("Arial", 12),
            width=15,
            bg="#FFFFE0"
        )
        self.edit_status_button.pack(side="left", padx=5)

        # Пошук
        search_frame = tk.LabelFrame(root, text="Пошук", font=("Arial", 12), padx=10, pady=10)
        search_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")

        self.search_label = tk.Label(search_frame, text="Ключове слово:", font=("Arial", 12))
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=50)
        self.search_button = tk.Button(search_frame, text="Шукати книгу", command=self.search_book, font=("Arial", 12),
                                       width=15, bg="#FFFFE0")
        self.search_by_tag_button = tk.Button(search_frame, text="Шукати за тегом", command=self.search_books_by_tag,
                                              font=("Arial", 12), width=15, bg="#FFFFE0")

        self.search_label.pack(side="left", padx=5)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_button.pack(side="left", padx=5)
        self.search_by_tag_button.pack(side="left", padx=5)

        # Таблиця для відображення книг
        self.table = ttk.Treeview(
            root,
            columns=("title", "author", "year", "genre", "tags", "status", "format"),
            show="headings",
        )

        # Заголовки колонок
        self.table.heading("title", text="Назва")
        self.table.heading("author", text="Автор")
        self.table.heading("year", text="Рік видання")
        self.table.heading("genre", text="Жанр")
        self.table.heading("tags", text="Теги")
        self.table.heading("status", text="Статус")
        self.table.heading("format", text="Формат")
        self.table.column("title", width=400)
        self.table.column("author", width=300)
        self.table.column("year", width=100, anchor="center")
        self.table.column("genre", width=300)
        self.table.column("tags", width=200, anchor="center")
        self.table.column("status", width=150, anchor="center")
        self.table.column("format", width=150, anchor="center")


        self.table.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Скролбар для таблиці
        scrollbar = tk.Scrollbar(root, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=4, column=4, sticky="ns")

        # Завантаження книг у таблицю при запуску
        self.load_books_to_table()

    def add_book(self):

        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year = int(self.year_entry.get()) if self.year_entry.get().isdigit() else 0
        genre = self.genre_entry.get().strip()
        tags = self.tags_entry.get().strip().split(",")
        status = self.status_combobox.get()
        book_format = self.format_combobox.get()

        # Мапінг статусу та формату
        status_map = {"Непрочитана": 0, "В процесі": 1, "Прочитана": 2}
        format_map = {"Паперова": "Паперова", "Електронна": "Електронна"}


        if not title or not author or not genre or year <= 0:
            messagebox.showwarning("Помилка вводу", "Усі поля обов'язкові!")
            return

        if status not in status_map or book_format not in format_map:
            messagebox.showwarning("Помилка вводу", "Оберіть дійсний статус і формат!")
            return


        try:
            self.library.add_book(title, author, year, genre, tags, status_map[status], format_map[book_format])
            messagebox.showinfo("Успішно", "Книгу успішно додано!")
            self.load_books_to_table()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося додати книгу: {e}")

    def delete_book(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Помилка", "Будь ласка, оберіть книгу для видалення!")
            return

        book_title = self.table.item(selected_item, "values")[0]
        success = self.library.delete_book(book_title)
        if success:
            messagebox.showinfo("Успішно", "Книга успішно видалена!")
            self.table.delete(selected_item)
            self.library.save_books_to_file("books.txt")
        else:
            messagebox.showerror("Помилка", "Книга не знайдена!")

    def search_book(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Помилка", "Будь ласка, введіть пошуковий запит!")
            return

        books = self.library.search_books(query)


        self.table.delete(*self.table.get_children())

        for book in books:
            if book.strip():
                parts = book.split("|")


                if len(parts) < 7:
                    print(f"Skipping malformed book entry: {book}")
                    continue

                title = parts[0]
                author = parts[1]
                year = parts[2]
                genre = parts[3]
                tags = parts[4]
                status_index = int(parts[5])
                format_index = int(parts[6])

                # Мапінг статусу та формату
                status_map = {0: "Непрочитана", 1: "В процесі", 2: "Прочитана"}
                format_map = {0: "Паперова", 1: "Електронна"}
                status = status_map.get(status_index, "Невідомий")
                book_format = format_map.get(format_index, "Невідомий")

                self.table.insert("", tk.END, values=(title, author, year, genre, tags, status, book_format))

        if not self.table.get_children():
            messagebox.showinfo("Пошук", "Немає книг за даним запитом.")

    def load_books_to_table(self):

        for row in self.table.get_children():
            self.table.delete(row)

        books = self.library.view_books()
        if books:
            for book in books:
                if book.strip():
                    parts = book.split("|")
                    title = parts[0] if len(parts) > 0 else ""
                    author = parts[1] if len(parts) > 1 else ""
                    year = parts[2] if len(parts) > 2 else ""
                    genre = parts[3] if len(parts) > 3 else ""
                    tags = parts[4] if len(parts) > 4 else ""
                    status_index = int(parts[5]) if len(parts) > 5 else -1
                    format_index = int(parts[6]) if len(parts) > 6 else -1

                    # Перетворення статусу та формату
                    status_map = {0: "Непрочитана", 1: "В процесі", 2: "Прочитана"}
                    format_map = {0: "Паперова", 1: "Електронна"}

                    status = status_map.get(status_index, "Невідомий")
                    book_format = format_map.get(format_index, "Невідомий")

                    # Додавання рядка в таблицю
                    self.table.insert("", tk.END, values=(title, author, year, genre, tags, status, book_format))

    def sort_books_by_author(self):
        books = self.library.view_books()
        if not books:
            messagebox.showinfo("Інформація", "Немає книг для сортування.")
            return

        sorted_books = sorted(books, key=lambda book: book.split("|")[1])  # Сортування за автором

        self.table.delete(*self.table.get_children())
        for book in sorted_books:
            if book.strip():
                parts = book.split("|")
                title = parts[0] if len(parts) > 0 else ""
                author = parts[1] if len(parts) > 1 else ""
                year = parts[2] if len(parts) > 2 else ""
                genre = parts[3] if len(parts) > 3 else ""
                tags = parts[4] if len(parts) > 4 else ""
                status_index = int(parts[5]) if len(parts) > 5 else -1
                format_index = int(parts[6]) if len(parts) > 6 else -1

                status_map = {0: "Непрочитана", 1: "В процесі", 2: "Прочитана"}
                format_map = {0: "Паперова", 1: "Електронна"}

                status = status_map.get(status_index, "Невідомий")
                book_format = format_map.get(format_index, "Невідомий")

                # Додавання формату до таблиці
                self.table.insert("", tk.END, values=(title, author, year, genre, tags, status, book_format))

    def search_books_by_tag(self):
        tag_query = self.search_entry.get().strip().lower()
        if not tag_query:
            messagebox.showwarning("Помилка", "Будь ласка, введіть тег для пошуку!")
            return

        books = self.library.search_books_by_tag(tag_query)
        self.table.delete(*self.table.get_children())

        for book in books:
            if book.strip():
                parts = book.split("|")
                title = parts[0] if len(parts) > 0 else ""
                author = parts[1] if len(parts) > 1 else ""
                year = parts[2] if len(parts) > 2 else ""
                genre = parts[3] if len(parts) > 3 else ""
                tags = parts[4] if len(parts) > 4 else ""
                status_index = int(parts[5]) if len(parts) > 5 else -1
                format_index = int(parts[6]) if len(parts) > 6 else -1
                status_map = {0: "Непрочитана", 1: "В процесі", 2: "Прочитана"}
                format_map = {0: "Паперова", 1: "Електронна"}

                status = status_map.get(status_index, "Невідомий")
                book_format = format_map.get(format_index, "Невідомий")

                self.table.insert("", tk.END, values=(title, author, year, genre, tags, status, book_format))

        if not self.table.get_children():
            messagebox.showinfo("Пошук", "Немає книг за заданим тегом.")

    def filter_books_by_status(self):
        # Мапінг статусів
        status_map = {"Непрочитана": 0, "В процесі": 1, "Прочитана": 2}
        selected_status = self.filter_status_combobox.get()

        # Перевірка обраного статусу
        if selected_status not in status_map:
            messagebox.showwarning("Помилка вводу", "Будь ласка, оберіть дійсний статус!")
            return


        books = self.library.get_books_by_status(status_map[selected_status])


        self.table.delete(*self.table.get_children())

        if not books or (len(books) == 1 and books[0].startswith("No books found")):
            messagebox.showinfo("Інформація", "Книги з обраним статусом не знайдено.")
            return

        for book in books:
            if book.strip():
                parts = book.split("|")
                title = parts[0] if len(parts) > 0 else ""
                author = parts[1] if len(parts) > 1 else ""
                year = parts[2] if len(parts) > 2 else ""
                genre = parts[3] if len(parts) > 3 else ""
                tags = parts[4] if len(parts) > 4 else ""
                status_index = int(parts[5]) if len(parts) > 5 else -1
                format_index = int(parts[6]) if len(parts) > 6 else -1

                # Зворотній мапінг статусу і формату
                status_map_reverse = {0: "Непрочитана", 1: "В процесі", 2: "Прочитана"}
                format_map_reverse = {0: "Паперова", 1: "Електронна"}

                status = status_map_reverse.get(status_index, "Невідомий")
                book_format = format_map_reverse.get(format_index, "Невідомий")

                self.table.insert("", tk.END, values=(title, author, year, genre, tags, status, book_format))

    def filter_books_by_format(self):

        book_format = self.filter_format_combobox.get()
        if not book_format:
            messagebox.showwarning("Помилка вводу", "Будь ласка, оберіть формат для фільтрації!")
            return

        # Мапінг форматів для відповідності C++ бібліотеці
        format_map = {"Паперова": "Paper", "Електронна": "Electronic"}
        if book_format not in format_map:
            messagebox.showerror("Помилка", f"Невірний формат: {book_format}")
            return


        try:
            books = self.library.get_books_by_format(format_map[book_format])
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))
            return


        self.table.delete(*self.table.get_children())


        for book in books:
            if book.strip():
                parts = book.split("|")
                title = parts[0]
                author = parts[1]
                year = parts[2]
                genre = parts[3]
                tags = parts[4]
                status_index = int(parts[5])
                format_index = int(parts[6])

                # Мапінг статусів і форматів для відображення
                status_map = {0: "Непрочитана", 1: "В процесі", 2: "Прочитана"}
                format_map_reverse = {0: "Паперова", 1: "Електронна"}

                status = status_map.get(status_index, "Невідомий")
                book_format_display = format_map_reverse.get(format_index, "Невідомий")

                self.table.insert("", tk.END, values=(title, author, year, genre, tags, status, book_format_display))

    def edit_book_status(self):

        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Помилка вводу", "Будь ласка, оберіть книгу для редагування!")
            return


        book_data = self.table.item(selected_item, "values")
        title = book_data[0]
        current_status = book_data[5]

        # Відкриваємо нове вікно для редагування статусу
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Редагування статусу - {title}")
        edit_window.geometry("300x150")
        tk.Label(edit_window, text="Оберіть новий статус:", font=("Arial", 12)).pack(pady=10)

        # Випадаючий список для статусу
        status_combobox = ttk.Combobox(
            edit_window,
            values=["Непрочитана", "В процесі", "Прочитана"],
            state="readonly",
            font=("Arial", 12)
        )
        status_combobox.set(current_status)
        status_combobox.pack(pady=10)

        # Логіка для збереження змін
        def save_status():
            new_status = status_combobox.get()
            if not new_status:
                messagebox.showwarning("Помилка вводу", "Будь ласка, оберіть дійсний статус!")
                return

            # Мапінг статусу
            status_map = {"Непрочитана": 0, "В процесі": 1, "Прочитана": 2}
            if new_status not in status_map:
                messagebox.showwarning("Помилка вводу", "Обрано недійсний статус!")
                return

            # Оновлюємо статус у бібліотеці
            success = self.library.update_book_status(title, status_map[
                new_status])
            if success:
                messagebox.showinfo("Успішно", "Статус книги успішно оновлено!")
                self.load_books_to_table()  # Оновлюємо таблицю
                edit_window.destroy()
            else:
                messagebox.showerror("Помилка", "Не вдалося оновити статус книги!")


        save_button = tk.Button(edit_window, text="Зберегти", command=save_status, font=("Arial", 12))
        save_button.pack(pady=10)

        # Зберегти зміни
        def save_status():
            new_status = status_combobox.get()
            if not new_status:
                messagebox.showwarning("Помилка", "Будь ласка, оберіть дійсний статус!")
                return


            status_map = {"Непрочитана": 0, "В процесі": 1, "Прочитана": 2}
            if new_status not in status_map:
                messagebox.showwarning("Помилка вводу", "Обрано недійсний статус!")
                return

            # Оновлюємо статус у бібліотеці
            success = self.library.update_book_status(title, status_map[
                new_status])
            if success:
                messagebox.showinfo("Успішно", "Статус книги успішно оновлено!")
                self.load_books_to_table()  # Оновлюємо таблицю
                edit_window.destroy()
            else:
                messagebox.showerror("Помилка", "Не вдалося оновити статус книги!")

            tk.Button(edit_window, text="Зберегти", command=save_status, font=("Arial", 12)).pack(pady=10)

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.tags_entry.delete(0, tk.END)

    def save_books(self):

        try:
            self.library.save_books_to_file("books.txt")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалось зберегти книги: {e}")

    def on_closing(self):

        self.save_books()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()