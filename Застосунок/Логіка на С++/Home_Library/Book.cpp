#include "Book.h"
#include <sstream>
#include <iostream>


// Конструктор
Book::Book(const std::string& title, const std::string& author, int year, const std::string& genre, const std::vector<std::string>& tags, Format format)
    : title(title), author(author), year(year), genre(genre), tags(tags.begin(), tags.end()), readStatus(ReadStatus::Unread), format(format) {}
   
// Геттери
std::string Book::getTitle() const {
    return title;
}

std::string Book::getAuthor() const {
    return author;
}

int Book::getYear() const {
    return year;
}

std::string Book::getGenre() const {
    return genre;
}

std::set<std::string> Book::getTags() const {
    return tags;
}


Book::Format Book::getFormat() const {
    return format;
}

Book::ReadStatus Book::getReadStatus() const {
    return readStatus;
}

// Сеттери
void Book::setReadStatus(ReadStatus status) {
    readStatus = status;
}

void Book::setFormat(Format format) {
    this->format = format;
}
bool Book::hasTag(const std::string& tag) const {
    return tags.find(tag) != tags.end(); // Перевірка наявності тега
}

// Перетворення в рядок
std::string Book::toString() const {
    std::ostringstream oss;
    oss << title << "|" << author << "|" << year << "|" << genre << "|";

    for (const auto& tag : tags) {
        oss << tag << ",";
    }
    oss << "|" << static_cast<int>(readStatus) << "|" << static_cast<int>(format); // Додано формат
    return oss.str();

}




