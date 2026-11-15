---
Created Date: 2026-11-11
tags:
  - PE
  - cpp
---
---
---
priority: high
status: learning
tags:
- amnafzar
- windows-internals
- reverse-engineering
- portable-executable
- c++
title: AmnAfzar Challenge --- PE Parser
---

## PE Parser

> \[!abstract\] هدف این یادداشت یادگیری ساختار **Portable Executable
> (PE)**، پیاده‌سازی یک PE Parser با C++ و آماده‌شدن برای توضیح فنی پروژه
> در مصاحبه استخدامی.


## 1. شرح بخش‌های چالش
### A — پیاده‌سازی PE Parser

پیاده‌سازی یک PE Parser ساده با قابلیت خواندن تمام فیلدهای زیر:

- DOS Header
- NT Header
  - File Header
  - Optional Header
- Section Header

### B — پارس Export Directory در DLL

در صورتی که فایل ورودی از نوع DLL باشد:

- استخراج نام توابع (Function Names)
- استخراج Ordinal
- استخراج Function RVA
- تحلیل نام‌های Decorated شده
- استخراج نام کلاس و آرگومان‌های توابع در صورت امکان

> نکته: بخش مربوط به تحلیل نام‌های Decorated شده باید برای MSVC پیاده‌سازی شود.

### C — پارس Import Directory

استخراج اطلاعات زیر از Import Directory:

- نام کتابخانه‌های مورد استفاده (DLL Names)
- نام توابع Import شده از هر کتابخانه

### D — توسعه Dependency Walker

این بخش اختیاری است.

- شناسایی DLLهای Import شده توسط فایل اصلی
- بررسی DLLهای Import شده توسط هر DLL
- ادامه بررسی به‌صورت بازگشتی برای شناسایی وابستگی‌های تو در تو
### ملاحظات فایل چالش

-   نسخه‌های MSVC v120 تا v142 پیشنهاد شده‌اند.
-   کد منبع و باینری‌های Buildشده به‌صورت استاتیک باید تحویل داده شوند.
-   زمان پیشنهادی انجام چالش: پنج روز.
-   بخش D اختیاری است.
-   تحلیل جزئیات Name Mangling در فایل به MSVC محدود شده است.

> \[!warning\] مرزبندی منبع موارد بالا از متن فایل چالش استخراج شده‌اند.
> توضیحات آموزشی و پیشنهادهای طراحی در ادامه، راهنمای فنی تکمیلی هستند و
> الزاماً عین متن چالش نیستند.

## 2. PE چیست؟

**PE** مخفف **Portable Executable** و قالب رایج فایل‌های اجرایی ویندوز
است. نمونه‌ها:

-   `.exe` --- فایل اجرایی
-   `.dll` --- کتابخانه پویا
-   `.sys` --- درایور ویندوز

Windows Loader برای بارگذاری یک ماژول، ساختار PE آن را بررسی می‌کند؛ از
جمله Headerها، Sectionها، آدرس شروع اجرا و وابستگی‌های موردنیاز.

## 3. نمای کلی ساختار PE

``` text
+-----------------------------+
| DOS Header                  |
|  - e_magic                  |
|  - e_lfanew                 |
+-----------------------------+
| DOS Stub                    |
+-----------------------------+
| NT Headers                  |
|  - PE Signature             |
|  - File Header              |
|  - Optional Header          |
|      - Data Directories     |
+-----------------------------+
| Section Headers             |
+-----------------------------+
| Section Data                |
|  - .text                    |
|  - .data                    |
|  - .rdata                   |
|  - ...                      |
+-----------------------------+
```

نام‌هایی مانند `.text`، `.data` و `.rdata` رایج‌اند؛ Parser نباید فرض کند
هر فایل دقیقاً همین Sectionها را دارد.

## 4. اجزای اصلی

### 4.1 DOS Header

ساختار متناظر در Windows SDK:

``` cpp
IMAGE_DOS_HEADER
```

فیلدهای مهم:

-   `e_magic`: امضای DOS با مقدار `0x5A4D` یا `MZ`.
-   `e_lfanew`: آفست فایل (File Offset) محل شروع NT Headers.

### 4.2 NT Headers

در آفستی که `e_lfanew` مشخص می‌کند قرار دارند.

``` text
NT Headers
├── Signature
├── IMAGE_FILE_HEADER
└── IMAGE_OPTIONAL_HEADER
```

-   `Signature`: بایت‌های `PE\0\0`.
-   `File Header`: اطلاعاتی مانند معماری هدف و تعداد Sectionها.
-   `Optional Header`: اطلاعاتی مانند Entry Point، Image Base، Alignment
    و Data Directoryها.

نکته: Optional Header با وجود نامش، برای فایل‌های اجرایی معمولاً بخش مهمی
از ساختار PE است.

