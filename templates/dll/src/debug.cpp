#ifdef _DEBUG

#include <iostream>
#include "exports.h"

int main() {
	int result = add(1, 2);

	std::cout << result << std::endl;
	return 0;
}

#endif