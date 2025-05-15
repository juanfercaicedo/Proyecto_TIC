#include <iostream>
#include <vector>

std::vector<unsigned long long> fibonacci_sequence(int n)
{
    std::vector<unsigned long long> sequence;
    if (n <= 0)
        return sequence;

    sequence.push_back(0);
    if (n == 1)
        return sequence;

    sequence.push_back(1);
    for (int i = 2; i < n; ++i)
    {
        sequence.push_back(sequence[i - 1] + sequence[i - 2]);
    }
    return sequence;
}

int main()
{
    int terms;
    std::cout << "Enter the number of Fibonacci terms to generate: ";
    std::cin >> terms;

    std::vector<unsigned long long> sequence = fibonacci_sequence(terms);

    std::cout << "Fibonacci sequence:\n";
    for (const auto &num : sequence)
    {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    return 0;
}