### 4.3 Section Headers

هر Section Header اطلاعات یک Section را مشخص می‌کند؛ از جمله:

-   نام Section
-   `VirtualAddress`
-   `VirtualSize`
-   `PointerToRawData`
-   `SizeOfRawData`
-   مشخصه‌های دسترسی و محتوا (`Characteristics`)

### 4.4 PE32 و PE32+

Magic مربوط به Optional Header را بررسی کن:

  نوع       مقدار Magic
  ------- -------------
  PE32          `0x10B`
  PE32+         `0x20B`

این دو قالب در برخی فیلدها و اندازه‌ها تفاوت دارند. از یک ساختار ثابت
برای هر دو استفاده نکن.

## 5. مفهوم کلیدی: RVA، VA و File Offset

  اصطلاح        معنی
  ------------- -------------------------------------
  File Offset   موقعیت داده در فایل روی دیسک
  RVA           آدرس نسبی داده نسبت به Image Base
  VA            آدرس مجازی داده در فضای آدرس پردازش

رابطه VA و RVA:

``` text
VA = ImageBase + RVA
```

اما RVA معمولاً با File Offset برابر نیست.

### مثال تبدیل RVA به File Offset

فرض:

``` text
Section.VirtualAddress   = 0x1000
Section.PointerToRawData = 0x0400
Target RVA               = 0x1250
```

محاسبه:

``` text
Delta = TargetRVA - VirtualAddress
      = 0x1250 - 0x1000
      = 0x250

FileOffset = PointerToRawData + Delta
           = 0x0400 + 0x0250
           = 0x0650
```

در این مثال، داده در RVA برابر `0x1250`، در آفست `0x650` فایل قرار دارد.

### شبه‌کد تبدیل

``` cpp
bool RvaToFileOffset(
    DWORD rva,
    const IMAGE_SECTION_HEADER* sections,
    WORD numberOfSections,
    DWORD& fileOffset
);
```

پیاده‌سازی نهایی باید این موارد را کنترل کند:

1.  آیا RVA در محدوده Header یا یکی از Sectionها قرار دارد؟
2.  آیا RVA در محدوده داده خام موجود در فایل است؟
3.  آیا Offset محاسبه‌شده از انتهای فایل عبور می‌کند؟
4.  آیا محاسبات باعث Integer Overflow می‌شوند؟
5.  آیا داده‌ای که قرار است خوانده شود به‌طور کامل در محدوده فایل قرار
    دارد؟

> \[!important\] نکته مصاحبه `VirtualSize` و `SizeOfRawData` مفاهیم
> یکسانی نیستند. ممکن است بخشی از فضای حافظه Section در فایل خام وجود
> نداشته باشد. بنابراین صرفاً پیدا کردن Section برای تبدیل RVA به File
> Offset کافی نیست.

## 6. Export Directory

Export Directory مشخص می‌کند یک ماژول چه Symbolهایی را برای استفاده
ماژول‌های دیگر صادر می‌کند.

اطلاعات مهم موردنیاز چالش:

-   نام تابع (در صورت وجود)
-   Ordinal
-   Function RVA

نکات تکمیلی:

-   همه Exportها الزاماً نام ندارند؛ برخی فقط با Ordinal قابل دسترسی‌اند.
-   بعضی Exportها Forwarded Export هستند؛ یعنی به Symbol یا DLL دیگری
    ارجاع می‌دهند.
-   Export Directory معمولاً پروتوتایپ تابع را ذخیره نمی‌کند.
-   برای Symbolهای C++ که با MSVC Decorate شده‌اند، می‌توان نام Symbol را
    با ابزار مناسب Undecorate کرد و اطلاعات کدگذاری‌شده در نام را بررسی
    کرد.
-   اگر نام Symbol اطلاعات کافی نداشته باشد، نباید پروتوتایپ را حدس زد.

## 7. Import Directory

Import Directory مشخص می‌کند یک ماژول برای کارکرد خود به چه کتابخانه‌ها و
Symbolهایی نیاز دارد.

مواردی که باید استخراج شوند:

-   نام DLL
-   نام تابع یا Ordinal
-   اطلاعات لازم برای شناسایی Importها

در پیاده‌سازی باید هر دو حالت Import by Name و Import by Ordinal در نظر
گرفته شوند.

## 8. Dependency Walker

بخش D چالش می‌خواهد وابستگی‌های DLLها نیز بررسی شوند.

مثال:

``` text
app.exe
├── A.dll
│   ├── C.dll
│   └── D.dll
└── B.dll
    └── C.dll
```

در این مثال `C.dll` از دو مسیر قابل دسترسی است؛ پس باید از پردازش تکراری
جلوگیری شود.

### نکات طراحی

