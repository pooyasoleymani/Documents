---
Created Date: 2026-09-15
tags:
  - cpp
---
---

## When should I use Vector at() instead of vector operator[]?

In C++, vector provides two methods for accessing its elements using indexes: ****vector operator[]**** and ****vector at()****. Although both methods provide similar functionality, but there are some differences between them.

****The following table lists the primary differences between the vector operator[] and vector at():****

|Parameter|vector operator[]|vector at()|
|---|---|---|
|Bound Checking|It does not perform bound checking.|This method performs the bound checking.|
|Exception|This method does not throw any exception, but shows an undefined behaviour on accessing the index which is out of bound.|This method throws an exception ****std::out_of_range**** on accessing the index which is out of bound.|
|Performance|It is faster as compared to vector at(), as it does not perform bound checking.|It is slower in comparison to vector operator[], as it performs the bound checking.|
|Use Case|Use vector operator[] when we are certain the index is within bounds and need maximum performance.|Use vector at() when we want to ensure safe access and handle out-of-bounds errors explicitly.|
|Syntax|v[i];|v.at(i);|

From the above table, we can infer that,

> One should use vector at() instead of the vector [] operator in situations where safety and bounds checking are important.


```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<int> v = {1, 3, 4, 7, 9};

    // Accessing the index which is in range
    cout << v[3] << endl;
    cout << v.at(3) << endl;

    // Accessing the index which is out of bound
    cout << v[7] << endl;
    try {
        cout << v.at(7) << endl;
    }
    catch (const out_of_range &e) {
        cout << "Exception: " << e.what() << endl;
    }
    return 0;
}
```
