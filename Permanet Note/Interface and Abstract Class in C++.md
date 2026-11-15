---
Created Date: 2026-09-10
tags:
  - cpp
---
---

## Problem

C++ haven't built-in functionality of *interface* it can be implemented using *abstract classes* and **pure virtual function**.

## Implementing Interfaces Using Abstract Classes in C++

> In programming, an [interface](https://www.geeksforgeeks.org/cpp/cpp-program-to-create-an-interface/) serves as a blueprint that specifies what methods a class will have without providing any implementation details about the methods.

Any class containing a [pure virtual function](https://www.geeksforgeeks.org/cpp/pure-virtual-functions-and-abstract-classes/) is considered an abstract class.

- Declare a class with at least one pure virtual function that will act as an interface for the other derived classes.
- Define the abstract class (interface):
    - Create classes that inherits from the abstract base class.
- Provide separate implementations in derived classes for each pure virtual function present in the abstract base class.
- If implementation for the pure virtual function is not provided in the derived class then it will also act as a base class.

```cpp
// C++ Program to Implement Interfaces Using Abstract Class

#include <iostream>
#include <string>
using namespace std;

// Declare the Student interface as an abstract class
class Student {
public:
    // Pure virtual function to get student information
    virtual string getStudentInfo() = 0;
    // Pure virtual function to print student information
    virtual void printStudentInfo() = 0;
};

// Define the UndergraduateStudent class that inherits from
// Student
class UndergraduateStudent : public Student {
private:
    string name;
    int year;
    string major;

public:
    // Constructor to initialize member variables
    UndergraduateStudent(string n, int y, string m)
        : name(n)
        , year(y)
        , major(m)
    {
    }

    // Override the getStudentInfo function to return
    // formatted student info
    string getStudentInfo() override
    {
        return name + ", Year: " + to_string(year)
               + ", Major: " + major;
    }

    // Override the printStudentInfo function to print
    // student info to console
    void printStudentInfo() override
    {
        cout << "Undergraduate Student: "
             << getStudentInfo() << endl;
    }
};

// Define the GraduateStudent class that inherits from
// Student
class GraduateStudent : public Student {
private:
    string name;
    string program;
    string thesis;

public:
    // Constructor to initialize member variables
    GraduateStudent(string n, string p, string t)
        : name(n)
        , program(p)
        , thesis(t)
    {
    }

    // Override the getStudentInfo function to return
    // formatted student info
    string getStudentInfo() override
    {
        return name + ", Program: " + program
               + ", Thesis: " + thesis;
    }

    // Override the printStudentInfo function to print
    // student info to console
    void printStudentInfo() override
    {
        cout << "Graduate Student: " << getStudentInfo()
             << endl;
    }
};

// Driver Code
int main()
{
    // Create an instance of UndergraduateStudent and print
    // its info
    UndergraduateStudent undergrad("Mohit Kumar", 3,
                                   "Computer Science");
    undergrad.printStudentInfo();

    // Create an instance of GraduateStudent and print its
    // info
    GraduateStudent grad("Rohit Kumar", "Master of Science",
                         "AI");
    grad.printStudentInfo();

    return 0;
}
```