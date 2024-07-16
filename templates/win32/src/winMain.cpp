#include <windows.h>
#include <string>

// 全局变量
HWND hEditUsername;
HWND hEditPassword;

// 窗口过程函数
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    case WM_COMMAND: {
        if (LOWORD(wParam) == 1) { // 按钮的ID
            char username[100];
            char password[100];

            GetWindowText(hEditUsername, username, 100);
            GetWindowText(hEditPassword, password, 100);

            std::string message = "Username: " + std::string(username) + "\nPassword: " + std::string(password);
            MessageBox(hwnd, message.c_str(), "Input", MB_OK);
        }
        break;
    }
    case WM_ERASEBKGND: {
        HBRUSH hBrush = CreateSolidBrush(RGB(255, 255, 255)); // 白色背景
        HBRUSH oldBrush = (HBRUSH)SelectObject((HDC)wParam, hBrush);
        RECT rect;
        GetClientRect(hwnd, &rect);
        FillRect((HDC)wParam, &rect, hBrush);
        SelectObject((HDC)wParam, oldBrush);
        DeleteObject(hBrush);
        return 1; // 处理了背景擦除
    }
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

int WINAPI WinMain(
    _In_ HINSTANCE hInstance,
    _In_opt_ HINSTANCE hPrevInstance,
    _In_ LPSTR lpCmdLine,
    _In_ int nShowCmd
) {
    // 注册窗口类
    const char CLASS_NAME[] = "Sample Window Class";

    WNDCLASS wc = {};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    // 创建窗口
    HWND hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        "Login Window",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 300, 200,
        NULL,
        NULL,
        hInstance,
        NULL
    );

    if (hwnd == NULL) {
        return 0;
    }

    // 创建控件
    CreateWindow("STATIC", "Username:", WS_VISIBLE | WS_CHILD, 10, 10, 80, 20, hwnd, NULL, hInstance, NULL);
    hEditUsername = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 10, 150, 20, hwnd, NULL, hInstance, NULL);

    CreateWindow("STATIC", "Password:", WS_VISIBLE | WS_CHILD, 10, 40, 80, 20, hwnd, NULL, hInstance, NULL);
    hEditPassword = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER | ES_PASSWORD, 100, 40, 150, 20, hwnd, NULL, hInstance, NULL);

    CreateWindow("BUTTON", "Submit", WS_VISIBLE | WS_CHILD, 100, 80, 80, 30, hwnd, (HMENU)1, hInstance, NULL);

    // 获取窗口的客户区宽度和高度
    RECT rect;
    GetWindowRect(hwnd, &rect);
    int windowWidth = rect.right - rect.left;
    int windowHeight = rect.bottom - rect.top;

    // 获取屏幕宽度和高度
    RECT screenRect = { 0 };
    SystemParametersInfo(SPI_GETWORKAREA, 0, &screenRect, 0);
    int screenWidth = screenRect.right - screenRect.left;
    int screenHeight = screenRect.bottom - screenRect.top;

    // 计算居中位置
    int x = (screenWidth - windowWidth) / 2;
    int y = (screenHeight - windowHeight) / 2;

    // 设置窗口的位置
    SetWindowPos(hwnd, HWND_TOPMOST, x, y, 0, 0, SWP_NOSIZE | SWP_NOACTIVATE);

    // 显示窗口
    ShowWindow(hwnd, nShowCmd);
    UpdateWindow(hwnd);

    // 消息循环
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}
