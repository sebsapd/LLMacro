#include <windows.h>

#pragma comment(lib, "user32.lib")

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT
#endif

// mouse code definitions
#define MOUSE_LMB      256
#define MOUSE_RMB      257
#define MOUSE_MMB      258
#define MOUSE_MB4      259
#define MOUSE_MB5      260
#define MOUSE_WHEEL_UP 261
#define MOUSE_WHEEL_DOWN 262

extern "C" {

    EXPORT void send_input(int code, BOOL key_up) {
        INPUT input = {0};

        if (code < 256) {
            // Keyboard – standard scancode
            input.type = INPUT_KEYBOARD;
            input.ki.wScan = code;
            input.ki.dwFlags = KEYEVENTF_SCANCODE | (key_up ? KEYEVENTF_KEYUP : 0);
        } else {
            // mouse
            input.type = INPUT_MOUSE;

            switch (code) {
                case MOUSE_LMB:
                    input.mi.dwFlags = key_up ? MOUSEEVENTF_LEFTUP : MOUSEEVENTF_LEFTDOWN;
                    break;
                case MOUSE_RMB:
                    input.mi.dwFlags = key_up ? MOUSEEVENTF_RIGHTUP : MOUSEEVENTF_RIGHTDOWN;
                    break;
                case MOUSE_MMB:
                    input.mi.dwFlags = key_up ? MOUSEEVENTF_MIDDLEUP : MOUSEEVENTF_MIDDLEDOWN;
                    break;
                case MOUSE_MB4:
                    input.mi.dwFlags = key_up ? MOUSEEVENTF_XUP : MOUSEEVENTF_XDOWN;
                    input.mi.mouseData = XBUTTON1;
                    break;
                case MOUSE_MB5:
                    input.mi.dwFlags = key_up ? MOUSEEVENTF_XUP : MOUSEEVENTF_XDOWN;
                    input.mi.mouseData = XBUTTON2;
                    break;
                case MOUSE_WHEEL_UP:
                    input.mi.dwFlags = MOUSEEVENTF_WHEEL;
                    input.mi.mouseData = 120;
                    break;
                case MOUSE_WHEEL_DOWN:
                    input.mi.dwFlags = MOUSEEVENTF_WHEEL;
                    input.mi.mouseData = -120;
                    break;
                default:
                    return; // unknown code
            }
        }

        SendInput(1, &input, sizeof(INPUT));
    }
}