-   برای هر ماژول، Import Directory را بخوان.
-   DLLهای وابسته را به‌صورت بازگشتی بررسی کن.
-   ماژول‌های پردازش‌شده را ثبت کن.
-   چرخه‌های وابستگی را مدیریت کن.
-   وضعیت DLLهای پیدا‌نشده یا حل‌نشده را گزارش بده.
-   بین نام DLL در Import Table و ماژولی که واقعاً در سیستم پیدا می‌شود
    تفاوت قائل شو.

> \[!warning\] محدودیت تحلیل ایستا فهرست Importها الزاماً تمام DLLهایی را
> که برنامه در زمان اجرا بارگذاری می‌کند نشان نمی‌دهد. برنامه ممکن است با
> `LoadLibrary` و `GetProcAddress` وابستگی پویا ایجاد کند. بنابراین
> ابزار این چالش را باید یک تحلیل‌گر وابستگی مبتنی بر Import Table دانست،
> نه تضمین‌کننده تمام وابستگی‌های زمان اجرا.

## 9. معماری پیشنهادی پروژه

``` text
PEParser/
├── src/
│   ├── main.cpp
│   ├── PEParser.h
│   ├── PEParser.cpp
│   ├── SectionParser.h
│   ├── SectionParser.cpp
│   ├── ExportParser.cpp
│   ├── ImportParser.cpp
│   ├── MsvcDemangler.cpp
│   └── DependencyWalker.cpp
├── samples/
└── README.md
```

مسئولیت‌های پیشنهادی:

  ماژول                مسئولیت
  -------------------- ------------------------------------
  `PEParser`           بارگذاری فایل و مدیریت ساختار اصلی
  `SectionParser`      خواندن Sectionها و تبدیل RVA
  `ExportParser`       استخراج Exportها
  `ImportParser`       استخراج Importها
  `MsvcDemangler`      تحلیل نام‌های Decorated با MSVC
  `DependencyWalker`   پیمایش گراف وابستگی DLLها

### توصیه پیاده‌سازی

فایل را به‌صورت بایت‌ها در حافظه بخوان و قبل از هر دسترسی محدوده را
اعتبارسنجی کن. از Cast مستقیم Pointer به Structure روی ورودی
غیرقابل‌اعتماد اجتناب کن؛ برای خواندن Structureها می‌توان از `memcpy` پس
از بررسی اندازه و Offset استفاده کرد.

## 10. تابع پایه برای خواندن امن داده

نمونه اولیه با C++:

``` cpp
#include <Windows.h>
#include <cstdint>
#include <cstring>
#include <vector>

template <typename T>
bool ReadAt(
    const std::vector<uint8_t>& data,
    uint64_t offset,
    T& result
)
{
    if (offset > data.size())
        return false;

    size_t position = static_cast<size_t>(offset);

    if (sizeof(T) > data.size() - position)
        return false;

    memcpy(&result, &data[position], sizeof(T));

    return true;
}
```

این تابع:

1.  Offset را بررسی می‌کند.
2.  مطمئن می‌شود اندازه Structure در محدوده فایل قرار دارد.
3.  داده را با `memcpy` کپی می‌کند.
4.  در صورت نامعتبر بودن محدوده، `false` برمی‌گرداند.

این کد یک تابع پایه است، نه Parser کامل. اعتبارسنجی امضاها، ساختارهای
داخلی و محدوده تمام داده‌های ارجاع‌شده نیز لازم است.

## 11. برنامه پیشنهادی پنج‌روزه

  -----------------------------------------------------------------------
  روز                     موضوع                   خروجی
  ----------------------- ----------------------- -----------------------
  1                       PE Basics، DOS Header،  Parser اولیه
                          NT Headers و Section    
                          Headers                 

  2                       RVA و Export Directory  استخراج Exportها

  3                       MSVC Name Mangling و    استخراج Importها و
                          Import Directory        تحلیل Symbolها

  4                       Dependency Walker       پیمایش بازگشتی
                                                  وابستگی‌ها

  5                       تست، رفع اشکال،         نسخه تحویلی
                          مستندسازی و آماده‌سازی   
                          مصاحبه                  
  -----------------------------------------------------------------------

## 12. ابزارهای تست و مقایسه

برای مقایسه خروجی Parser با ابزارهای موجود Visual Studio:

``` cmd
dumpbin /headers sample.exe
dumpbin /imports sample.exe
dumpbin /exports sample.dll
```

خروجی برنامه خودمان را با خروجی `dumpbin` مقایسه می‌کنیم.

## 13. پرسش‌های مصاحبه

### 1. What is PE format?

PE مخفف Portable Executable است و قالب استاندارد فایل‌های اجرایی ویندوز،
DLLها و برخی فایل‌های سیستمی محسوب می‌شود.

### 2. What is e_lfanew?

فیلدی در `IMAGE_DOS_HEADER` است که File Offset مربوط به شروع NT Headers
را مشخص می‌کند.

