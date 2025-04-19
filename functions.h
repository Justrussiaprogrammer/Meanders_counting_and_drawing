#include <algorithm>
#include <bitset>
#include <iostream>
#include <set>
#include <vector>
#include <cmath>

template <class T>
std::ostream& operator << (std::ostream& os, const std::vector<T>& v) 
{
    os << "[";
    for (typename std::vector<T>::const_iterator ii = v.begin(); ii != v.end(); ++ii)
    {
        os << *ii << ", ";
    }
    os << "end]";
    return os;
}


// Размер меандров считается ограниченным 32
class Meanders {
    private:
        std::vector<std::vector<int>> all_meanders_;
        std::chrono::duration<double> speed_;
        int n_;

        void __go_deep_to_build(int is_even, std::vector<bool>& visited, std::set<int>& set_visited,
            std::vector<std::bitset<32>>& neighs, std::vector<int>& to_answer, int depth) {
            if (depth == n_) {
                all_meanders_.push_back(to_answer);
                return;
            }
            for (int i = is_even; i < n_ + 1; i += 2) {
                if (!visited[i]) {
                    for (int j = i + 1; j < n_ + 1; ++j) {
                        if (visited[j] == 0) {
                            neighs[i].set(j);
                            neighs[j].set(i);
                        }
                    }
                    if (!check_noted(i, set_visited, neighs)) {
                        for (int j = i + 1; j < n_ + 1; ++j) {
                            if (!visited[j]) {
                                neighs[i].reset(j);
                                neighs[j].reset(i);
                            }
                        }
                        continue;
                    }
                    visited[i] = true;
                    set_visited.insert(i);
                    to_answer[depth] = i;
                    __go_deep_to_build(3 - is_even, visited, set_visited, neighs, to_answer, depth + 1);
                    to_answer[depth] = 0;
                    for (int j = i + 1; j < n_ + 1; ++j) {
                        if (!visited[j]) {
                            neighs[i].reset(j);
                            neighs[j].reset(i);
                        }
                    }
                    visited[i] = false;
                    set_visited.erase(i);
                }
            }
        }

        bool check_noted(int pos, std::set<int>& visited, std::vector<std::bitset<32>>& neighs) {
            for (int x : visited) {
                if (neighs[pos][x] == 1) {
                    std::bitset<32> land = neighs[pos] & neighs[x];
                    if (land.count() % 2 == 1) {
                        return false;
                    }
                } else {
                    std::bitset<32> land = neighs[pos] & neighs[x];
                    if (land.count() % 2 == 0) {
                        return false;
                    }
                }
            }
            return true;
        }

    public:
        Meanders(int m);

        std::vector<std::vector<int>> get_all_meanders();
        void get_meanders_info();
        void print_meanders();

        void head(size_t m=10) {
            for (int i = 0; i < std::min(all_meanders_.size(), m); ++i) {
                std::cout << all_meanders_[i] << std::endl;
            }
        }

        void tail(size_t m=10) {
            for (int i = all_meanders_.size() - std::min(all_meanders_.size(), m); i < all_meanders_.size(); ++i) {
                std::cout << all_meanders_[i] << std::endl;
            }
        }
};


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
