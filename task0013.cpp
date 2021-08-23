#include <bits/stdc++.h>
#include <string>

using namespace std;


int main()
{
    string arr;
    cin >> arr;
    int m;
    cin >> m;
    int n;
    n = arr.length();
    int eq_arr[n - 1];


    for (int i = 0; i < n - 1; i++)
    {
        if (arr[i] == arr[i + 1])
        {
            eq_arr[i] = 1;
        }
        else
        {
            eq_arr[i] = 0;
        }
    }
    int neq_eq_arr[n];
    neq_eq_arr[0] = 0;
    for (int i = 1; i < n; i++)
    {
        neq_eq_arr[i] = neq_eq_arr[i - 1] + eq_arr[i - 1];
    }

    int left, right;
    int current_sum;
    for (int i = 0; i < m; i++)
    {
        cin >> left >> right;
        left--;
        right--;
        current_sum = neq_eq_arr[right] - neq_eq_arr[left]
    
        cout << current_sum << endl;
    }

    return 0;
}