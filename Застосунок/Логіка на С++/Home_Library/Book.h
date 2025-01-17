#ifndef BOOK_H
#define BOOK_H

#include <string>
#include <vector>
#include <set>

class Book {
public:
    enum class ReadStatus { Unread, InProgress, Read }; // ������ �������
    enum class Format { Paper, Electronic };

private:
    std::string title;
    std::string author;
    int year;
    std::string genre;
    std::set<std::string> tags;
    ReadStatus readStatus; // ���� ��� ���������� �������
    Format format;

public:
    // �����������
    Book(const std::string& title, const std::string& author, int year, const std::string& genre, const std::vector<std::string>& tags, Format format);
       
    // �������
    std::string getTitle() const;
    std::string getAuthor() const;
    int getYear() const;
    std::string getGenre() const;
    std::set<std::string> getTags() const;
    ReadStatus getReadStatus() const; // ������ ��� �������
    Format getFormat() const;

    // �������
    void setReadStatus(ReadStatus status); // ������ ��� �������
    void setFormat(Format format);
    void addTag(const std::string& tag); // ���� ���
    void removeTag(const std::string& tag); // ������� ���
    bool hasTag(const std::string& tag) const; // ��������, �� � ���
    std::string toString() const; // ������� ��� ����� � ������ �����
};

#endif // BOOK_H
