#include "functions.h"
#include <fstream>

int main() {
    int x;
    std::cin >> x;

    Meanders meanders(x);

    std::vector<std::vector<int>> answer = meanders.get_all_meanders();

    std::ofstream out;
    out.open("meanders.txt");
    if (out.is_open())
    {
        for (std::vector<int> meander : answer) {
            out << meander << std::endl;
        }
    }

    return 0;
}
