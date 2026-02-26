---
Created Date: 2026-02-25
tags:
  - Data_Analysis
---
---
**Numpy** is library for work with *numerical* data. 

### Create Array

```python
import numpy as np
np.__version__ # '2.1.2'

np.array([1, 2, 3]) #آرایه‌ی یک بعدی شامل ۳ عدد
np.array(
	[[1, 2], # آرایه‌ی دو بعدی ۲*۳ شامل ۶ عدد
	[3, 4],
	[5, 6]]
 )
 
 np.zeros(3) # آرایه‌ی یک بعدی شامل ۳ عدد حقیقی برابر صفر
 np.ones((2, 3))# آرایه‌‌ی دو بعدی ۳*۲ شامل ۶ عدد حقیقی برابر یک
 np.arange(0, 15, 4)# آرایه‌ی یک بعدی شامل اعداد صحیح پیش از ۱۵ با شروع از ۰ و با فاصله ۴
 
 np.linspace(0, 20, 5)# آرایه‌ی یک بعدی شامل ۵ عدد حقیقی در بازه ۰ تا ۲۰ (شامل این دو) با فاصله برابر
 np.eye(3)# آرایه‌ی دو بعدی ۳*۳ متناظر با ماتریس همانی (قطر ۱ و باقی خانه‌ها ۰)
 
 np.empty(3)# آرایه‌ی یک بعدی شامل ۳ عدد نامشخص (بسته به مقدار داخل حافظه)
 
 np.random.random(3)# آرایه‌ی یک بعدی شامل ۳ عدد تصادفی از توزیع یکنواخت بین ۰ و ۱
 np.random.randint(0, 10, (3, 3)) # آرایه‌ی دو بعدی ۳*۳ شامل اعداد صحیح تصادفی بین ۰ تا ۹
 np.random.normal(0, 1, (2, 3))# آرایه‌ی دو بعدی ۳*۲ شامل اعداد تصادفی از توزیع نرمال با میانگین ۰ و واریانس ۱
 a = np.random.randint(0, 10, (2, 3)) # آرایه‌ی دو بعدی ۳*۲ شامل اعداد صحیح تصادفی بین ۰ تا ۱۰ 
# آرایه‌ی پر از ۳ با ابعاد مشابه آرایه ورودی (۳*۲)
np.full_like(a, 3)

```


### Data Type
**astype()** method can cast data type of after creation.

```python
np.array([False, True], dtype='bool_') # نوع مقدار بولی
# کاراکتر _ برای اشاره به نوع داخل نامپای است اما می‌توان آن را برداشت

np.array([1, 2, 3.14], dtype='int_') # نوع عدد صحیح (عدد سوم تبدیل به 3 می‌شود)

np.array([2.71828182845, 3.14159265359], dtype='float64') # نوع عدد حقیقی ۶۴ بیتی

np.array([255], dtype='uint8') # نوع عدد صحیح نامنفی ۸ بیتی

np.array(['Hello', 'World'], dtype='str_') # نوع رشته
```


### Attributes

```python
a = np.array([[1, 2],
             [3, 4],
             [5, 6]], dtype='float64')
print(a)
print('number of dimensions:', a.ndim) # تعداد ابعاد آرایه
print('shape:', a.shape) # اندازه ابعاد آرایه
print('size:', a.size) # تعداد خانه‌های آرایه
print('dtype:', a.dtype) # نوع داده آرایه
```



### Indexing
- Access to elements with [] operator.
```python
a = np.array([0, 1, 2, 3])
print(a)
print('a[0] =', a[0])
print('a[2] =', a[2])
print('a[-1] =', a[-1])
```


- For access to another dimensions can use `,` operator.
```python
a = np.random.randint(0, 10, (3, 5))
print('a[2, 3] =', a[2, 3])
```

- *numpy* can implicit cast values
```python
a = np.array([1, 2, 3, 4], dtype='int_')
a[1] = 3.144
print('a[1] = ', a[1]) # a[1] = 3
```


### Slicing
```python
a = np.array([[0, 1, 2],
              [3, 4, 5],
              [6, 7, 8],
              [9, 10, 11]])
print('a[:2, 1:]= ',a[:2, 1:])
print('a[1:3, ::2]= ',a[1:3, ::2])
```


- For copy a Array we can use **copy()** method .
```python 
a = np.array([[0, 1, 2],
              [3, 4, 5],
              [6, 7, 8]])
sub_copy_a = a[2:4, 1:].copy()
sub_copy_a[0, 0] = 10
```

>[!NOTE]
> If use `=` for copy array when change elements in every array both of array changed.


### Reshaping

```python
a = np.array([1, 2, 3])
print(a.reshape(3, 1))
print(a.reshape(1, 3))

a = np.arange(12)
print(a.reshape(2, -1, 3))
```



### Transpose

```python
a = np.arange(8).reshape(2, 4)
print(a)
print(a.T)
```
