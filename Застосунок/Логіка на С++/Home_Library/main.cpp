#include "Library.h"
#include <iostream>

int main() {
    // ��������� ���� � ��������
    addBook("Book A", "Author X", 2020, "Fiction", "tag1,tag2", 0, 1); // Status: Unread
    addBook("Book B", "Author Y", 2018, "Non-Fiction", "tag3,tag4", 1, 1); // Status: In Progress
    addBook("Book C", "Author Z", 2022, "Mystery", "tag5", 2, 1); // Status: Read

    // �������� ��� ����
    std::cout << "All books:\n" << viewBooks() << "\n";

    // ��������� �����
    if (deleteBook("Book A")) {
        std::cout << "Book A deleted successfully.\n";
    }
    else {
        std::cout << "Book A not found.\n";
    }

    // ��������� ������ ����
    std::cout << "Updated book list:\n" << viewBooks() << "\n";

    return 0;
}
