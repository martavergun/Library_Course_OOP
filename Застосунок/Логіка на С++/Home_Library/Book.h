#ifndef BOOK_H
#define BOOK_H

#include <string>
#include <vector>
#include <set>

class Book {
public:
    enum class ReadStatus { Unread, InProgress, Read }; // Перелік статусів
    enum class Format { Paper, Electronic };

private:
    std::string title;
    std::string author;
    int year;
    std::string genre;
    std::set<std::string> tags;
    ReadStatus readStatus; // Поле для збереження статусу
    Format format;

public:
    // Конструктор
    Book(const std::string& title, const std::string& author, int year, const std::string& genre, const std::vector<std::string>& tags, Format format);
       
    // Геттери
    std::string getTitle() const;
    std::string getAuthor() const;
    int getYear() const;
    std::string getGenre() const;
    std::set<std::string> getTags() const;
    ReadStatus getReadStatus() const; // Геттер для статусу
    Format getFormat() const;

    // Сеттери
    void setReadStatus(ReadStatus status); // Сеттер для статусу
    void setFormat(Format format);
    void addTag(const std::string& tag); // Додає тег
    void removeTag(const std::string& tag); // Видаляє тег
    bool hasTag(const std::string& tag) const; // Перевіряє, чи є тег
    std::string toString() const; // Повертає дані книги у вигляді рядка
};

#endif // BOOK_H
