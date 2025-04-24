#pragma once

#include <algorithm>
#include <bitset>
#include <iostream>
#include <set>
#include <vector>

template <class T>
std::ostream& operator << (std::ostream& os, const std::vector<T>& v) {
    for (typename std::vector<T>::const_iterator ii = v.begin(); ii != v.end(); ++ii)
    {
        os << *ii << " ";
    }
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
                    if (!__check_noted(i, set_visited, neighs)) {
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

        bool __check_noted(int pos, std::set<int>& visited, std::vector<std::bitset<32>>& neighs) {
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
