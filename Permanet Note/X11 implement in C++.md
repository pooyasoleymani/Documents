---
Created Date: 2026-03-05
tags:
  - cpp
  - programming
---
---

```cpp
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <iostream>
#include <ostream>
#include <string>

int main()
{
Display* display;
Window window;
XEvent event;
int screen_num;
unsigned long black_pixel, white_pixel;
// --- 1. Connect to the X Server ---
// Open a connection to the X server
display = XOpenDisplay(NULL);
if(display == NULL)
return 1;
// Get the default screen number
screen_num = DefaultScreen(display);
// Get black and white pixel values for the default screen
black_pixel = BlackPixel(display, screen_num);
white_pixel = WhitePixel(display, screen_num);
// --- 2. Create a Window ---
// Define window attributes XSetWindowAttributes attributes;
attributes.background_pixel = white_pixel; // Set background to white
attributes.event_mask = ExposureMask | KeyPressMask | ButtonPressMask | StructureNotifyMask; // Which events to listen for
// Create the window
// Parameters:
// display: Connection to the X server
// parent: The parent window (CopyFromParent means use default root window)
// x, y: Position of the window (0,0 is top-left corner)
// width, height: Dimensions of the window
// border_width: Width of the border
// depth: Color depth (CopyFromParent uses default)
// class: Visual class (InputOutput means it's a visible window)
// visual: Visual information (CopyFromParent uses default)
// valuemask: Which attributes are set
// attributes: The XSetWindowAttributes struct
window = XCreateWindow(display, RootWindow(display, screen_num),
10, 10 , 300, 400, 1, CopyFromParent, InputOutput, CopyFromParent,
CWBackingPixel | CWEventMask, &attributes
);
// Set window properties (title, etc.)
XStoreName(display, window, "Basic X11 Drawing Example");
XSetStandardProperties(display, window, "Basic X11 Drawing Example", "Basic X11 Drawing Example", None, NULL, 0, NULL);
// --- 3. Map the Window (Make it visible) ---
XMapWindow(display, window);
// --- 4. Event Loop ---
bool running = true;
while(running)
{
XNextEvent(display, &event); // Wait for the next event
// Process events
switch (event.type) {
case Expose: // Window needs to be redrawn
// Only draw if it's the actual redraw event (event.count == 0)
if (event.xexpose.window == window && event.xexpose.count == 0) {
// --- 5. Drawing ---
// Get the window's dimensions (important for resizing)
int win_width, win_height;
XWindowAttributes w_attr;
XGetWindowAttributes(display, window, &w_attr);
win_width = w_attr.width;
win_height = w_attr.height;
// Create a Graphics Context (GC) for drawing
// We create it here for simplicity, but in a real app, you'd create it once
// and reuse it.
GC gc = XCreateGC(display, window, 0, NULL);
// Set foreground color to black
XSetForeground(display, gc, black_pixel);
// Draw a line from top-left to bottom-right
XDrawLine(display, window, gc,
0, 0, // Start point (x, y)
win_width, win_height); // End point (x, y)
// Draw a rectangle (outline)
XDrawRectangle(display, window, gc,
50, 50, // Top-left corner (x, y)
100, 75); // Width, Height
// Draw some text
XSetFont(display, gc, XLoadFont(display, "-adobe-helvetica-bold-r-normal--14-*-*-*-*-*-iso8859-1")); // Example font

XDrawString(display, window, gc,
200, 100, // Position (x, y)
"Hello X11!", // Text
10); // Length of text
// Free the GC when done (if created locally)
XFreeGC(display, gc);
}
break;
case KeyPress: // A key was pressed
// If the Escape key is pressed, exit the loop
// XLookupString converts the key event to a string (or symbol)
char key_buffer[32];
KeySym keysym;
XLookupString(&event.xkey, key_buffer, sizeof(key_buffer), &keysym, NULL);
if (keysym == XK_Escape) {
	running = false;
}
break;
case ButtonPress: // A mouse button was pressed
// For simplicity, we'll just print the coordinates
std::cout << "Mouse clicked at: (" << event.xbutton.x << ", " << event.xbutton.y << ")" << std::endl;
break;
case ConfigureNotify: // Window was resized, moved, etc.
// This event is triggered when the window's size or position changes.
// We don't need to do anything specific here for this simple example,
// but in a real app, you'd re-calculate widget positions/sizes.
// The Expose event will be triggered to redraw the window content.
break;
case DestroyNotify: // Window was closed (e.g., by window manager)
running = false;
break;

default:
// Ignore other event types
break;
	}
}
// --- 6. Clean up ---
XDestroyWindow(display, window); // Destroy the window
XCloseDisplay(display); // Close the connection to the X server
return 0;
}
```