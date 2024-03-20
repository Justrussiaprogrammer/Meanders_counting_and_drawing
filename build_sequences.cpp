#include <iostream>
#include <vector>
#include <set>
#include <chrono>
#include <string>

void go_deep_to_build(int n, int is_even, std::set<int> visited, std::vector<std::set<int> > neighs, std::vector<int>sequence) {
    return;
}

size_t global_answer = 0;

int main() {
    int x;

    std::cin >> x;
    std::vector<std::set<int> > X_all(x + 1);
    std::set<int> empty_set;
    std::vector<int> empty_vector;

    std::cout << "Задайте размер поиска меандров:" << std::endl;

    auto start_point = std::chrono::system_clock::now();
    go_deep_to_build(x, 1, empty_set, X_all, empty_vector);
    std::string string_for_meanders1 = " найден ";
    std::string string_for_meanders2 = " меандр";
    if (global_answer % 10 > 4 || (4 < global_answer % 100 && global_answer % 100 < 21) || global_answer == 0) {
        string_for_meanders1 = " найдено ";
        string_for_meanders2 = " меандров";
    } else if (global_answer % 10 > 1) {
        string_for_meanders1 = " найдено ";
        string_for_meanders2 = " меандра";
    }
    std::cout << "Для числа " << x << string_for_meanders1 << global_answer << string_for_meanders2 << std::endl;

    auto end_point = std::chrono::system_clock::now();
    std::chrono::duration<double> between = end_point - start_point;

    std::cout << "Всего прошло: " << between.count() << std::endl;

    return 0;
}
