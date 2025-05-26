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
            hw = (hw * d + ord(word[i])) % q  # dla d będącego potęgą 2 można mnożenie zastąpić shiftem uzyskując pewne przyspieszenie obliczeń

        return hw

    has_W = hash(W)
    m = 0
    count = 0
    out = []
    while m+len(W) <= len(S):
        hash_S = hash(S[m:m + len(W)])
        count += 1
        if hash_S == has_W:
            i = 0
            while i < len(W) and m + i < len(S):
                count += 1
                if S[m + i] == W[i]:
                    i += 1
                else:
                    m += 1
                    break
            else:
                out.append(m)
        m += 1
    return out, count


t_start = time.perf_counter()
out, count = naiwna(S, "time.")
t_stop = time.perf_counter()
print(f"{len(out)};{count};{t_stop - t_start}")

t_start = time.perf_counter()
out, count = rabinKarp(S, "time.")
t_stop = time.perf_counter()
print(f"{len(out)};{count};{t_stop - t_start}")

