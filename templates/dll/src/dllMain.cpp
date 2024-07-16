#ifndef _DEBUG

#include "windows.h"
#include "exports.h"

BOOL APIENTRY DllMain(HMODULE hModule,
    DWORD  ul_reason_for_call,
    LPVOID lpReserved
)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        // 进程加载DLL时调用
        // DLL被加载时调用
        MessageBox(NULL, "DLL 加载完成！2", "提示", MB_OK);
        break;

    case DLL_THREAD_ATTACH:
        // 线程创建时调用
        break;

    case DLL_THREAD_DETACH:
        // 线程退出时调用
        break;

    case DLL_PROCESS_DETACH:
        // 进程卸载DLL时调用
        break;
    }
    return TRUE;  // 成功处理
}

#endif
