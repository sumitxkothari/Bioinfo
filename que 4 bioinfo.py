seq1 = "ACAGTCGAACG"
seq2 = "ACCGTCCG"

match_score = 2
mismatch_score = -1
gap_penalty = -2

n, m = len(seq1), len(seq2)

score = [[0] * (m + 1) for _ in range(n + 1)]

for i in range(n + 1):
    score[i][0] = i * gap_penalty
for j in range(m + 1):
    score[0][j] = j * gap_penalty

for i in range(1, n + 1):
    for j in range(1, m + 1):
        match = score[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_score)
        delete = score[i-1][j] + gap_penalty
        insert = score[i][j-1] + gap_penalty
        score[i][j] = max(match, delete, insert)

#tracebaack
aligned1, aligned2 = "", ""
i, j = n, m
while i > 0 and j > 0:
    current = score[i][j]
    if current == score[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_score):
        aligned1 = seq1[i-1] + aligned1
        aligned2 = seq2[j-1] + aligned2
        i -= 1
        j -= 1
    elif current == score[i-1][j] + gap_penalty:
        aligned1 = seq1[i-1] + aligned1
        aligned2 = "-" + aligned2
        i -= 1
    else:
        aligned1 = "-" + aligned1
        aligned2 = seq2[j-1] + aligned2
        j -= 1

while i > 0:
    aligned1 = seq1[i-1] + aligned1
    aligned2 = "-" + aligned2
    i -= 1

while j > 0:
    aligned1 = "-" + aligned1
    aligned2 = seq2[j-1] + aligned2
    j -= 1

print("Optimal Alignment:")
print(aligned1)
print(aligned2)
print("Optimal Alignment Score:", score[n][m])