#include <chrono>
#include <string>
#include <stdio.h>
#include <algorithm>
#include <iostream>
#include <set>
#include <vector>

bool check_noted(int n, int pos, const std::vector<int>& sequence, const std::vector<std::vector<int> >& neighs) {
    for (auto i : sequence) {
        if (i > 0) {
            int count = 0;
            for (int j = 1; j < n + 1; ++j) {
                if (neighs[pos][j] == 1 && neighs[i][j] == 1) {
                    ++count;
                }
            }

            if (neighs[pos][i] == 1) {
                if (count % 2 != 0) {
                    return false;
                }
            }
            else {
                if (count % 2 != 1) {
                    return false;
                }
            }
        }
        else {
            return true;
        }
    }

    return true;
}

int global_answer = 0;

void go_deep_to_build(int n, std::vector<int>& visited, std::vector<std::vector<int>>& neighs,
    std::vector<int>& sequence, int step) {
    if (step == n) {
        ++global_answer;
        /*printf("Найдена комбинация номер %d: ", global_answer);
        for (int elem : sequence) {
            printf("%d, ", elem);
        }
        printf("\n");
        for (int i = 0; i < n; ++i) {
            printf("-");
        }
        printf("\n");*/
        return;
    }
    for (int i = 2 - ((step + 1) % 2); i < n + 1; i += 2) {
        if (visited[i] == 0) {
            for (int j = i + 1; j < n + 1; ++j) {
                if (visited[j] == 0) {
                    neighs[i][j] = 1;
                    neighs[j][i] = 1;
                }
            }
            if (!check_noted(n, i, sequence, neighs)) {
                for (int j = i + 1; j < n + 1; ++j) {
                    if (visited[j] == 0) {
                        neighs[i][j] = 0;
                        neighs[j][i] = 0;
                    }
                }
                continue;
            }

            visited[i] = 1;

            sequence[step] = i;
            go_deep_to_build(n, visited, neighs, sequence, step + 1);

            for (int j = i + 1; j < n + 1; ++j) {
                if (visited[j] == 0) {
                    neighs[i][j] = 0;
                    neighs[j][i] = 0;
                }
            }
            sequence[step] = 0;
            visited[i] = 0;
        }
    }
}


int main() {
    int x;

    std::cout << "Задайте размер поиска меандров:" << std::endl;

    std::cin >> x;
    std::vector<std::vector<int> > X_all(x + 1);

    for (int i = 0; i < x + 1; ++i) {
        for (int j = 0; j < x + 1; ++j) {
            X_all[i].push_back(0);
        }
    }

    std::vector<int> empty_visited(x + 1);
    std::vector<int> empty_vector(x, 0);

    auto start_point = std::chrono::system_clock::now();
    go_deep_to_build(x, empty_visited, X_all, empty_vector, 0);
    std::string string_for_meanders1 = " найден ";
    std::string string_for_meanders2 = " меандр";
    if (global_answer % 10 > 4 || (4 < global_answer % 100 && global_answer % 100 < 21) || global_answer == 0) {
        string_for_meanders1 = " найдено ";
        string_for_meanders2 = " меандров";
    }
    else if (global_answer % 10 > 1) {
        string_for_meanders1 = " найдено ";
        string_for_meanders2 = " меандра";
    }
    std::cout << "Для числа " << x << string_for_meanders1 << global_answer << string_for_meanders2 << std::endl;

    auto end_point = std::chrono::system_clock::now();
    std::chrono::duration<double> between = end_point - start_point;

    std::cout << "Всего прошло: " << between.count() << std::endl;

    return 0;
}