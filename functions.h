#include <algorithm>
#include <iostream>
#include <set>
#include <vector>

bool check_noted(int n, int pos, const std::vector<int> &visited, const std::vector<std::vector<int> > &neighs) {
    for (int i = 1; i < n + 1; ++i) {
        if (visited[i] == 1) {
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
            } else {
                if (count % 2 != 1) {
                    return false;
                }
            }
        }
    }

    return true;
}
