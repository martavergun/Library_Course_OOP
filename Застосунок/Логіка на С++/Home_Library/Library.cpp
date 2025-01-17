#include "Library.h"
#include <sstream>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <iomanip>


Library library;

extern "C" {
    void addBook(const char* title, const char* author, int year, const char* genre, const char* tags, int status, int format) {
        std::vector<std::string> tagsVec;
        std::istringstream iss(tags);
        std::string tag;
        while (std::getline(iss, tag, ',')) {
            tagsVec.push_back(tag);
        }

        Book::ReadStatus readStatus = static_cast<Book::ReadStatus>(status);
        Book::Format bookFormat = static_cast<Book::Format>(format);

        // Додайте логування
        std::cout << "Title: " << title << ", Format: " << static_cast<int>(bookFormat) << std::endl;

        Book newBook(title, author, year, genre, tagsVec, bookFormat);
        newBook.setReadStatus(readStatus);

        library.addBook(newBook);
    }



    const char* viewBooks() {
        library.viewBooksString = library.viewBooks();
        return library.viewBooksString.c_str();
    }

    bool deleteBook(const char* title) {
        return library.deleteBook(title);
    }

    const char* searchBooks(const char* title) {
        static std::string result;
        result.clear();

        // Перетворення запиту до нижнього регістру
        std::string query = title ? title : "";
        std::transform(query.begin(), query.end(), query.begin(),
            [](unsigned char c) { return std::tolower(c); });

        for (const auto& book : library.getBooks()) {
            // Отримання даних книги
            std::string bookTitle = book.getTitle();
            std::string bookAuthor = book.getAuthor();
            std::string bookGenre = book.getGenre();

            // Перетворення до нижнього регістру
            std::transform(bookTitle.begin(), bookTitle.end(), bookTitle.begin(),
                [](unsigned char c) { return std::tolower(c); });
            std::transform(bookAuthor.begin(), bookAuthor.end(), bookAuthor.begin(),
                [](unsigned char c) { return std::tolower(c); });
            std::transform(bookGenre.begin(), bookGenre.end(), bookGenre.begin(),
                [](unsigned char c) { return std::tolower(c); });

            // Перевірка, чи містить запит назву, автора або жанр
            if (bookTitle.find(query) != std::string::npos ||
                bookAuthor.find(query) != std::string::npos ||
                bookGenre.find(query) != std::string::npos) {
                result += book.toString() + "\n";
            }
        }

        // Якщо результат порожній, повертаємо повідомлення
        if (result.empty()) {
            result = "No books found.\n";
        }

        return result.c_str();
    }







    const char* searchBooksByTag(const char* tag) {
        static std::string result;
        result.clear();  // Clear previous results

        for (const auto& book : library.getBooks()) {
            for (const auto& bookTag : book.getTags()) {
                if (bookTag.find(tag) != std::string::npos) {
                    result += book.toString() + "\n";
                    break;  // Avoid duplicate entries if multiple tags match
                }
            }
        }

        return result.c_str();
    }

   
    const char* getBooksByStatus(int status) {
        static std::string result;
        result.clear();

        for (const auto& book : library.getBooks()) {
            if (static_cast<int>(book.getReadStatus()) == status) {
                result += book.toString() + "\n";
            }
        }

        if (result.empty()) {
            result = "No books found for the given status.";
        }

        return result.c_str();
    }


    __declspec(dllexport) bool updateBookStatus(const char* title, int newStatus) {
        std::cout << "C++: Received title: " << title << ", newStatus: " << newStatus << std::endl;
        return library.updateBookStatus(title, static_cast<Book::ReadStatus>(newStatus));
    }

    const char* getBooksByFormat(int format) {
        static std::string result;
        result.clear();

        for (const auto& book : library.getBooks()) {
            if (static_cast<int>(book.getFormat()) == format) {
                result += book.toString() + "\n";
            }
        }

        if (result.empty()) {
            result = "No books found for the given format.\n";
        }

        return result.c_str();
    }


    void Library::sortBooksByFormat() {
        books.sort([](const Book& a, const Book& b) {
            return static_cast<int>(a.getFormat()) < static_cast<int>(b.getFormat());
            });
    }



    void saveToFile(const char* filename) {
        library.saveToFile(filename);
    }

    void loadFromFile(const char* filename) {
        library.loadFromFile(filename);
    }

    void sortBooksByAuthor() {
        library.sortBooksByAuthor();
    }
}

