#include <bits/stdc++.h>
#include <string>

using namespace std;


int main()
{
    int n, k;
    cin >> n >> k;
    int arr[n];
    for (int i = 0; i < n; i++)
    {
        cin >> arr[i];
    }

    int smallest_sum;
    smallest_sum = 1000000;
    int answer;
    answer = smallest_sum;
    int current_sum;
    for (int i = 0; i < n - k + 1; i++)
    {
        current_sum = 0;
        for (int j = 0; j < k; j++)
        {
            current_sum = current_sum + arr[i + j];
        }
        if (current_sum < smallest_sum)
        {
            smallest_sum = current_sum;
            answer = i;
        }
    }

    cout << answer + 1 << endl;


    return 0;
}