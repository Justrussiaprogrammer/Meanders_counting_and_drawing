#include <algorithm>
#include <iostream>
#include <set>
#include <vector>

bool check_noted(int n, int pos, std::set<int> visited, std::vector<std::set<int> > neighs) {
    for (int x : visited) {
        if (neighs[pos].find(x) != neighs[pos].end()) {
            std::set<int> intersect_example;
            std::set_intersection(neighs[pos].begin(), neighs[pos].end(), neighs[x].begin(), neighs[x].end(),
             std::inserter(intersect_example, intersect_example.begin()));
            if (intersect_example.size() % 2 != 0) {
                return false;
            }
        } else {
            std::set<int> intersect_example;
            std::set_intersection(neighs[pos].begin(), neighs[pos].end(), neighs[x].begin(), neighs[x].end(),
             std::inserter(intersect_example, intersect_example.begin()));
            if (intersect_example.size() % 2 != 1) {
                return false;
            }
        }
    }

    return true;
}
