#ifndef LIBRARY_H
#define LIBRARY_H

#include "Book.h"
#include <list>
#include <string>
#include <vector>
#include <iostream>

// Оголошення глобального об'єкта Library
class Library;
extern Library library;

extern "C" {
    __declspec(dllexport) void addBook(const char* title, const char* author, int year, const char* genre, const char* tags, int status, int format);
    __declspec(dllexport) const char* viewBooks();
    __declspec(dllexport) bool deleteBook(const char* title);
    __declspec(dllexport) const char* searchBooks(const char* title);
    __declspec(dllexport) const char* searchBooksByTag(const char* tag);
    __declspec(dllexport) void saveToFile(const char* filename);
    __declspec(dllexport) void loadFromFile(const char* filename);
    __declspec(dllexport) void sortBooksByAuthor();
    __declspec(dllexport) const char* getBooksByStatus(int status);
    __declspec(dllexport) bool updateBookStatus(const char* title, int newStatus);
    __declspec(dllexport) const char* getBooksByFormat(int format);
}

class Library {

private:
    std::list<Book> books;

public:
    void addBook(const Book& book);
    bool deleteBook(const std::string& title);
    std::string viewBooks() const;
    const std::list<Book>& getBooks() const;
    void saveToFile(const std::string& filename) const;
    void loadFromFile(const std::string& filename);
    std::string searchBooks(const std::string& title) const;
    std::string viewBooksString;
    void sortBooksByAuthor();
    std::vector<Book> searchBooksByTag(const std::string& tag) const;
    std::vector<Book> getBooksByStatus(Book::ReadStatus status) const;
    bool updateBookStatus(const std::string& title, Book::ReadStatus newStatus);
    void sortBooksByFormat();
    std::vector<Book> getBooksByFormat(Book::Format format) const;



};

#endif // LIBRARY_H
