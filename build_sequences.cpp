#include "functions.h"
#include <chrono>
#include <string>
#include <iostream>


int main() {
    int x;
    std::string type_output;
    bool is_do_out = false;

    std::cout << "Задайте размер поиска меандров:" << std::endl;

    std::cin >> x;

    Meanders meanders(x);

    meanders.get_meanders_info();

    return 0;
}