void Library::addBook(const Book& book) {
    books.push_back(book);
}

bool Library::deleteBook(const std::string& title) {
    for (auto it = books.begin(); it != books.end(); ++it) {
        if (it->getTitle() == title) {
            books.erase(it);
            return true;
        }
    }
    return false;
}

std::string Library::viewBooks() const {
    std::ostringstream oss;
    for (const auto& book : books) {
        oss << book.getTitle() << "|"
            << book.getAuthor() << "|"
            << book.getYear() << "|"
            << book.getGenre() << "|";

        std::string tags;
        for (const auto& tag : book.getTags()) {
            if (!tags.empty()) tags += ",";
            tags += tag;
        }

        oss << tags << "|"
            << static_cast<int>(book.getReadStatus()) << "|"
            << static_cast<int>(book.getFormat()) << "\n"; // Додаємо статус і формат
    }
    return oss.str();
}







const std::list<Book>& Library::getBooks() const {
    return books;
}

std::string Library::searchBooks(const std::string& title) const {
    std::ostringstream result;
    bool found = false;

    for (const auto& book : books) {
        if (book.getTitle().find(title) != std::string::npos) {
            found = true;
            result << book.toString() << "\n";
        }
    }

    return found ? result.str() : "No books found.";
}


void Library::sortBooksByAuthor() {
    std::vector<Book> bookVector(books.begin(), books.end());

    for (size_t i = 1; i < bookVector.size(); ++i) {
        Book key = bookVector[i];
        int j = static_cast<int>(i) - 1;

        while (j >= 0 && bookVector[j].getAuthor() > key.getAuthor()) {
            bookVector[j + 1] = bookVector[j];
            --j;
        }
        bookVector[j + 1] = key;
    }

    books.assign(bookVector.begin(), bookVector.end());
}

std::vector<Book> Library::searchBooksByTag(const std::string& tag) const {
    std::vector<Book> result;
    for (const auto& book : books) {
        if (book.hasTag(tag)) {
            result.push_back(book);
        }
    }
    return result;
}


std::vector<Book> Library::getBooksByStatus(Book::ReadStatus status) const {
    std::vector<Book> filteredBooks;
    for (const auto& book : books) {
        if (book.getReadStatus() == status) {
            filteredBooks.push_back(book);
        }
    }
    return filteredBooks;
}

std::vector<Book> Library::getBooksByFormat(Book::Format format) const {
    std::vector<Book> filteredBooks;
    for (const auto& book : books) {
        if (book.getFormat() == format) {
            filteredBooks.push_back(book);
        }
    }
    return filteredBooks;
}

bool Library::updateBookStatus(const std::string& title, Book::ReadStatus newStatus) {
    for (auto& book : books) {
        std::cout << "Checking book: " << book.getTitle() << " against " << title << std::endl;
        if (book.getTitle() == title) {
            book.setReadStatus(newStatus);
            std::cout << "Status updated for: " << title << std::endl;
            return true;
        }
    }
    std::cout << "Book not found: " << title << std::endl;
    return false;
}



void Library::saveToFile(const std::string& filename) const {
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Unable to open file for writing: " << filename << std::endl;
        return;
    }

    for (const auto& book : books) {
        file << book.getTitle() << "\n"
            << book.getAuthor() << "\n"
            << book.getYear() << "\n"
            << book.getGenre() << "\n";

        for (const auto& tag : book.getTags()) {
            file << tag << " ";
        }
        file << "\n";

        file << static_cast<int>(book.getReadStatus()) << "\n"
            << static_cast<int>(book.getFormat()) << "\n"; // Додаємо формат
    }

    file.close();
}


void Library::loadFromFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Unable to open file for reading: " << filename << std::endl;
        return;
    }

    books.clear();

    std::string title, author, genre, tagsLine;
    int year, readStatus, format;

    while (std::getline(file, title)) {
        std::getline(file, author);
        file >> year;
        file.ignore();
        std::getline(file, genre);
        std::getline(file, tagsLine);
        file >> readStatus;
        file >> format;
        file.ignore();

        std::vector<std::string> tags;
        std::istringstream tagsStream(tagsLine);
        std::string tag;
        while (tagsStream >> tag) {
            tags.push_back(tag);
        }

        Book book(title, author, year, genre, tags, static_cast<Book::Format>(format));
        book.setReadStatus(static_cast<Book::ReadStatus>(readStatus));
        books.push_back(book);
    }

    file.close();
}


