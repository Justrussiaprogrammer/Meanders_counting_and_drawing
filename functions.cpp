#include "functions.h"

Meanders::Meanders(const int m) {
    n_ = m;
    std::cout << ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" << std::endl;
    std::cout << "- Подождите, идет инициализация класса меандров -" << std::endl;
    std::cout << ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" << std::endl;
    std::vector<bool> is_visited(n_ + 1);
    std::set<int> set_visited;
    std::vector<std::bitset<32>> neighs(n_ + 1);
    std::vector<int> future_meander(n_ + 1);
    auto start_point = std::chrono::system_clock::now();
    __go_deep_to_build(1, is_visited, set_visited, neighs, future_meander, 0);
    speed_ = std::chrono::system_clock::now() - start_point;
    std::cout << "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" << std::endl;
    std::cout << "- Инициализация класса завершена -" << std::endl;
    std::cout << "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" << std::endl;
}

std::vector<std::vector<int>> Meanders::get_all_meanders() {
    return all_meanders_;
}

void Meanders::get_meanders_info() {
    size_t answer = all_meanders_.size();
    std::string string_for_meanders1 = " найден ";
    std::string string_for_meanders2 = " меандр";
    if (answer % 10 > 4 || (4 < answer % 100 && answer % 100 < 21)) {
        string_for_meanders1 = " найдено ";
        string_for_meanders2 = " меандров";
    } else if (answer % 10 > 1) {
        string_for_meanders1 = " найдено ";
        string_for_meanders2 = " меандра";
    }
    std::cout << "Для числа " << n_ << string_for_meanders1 << answer << string_for_meanders2 << std::endl;
    std::cout << "Затрачено времени: " << speed_.count() << std::endl;
}

void Meanders::print_meanders() {
    for (std::vector<int> meander : all_meanders_) {
        std::cout << meander << std::endl;
    }
}