### 3. What is the difference between RVA and VA?

RVA آدرس نسبی نسبت به Image Base است؛ VA آدرس مجازی نهایی در فضای آدرس
پردازش است.

``` text
VA = ImageBase + RVA
```

### 4. What is the difference between PE32 and PE32+?

Magic مربوط به PE32 برابر `0x10B` و PE32+ برابر `0x20B` است. PE32+ قالب
۶۴ بیتی PE است و ساختار Optional Header آن با PE32 تفاوت دارد.

### 5. What is an Import Directory?

ساختاری است که DLLها و Symbolهای موردنیاز یک ماژول را برای Import مشخص
می‌کند.

### 6. What is an Export Directory?

ساختاری است که Symbolهای Exportشده توسط یک ماژول را معرفی می‌کند.

### 7. What is Name Mangling?

فرایند Decorate کردن نام Symbolهای C++ است. در MSVC نام Decorated
می‌تواند اطلاعاتی مانند کلاس، نوع پارامترها و Calling Convention را
کدگذاری کند.

### 8. What is an Ordinal?

شماره‌ای است که برای شناسایی یک Export به کار می‌رود و می‌تواند جایگزین
دسترسی از طریق نام Symbol شود.

### 9. Why is RVA-to-File-Offset conversion necessary?

چون Data Directoryها و بسیاری از ارجاع‌های داخلی PE با RVA بیان می‌شوند،
اما برای خواندن داده از فایل روی دیسک به File Offset نیاز داریم.

### 10. Does Import Directory show every runtime dependency?

خیر. وابستگی‌هایی که در زمان اجرا با روش‌هایی مانند `LoadLibrary` بارگذاری
می‌شوند، لزوماً در Import Table ثابت فایل دیده نمی‌شوند.

## 14. چک‌لیست تحویل

-   [ ] خواندن و اعتبارسنجی DOS Header
-   [ ] خواندن NT Signature
-   [ ] خواندن تمام فیلدهای File Header
-   [ ] پشتیبانی از PE32 و PE32+
-   [ ] خواندن Optional Header با توجه به اندازه واقعی آن
-   [ ] خواندن Section Headers
-   [ ] پیاده‌سازی امن RVA-to-File-Offset
-   [ ] پارس Export Directory
-   [ ] پشتیبانی از Exportهای Ordinal-only
-   [ ] تشخیص Forwarded Export
-   [ ] تحلیل Symbolهای Decorated شده با MSVC
-   [ ] پارس Import Directory
-   [ ] پشتیبانی از Import by Name و Import by Ordinal
-   [ ] پیمایش وابستگی‌های DLL
-   [ ] مدیریت چرخه و DLL تکراری
-   [ ] تست با فایل‌های معتبر و خراب
-   [ ] مقایسه خروجی با DUMPBIN
-   [ ] تهیه README و مستندات
-   [ ] Build نسخه استاتیک طبق شرایط چالش
-   [ ] تحویل Source Code و Binary

## 15. مسیر یادگیری

-   \[\[01 - PE Fundamentals\]\]
-   \[\[02 - DOS Header and NT Headers\]\]
-   \[\[03 - Section Headers and RVA Mapping\]\]
-   \[\[04 - Export Directory\]\]
-   \[\[05 - MSVC Name Mangling\]\]
-   \[\[06 - Import Directory\]\]
-   \[\[07 - Dependency Walker\]\]
-   \[\[08 - PE Parser Interview Questions\]\]

## 16. قدم بعدی

**اولین تمرین عملی:** برنامه‌ای بنویس که یک فایل EXE یا DLL را باز کند و
موارد زیر را چاپ کند:

1.  مقدار `e_magic`
2.  مقدار `e_lfanew`
3.  NT Signature
4.  تعداد Sectionها
5.  مقدار Optional Header Magic
6.  نوع PE (PE32 یا PE32+)

بعد خروجی را با `dumpbin /headers` مقایسه کن.

> \[!question\] سؤال برای شروع در یک فایل PE، چرا نمی‌توانیم فرض کنیم که
> `e_lfanew` همیشه برابر `0x80` است؟

------------------------------------------------------------------------

# منابع

## فایل اصلی چالش

-   `PE_Parser.pdf` --- فایل آپلودشده در این پروژه.

## منابع تکمیلی برای مطالعه

-   [Microsoft PE
    Format](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format)
-   [Microsoft
    UnDecorateSymbolName](https://learn.microsoft.com/en-us/windows/win32/api/dbghelp/nf-dbghelp-undecoratesymbolname)
-   [Visual C++ Name Mangling ---
    Wikiversity](https://en.wikiversity.org/wiki/Visual_C%2B%2B_name_mangling)

#tags #PE #WindowsInternals #ReverseEngineering #CPlusPlus #AmnAfzar