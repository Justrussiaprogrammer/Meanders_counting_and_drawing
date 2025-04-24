#include "functions.h"
#include <iostream>

int main() {
    int x;
    std::cout << "Задайте размер поиска меандров:" << std::endl;
    std::cin >> x;

    Meanders meanders(x);

    meanders.get_meanders_info();

    return 0;
}
