#include "functions.h"
#include <chrono>
#include <string>

size_t global_answer = 0;


void go_deep_to_build(int n, int is_even, std::set<int> &visited, std::vector<std::set<int> > &neighs,
 std::vector<int> &sequence) {
    if (visited.size() == n) {
        ++global_answer;
        std::cout << "Найдена комбинация номер " << global_answer << ": ";
        for (int elem : sequence) {
            std::cout << elem << ", ";
        }
        std::cout << std::endl;
        for (int i = 0; i < n; ++i) {
            std::cout << '-';
        }
        std::cout << std::endl;
        return;
    }
    for (int i = is_even; i < n + 1; i += 2) {
        if (visited.find(i) == visited.end()) {
            for (int j = i + 1; j < n + 1; ++j) {
                if (visited.find(j) == visited.end()) {
                    neighs[i].insert(j);
                    neighs[j].insert(i);
                }
            }
            if (!check_noted(n, i, visited, neighs)) {
                for (int j = i + 1; j < n + 1; ++j) {
                    if (visited.find(j) == visited.end()) {
                        neighs[i].erase(j);
                        neighs[j].erase(i);
                    }
                }
                continue;
            }
                
            visited.insert(i);

            sequence[visited.size() - 1] = i;
            go_deep_to_build(n, 3 - is_even, visited, neighs, sequence);
            sequence[visited.size() - 1] = i;

            for (int j = i + 1; j < n + 1; ++j) {
                if (visited.find(j) == visited.end()) {
                    neighs[i].erase(j);
                    neighs[j].erase(i);
                }
            }

            visited.erase(i);
        }
    }
}


int main() {
    int x;

    std::cout << "Задайте размер поиска меандров:" << std::endl;

    std::cin >> x;
    std::vector<std::set<int> > X_all(x + 1);
    std::set<int> empty_set;
    std::vector<int> empty_vector(x);

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
