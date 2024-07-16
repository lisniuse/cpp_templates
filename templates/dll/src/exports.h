#pragma once

#ifdef _DEBUG
#define EXPORT
#else
#define EXPORT extern "C" _declspec(dllexport)
#endif

EXPORT int add(int a, int b);
