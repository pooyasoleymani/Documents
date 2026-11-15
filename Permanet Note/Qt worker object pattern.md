---
Created Date: 2026-09-22
tags:
  - cpp
  - Qt
---
---
### Why `QMetaObject::invokeMethod(m_worker, ...)` instead of `m_worker->start()`?

Because `m_worker` lives in a **different `QThread`**.

```
m_worker->moveToThread(m_workerThread);
```

If you call:

```
m_worker->start(endpoint);
```

the function executes **immediately in the caller's thread**, not in `m_workerThread`.

That defeats the purpose of moving the worker.

With:

```cpp
QMetaObject::invokeMethod(
    m_worker,
    [this, endpoint]() {
        m_worker->start(endpoint);
    },
    Qt::QueuedConnection
);
```

Qt puts the call into the worker thread's **event queue**, so `start()` executes there.

Conceptually:

```text
ZmqStreamClient thread
        |
        | invokeMethod()
        v
   Qt event queue
        |
        v
ZmqStreamWorker thread
        |
        +--> start()
```

>This is the standard Qt **worker-object pattern**.

