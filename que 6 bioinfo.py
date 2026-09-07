seq1 = "ACGTATCGCGTATA"
seq2 = "GATGCGTATCG"

match_score = 2
mismatch_score = -1
gap_penalty = -2

n, m = len(seq1), len(seq2)

score = [[0] * (m + 1) for _ in range(n + 1)]
max_score = 0
max_pos = (0, 0)

for i in range(1, n + 1):
    for j in range(1, m + 1):
        match = score[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_score)
        delete = score[i-1][j] + gap_penalty
        insert = score[i][j-1] + gap_penalty
        score[i][j] = max(0, match, delete, insert)

        if score[i][j] > max_score:
            max_score = score[i][j]
            max_pos = (i, j)

#tracebaack 
aligned1, aligned2 = "", ""
i, j = max_pos

while i > 0 and j > 0 and score[i][j] != 0:
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

start_i, end_i = i, max_pos[0]  

print("Best Local Alignment:")
print(aligned1)
print(aligned2)
print("Score:", max_score)

full_seq1 = seq1[:start_i] + aligned1 + seq1[end_i:]
full_seq2 = ("-" * start_i) + aligned2 + ("-" * (n - end_i))

print("Full alignment view:")
print("Seq1:", full_seq1)
print("Seq2:", full_seq2)