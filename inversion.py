def merge_count(a, temp, left, mid, right):
    i, j, k = left, mid + 1, left
    count = 0

    while i <= mid and j <= right:
        if a[i] <= a[j]:
            temp[k] = a[i]
            i += 1
        else:
            temp[k] = a[j]
            j += 1
            count += mid - i + 1
        k += 1

    while i <= mid:
        temp[k] = a[i]
        i += 1
        k += 1
    while j <= right:
        temp[k] = a[j]
        j += 1
        k += 1

    a[left:right + 1] = temp[left:right + 1]
    return count


def sort_count(a, temp, left, right):
    if left >= right:
        return 0

    mid = left + (right - left) // 2
    count = sort_count(a, temp, left, mid)
    count += sort_count(a, temp, mid + 1, right)
    count += merge_count(a, temp, left, mid, right)
    return count


def count_inversions(a):
    temp = [0] * len(a)
    return sort_count(a, temp, 0, len(a) - 1)


def main():
    n = int(input())
    a = list(map(int, input().split()))[:n]
    print(count_inversions(a))


if __name__ == "__main__":
    main()
