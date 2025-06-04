import time

with open("lotr.txt", encoding='utf-8') as f:
    text = f.readlines()

S = ' '.join(text).lower()


def naiwna(S, W):
    m = 0
    i = 0
    out = []
    count = 0
    while m < len(S):
        while i < len(W) and m + i < len(S):
            count += 1
            if S[m + i] == W[i]:
                i += 1
            else:
                m += 1
                i = 0
                break
        else:
            out.append(m)
            m += 1
            i = 0
    return out, count


def rabinKarp(S, W):
    d = 256

    q = 101  # liczba pierwsza

    def hash(word):
        hw = 0
        for i in range(len(W)):  # N - to długość wzorca
            hw = (hw * d + ord(word[
                                   i])) % q  # dla d będącego potęgą 2 można mnożenie zastąpić shiftem uzyskując pewne przyspieszenie obliczeń

        return hw

    has_W = hash(W)
    m = 0
    count = 0
    collision = 0
    out = []
    while m + len(W) <= len(S):
        hash_S = hash(S[m:m + len(W)])
        count += 1
        if hash_S == has_W:
            i = 0
            collision += 1
            while i < len(W) and m + i < len(S):
                count += 1
                if S[m + i] == W[i]:
                    i += 1
                else:
                    break
            else:
                collision -= 1
                out.append(m)
        m += 1
    return out, count, collision


def rabinKarp_rolling(S, W):
    d = 256

    q = 101  # liczba pierwsza

    def hash(word):
        hw = 0
        for i in range(len(W)):  # N - to długość wzorca
            hw = (hw * d + ord(word[
                                   i])) % q  # dla d będącego potęgą 2 można mnożenie zastąpić shiftem uzyskując pewne przyspieszenie obliczeń

        return hw

    h = 1
    for i in range(len(W) - 1):
        h = (h * d) % q

    has_W = hash(W)
    m = 0
    count = 0
    collision = 0
    out = []
    hash_S = hash(S[:len(W)])
    while m + len(W) <= len(S):
        count += 1
        if hash_S == has_W:
            i = 0
            collision += 1
            while i < len(W) and m + i < len(S):
                count += 1
                if S[m + i] == W[i]:
                    i += 1
                else:
                    break
            else:
                out.append(m)
        if m < len(S) - len(W):
            hash_S = (d * (hash_S - ord(S[m]) * h) + ord(S[m + len(W)])) % q
            if hash_S < 0:
                hash_S += q
        m += 1
    return out, count, collision


def kmp_table(W):
    T = [-1] * (len(W) + 1)
    pos = 1
    cnd = 0
    while pos < len(W):
        if W[pos] == W[cnd]:
            T[pos] = T[cnd]
        else:
            T[pos] = cnd
            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]
        pos += 1
        cnd += 1
    T[pos] = cnd
    return T


def kmp_search(S, W):
    m = 0
    i = 0
    count = 0
    T = kmp_table(W)
    out = []

    while m < len(S):
        count += 1
        if W[i] == S[m]:
            m += 1
            i += 1
            if i == len(W):
                out.append(m - i)
                i = T[i]
        else:
            i = T[i]
            if i < 0:
                m += 1
                i += 1

    return out, count, T

W = "i shan’t often be visiting the shire openly again.".lower()
t_start = time.perf_counter()
out, count = naiwna(S, W)
t_stop = time.perf_counter()
print(f"{len(out)};{count};{t_stop - t_start:.7f}")

t_start = time.perf_counter()
out, count, collision = rabinKarp(S, W)
t_stop = time.perf_counter()
print(f"{len(out)};{count};{collision};{t_stop - t_start:.7f}")

t_start = time.perf_counter()
out, count, collision = rabinKarp_rolling(S, W)
t_stop = time.perf_counter()
print(f"{len(out)};{count};{collision};{t_stop - t_start:.7f}")

t_start = time.perf_counter()
out, count, T = kmp_search(S, W)
t_stop = time.perf_counter()
print(f"{len(out)};{count};{T};{t_stop - t_start:.7f}")