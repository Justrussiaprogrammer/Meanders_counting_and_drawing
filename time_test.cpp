#include "Meanders_Cpp/functions.h"
#include <iostream>

int main() {
    int iterations, start, finish;
    std::cout << "Введите через пробел 3 числа: первый и последний класс меандров для проверки времени и ";
    std::cout << "количество итераций для каждого класса" << std::endl;
    std::cin >> start >> finish >> iterations;
    for (int n = start; n < finish + 1; n += 2) {
        double local_time = 0.0;
        for (int i = 0; i < iterations; ++i) {
            Meanders local_meanders(n, true);
            local_time += local_meanders.speed();
            std::cout << i << " " << local_meanders.speed() << std::endl;
        }
        std::cout << "Для меандров размера " << n;
        std::cout << " среднее время работы составляет " << local_time / iterations << std::endl;
        std::cout << std::endl;
    }

    return 0;
}
