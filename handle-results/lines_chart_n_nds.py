import matplotlib.pyplot as plt

experiment_1_front_nums = [8, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
experiment_1_n_nds = [8, 9, 9, 5, 6, 9, 6, 7, 8, 9, 11, 12, 12, 6, 11, 14, 3, 4, 6, 8, 7, 13, 4, 5, 7, 6, 7, 9, 4, 9, 8,
                      7, 8, 9, 14, 14, 19, 19, 13, 14, 16, 16, 12, 18, 17, 13, 13, 12, 11, 13, 11, 11, 14, 20, 19, 26,
                      17, 19, 17, 22, 20, 19, 25, 18, 23, 23, 26, 31, 28, 22, 26, 23, 20, 26, 27, 27, 25, 29, 25, 27,
                      25, 23, 27, 18, 21, 30, 28, 27, 27, 21, 25, 27, 30, 31, 28, 28, 29, 30, 35, 26, 35, 31, 35, 35,
                      32, 30, 32, 37, 32, 34, 35, 37, 38, 37, 37, 39, 38, 40, 39, 40, 41, 46, 53, 46, 48, 46, 48, 46,
                      46, 49, 46, 44, 48, 47, 51, 52, 50, 49, 53, 50, 49, 49, 47, 53, 50, 54, 49, 53, 55, 55, 53, 51,
                      48, 48, 45, 49, 54, 50, 57, 60, 51, 46, 47, 54, 52, 54, 55, 54, 50, 55, 53, 52, 55, 59, 54, 50,
                      51, 48, 54, 48, 56, 57, 58, 58, 61, 55, 63, 62, 63, 65, 60, 63, 64, 65, 67, 72, 68, 59, 60, 63]
experiment_2_front_nums = [8, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
experiment_2_n_nds = [6, 7, 9, 10, 6, 8, 9, 7, 11, 10, 10, 8, 8, 10, 8, 7, 10, 6, 7, 9, 7, 4, 5, 7, 7, 11, 7, 13, 13,
                      21, 8, 14, 17, 16, 19, 19, 21, 18, 17, 15, 20, 20, 23, 17, 23, 20, 22, 22, 15, 13, 17, 22, 23, 19,
                      16, 24, 27, 20, 20, 23, 22, 21, 21, 19, 22, 24, 23, 22, 25, 19, 16, 17, 18, 22, 21, 27, 26, 24,
                      28, 28, 22, 24, 19, 26, 19, 15, 20, 16, 16, 21, 7, 9, 9, 11, 11, 11, 10, 14, 11, 15, 14, 17, 17,
                      17, 14, 17, 23, 22, 20, 17, 17, 21, 20, 23, 15, 15, 22, 18, 24, 23, 17, 16, 16, 19, 18, 15, 21,
                      22, 22, 24, 21, 18, 11, 14, 17, 15, 20, 18, 18, 17, 19, 20, 23, 17, 22, 19, 25, 19, 22, 20, 22,
                      25, 19, 22, 26, 20, 25, 21, 25, 24, 21, 24, 22, 21, 31, 22, 22, 29, 30, 26, 25, 21, 25, 22, 28,
                      31, 30, 27, 29, 29, 33, 29, 36, 31, 29, 32, 27, 26, 26, 30, 21, 27, 24, 28, 29, 29, 30, 26, 27,
                      26]
experiment_3_front_nums = [8, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
experiment_3_n_nds = [8, 8, 10, 10, 11, 16, 12, 7, 10, 7, 7, 10, 10, 8, 9, 4, 6, 7, 9, 9, 8, 11, 12, 12, 13, 14, 10, 13,
                      14, 13, 12, 12, 20, 14, 16, 21, 22, 20, 28, 24, 20, 26, 23, 24, 21, 22, 20, 27, 27, 29, 32, 33,
                      25, 27, 26, 33, 28, 25, 28, 23, 35, 27, 30, 33, 27, 33, 30, 32, 34, 32, 35, 33, 35, 31, 30, 35,
                      32, 39, 27, 38, 32, 35, 36, 31, 30, 31, 29, 29, 31, 40, 34, 38, 37, 31, 39, 21, 30, 32, 43, 39,
                      36, 32, 42, 38, 40, 42, 46, 34, 42, 43, 44, 36, 39, 47, 42, 44, 39, 42, 36, 43, 41, 43, 44, 45,
                      48, 42, 50, 51, 38, 46, 53, 45, 44, 48, 41, 41, 47, 51, 56, 48, 51, 43, 39, 41, 45, 44, 44, 41,
                      42, 39, 50, 50, 43, 44, 44, 43, 42, 43, 43, 49, 55, 50, 50, 44, 40, 40, 42, 46, 43, 48, 47, 53,
                      52, 47, 44, 46, 53, 59, 57, 51, 61, 47, 58, 53, 56, 49, 59, 53, 51, 52, 48, 54, 51, 52, 53, 52,
                      46, 50, 54, 50]
experiment_4_front_nums = [5, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
experiment_4_n_nds = [4, 6, 10, 9, 9, 12, 10, 14, 17, 12, 10, 7, 8, 10, 7, 9, 8, 8, 6, 6, 7, 8, 8, 9, 10, 10, 9, 8, 8,
                      8, 7, 9, 11, 8, 8, 12, 12, 14, 11, 12, 11, 8, 6, 6, 12, 12, 13, 14, 14, 17, 9, 9, 9, 8, 9, 12, 13,
                      15, 11, 16, 15, 16, 15, 12, 17, 18, 15, 21, 16, 14, 13, 15, 18, 20, 18, 10, 19, 22, 20, 21, 17,
                      22, 22, 17, 20, 22, 21, 23, 23, 18, 18, 17, 18, 16, 20, 21, 21, 23, 21, 23, 19, 24, 24, 24, 22,
                      25, 25, 23, 25, 27, 26, 28, 26, 24, 27, 20, 31, 31, 29, 27, 24, 24, 23, 26, 27, 27, 24, 25, 23,
                      22, 27, 23, 21, 20, 16, 18, 22, 21, 20, 21, 23, 18, 24, 25, 22, 24, 22, 20, 27, 24, 22, 27, 24,
                      23, 22, 24, 24, 23, 29, 30, 31, 28, 30, 28, 29, 27, 32, 27, 28, 25, 26, 27, 32, 24, 23, 22, 23,
                      26, 25, 22, 26, 24, 25, 24, 25, 27, 25, 20, 22, 19, 20, 24, 20, 19, 21, 20, 21, 21, 21, 19]
experiment_5_front_nums = [5, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1,
                           2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
experiment_5_n_nds = [4, 5, 5, 8, 8, 8, 13, 11, 3, 2, 3, 4, 4, 3, 5, 5, 4, 5, 5, 3, 4, 7, 9, 4, 6, 6, 6, 6, 7, 9, 7, 9,
                      5, 7, 9, 9, 14, 8, 6, 7, 6, 6, 11, 12, 15, 10, 8, 7, 9, 8, 10, 9, 11, 11, 12, 11, 15, 10, 13, 15,
                      16, 15, 15, 16, 18, 23, 16, 15, 14, 14, 15, 14, 13, 14, 15, 16, 12, 15, 16, 17, 18, 8, 9, 12, 10,
                      10, 10, 14, 9, 13, 12, 14, 13, 17, 19, 18, 18, 19, 19, 15, 18, 16, 17, 19, 22, 20, 24, 19, 18, 18,
                      20, 15, 19, 18, 18, 17, 16, 20, 18, 19, 21, 16, 17, 16, 19, 20, 22, 15, 16, 17, 16, 12, 17, 16,
                      17, 16, 15, 15, 18, 18, 21, 20, 18, 21, 18, 21, 16, 21, 14, 17, 15, 15, 13, 12, 15, 14, 14, 15,
                      14, 15, 17, 17, 15, 16, 16, 16, 19, 18, 17, 17, 16, 17, 14, 18, 22, 18, 17, 17, 17, 17, 18, 19,
                      18, 18, 22, 20, 18, 18, 18, 18, 19, 19, 19, 18, 16, 16, 18, 18, 18, 19]
experiment_6_front_nums = [5, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
experiment_6_n_nds = [5, 6, 9, 5, 8, 11, 14, 16, 16, 14, 16, 14, 8, 7, 8, 10, 10, 11, 5, 9, 6, 8, 6, 7, 7, 7, 9, 9, 9,
                      9, 10, 13, 16, 14, 10, 12, 15, 16, 15, 10, 9, 11, 7, 11, 11, 10, 15, 14, 16, 18, 18, 19, 18, 17,
                      19, 18, 18, 15, 14, 17, 19, 22, 19, 17, 21, 22, 13, 13, 16, 14, 15, 14, 11, 14, 15, 13, 16, 18,
                      20, 12, 15, 15, 9, 16, 13, 12, 10, 13, 7, 15, 12, 12, 14, 13, 12, 14, 11, 10, 17, 15, 13, 15, 19,
                      18, 19, 24, 25, 22, 25, 28, 26, 24, 31, 22, 17, 24, 26, 26, 19, 20, 16, 18, 17, 13, 14, 22, 26,
                      19, 30, 27, 22, 31, 23, 30, 24, 27, 32, 20, 28, 26, 23, 29, 25, 28, 32, 28, 33, 36, 29, 27, 23,
                      25, 25, 26, 24, 23, 28, 25, 28, 25, 22, 26, 27, 30, 28, 31, 26, 21, 26, 27, 24, 24, 24, 30, 21,
                      36, 33, 28, 32, 27, 26, 29, 28, 22, 27, 28, 29, 31, 28, 25, 27, 23, 24, 24, 23, 21, 20, 23, 22,
                      20]

# experiment_1_front_nums = [4, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_1_n_nds = [3, 5, 9, 5, 13, 8, 4, 5, 7, 10, 13, 13, 15, 3, 5, 8, 11, 15, 20, 20, 14, 12, 12, 16, 10, 12, 13, 15, 15, 11, 4, 16, 11, 14, 13, 16, 8, 8, 17, 15, 19, 18, 15, 10, 14, 11, 15, 10, 7, 6, 10, 16, 18, 17, 10, 18, 13, 14, 18, 16, 16, 15, 15, 17, 19, 13, 12, 21, 10, 15, 19, 13, 9, 11, 17, 12, 16, 12, 10, 10, 14, 6, 7, 8, 10, 8, 9, 8, 10, 14, 12, 14, 16, 16, 20, 18, 19, 19, 21, 21, 21, 21, 23, 21, 22, 25, 21, 20, 17, 18, 18, 20, 15, 14, 16, 18, 18, 16, 15, 14, 18, 19, 20, 20, 16, 17, 15, 11, 13, 19, 19, 16, 16, 16, 17, 20, 15, 17, 18, 20, 21, 23, 24, 19, 21, 20, 21, 23, 24, 21, 23, 18, 22, 22, 19, 21, 21, 22, 25, 23, 20, 23, 19, 18, 21, 24, 22, 24, 8, 8, 8, 8, 8, 8, 8, 9, 8, 11, 9, 8, 9, 8, 12, 14, 10, 11, 11, 7, 16, 17, 18, 20, 18, 18, 16, 19, 18, 21, 23, 26]
#
# experiment_2_front_nums = [4, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_2_n_nds = [3, 5, 7, 13, 7, 8, 13, 11, 8, 12, 13, 16, 13, 13, 10, 10, 6, 8, 11, 15, 16, 16, 13, 11, 13, 15, 15, 17, 17, 19, 19, 14, 20, 15, 12, 13, 11, 15, 13, 16, 12, 12, 15, 18, 14, 17, 11, 15, 15, 20, 19, 18, 17, 19, 17, 14, 21, 20, 30, 5, 10, 9, 13, 12, 16, 13, 13, 13, 13, 17, 16, 21, 18, 16, 13, 18, 12, 17, 16, 19, 14, 24, 15, 17, 27, 20, 28, 26, 23, 28, 7, 12, 10, 23, 23, 23, 24, 28, 30, 32, 27, 33, 29, 24, 24, 23, 26, 30, 26, 30, 29, 15, 11, 8, 12, 12, 9, 9, 11, 10, 10, 11, 12, 16, 13, 14, 11, 14, 18, 12, 10, 12, 12, 10, 11, 12, 11, 12, 8, 2, 2, 4, 8, 9, 9, 6, 7, 8, 7, 12, 15, 14, 18, 18, 16, 23, 23, 21, 25, 24, 24, 24, 15, 27, 25, 26, 23, 32, 26, 23, 25, 31, 27, 33, 37, 39, 35, 18, 25, 20, 22, 27, 23, 26, 20, 27, 28, 29, 31, 33, 35, 29, 34, 22, 24, 21, 30, 26, 27, 26]
#
# experiment_3_front_nums = [4, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_3_n_nds = [3, 5, 9, 10, 8, 9, 9, 11, 14, 16, 12, 5, 6, 8, 7, 10, 11, 11, 9, 10, 12, 10, 14, 16, 17, 16, 15, 11, 15, 12, 14, 9, 10, 5, 7, 4, 6, 7, 8, 10, 7, 14, 12, 18, 14, 17, 14, 10, 11, 3, 4, 4, 10, 8, 10, 9, 11, 8, 10, 12, 18, 15, 17, 20, 22, 19, 24, 21, 20, 19, 13, 15, 13, 20, 21, 21, 22, 25, 27, 30, 25, 28, 27, 33, 29, 24, 11, 15, 13, 17, 17, 20, 28, 14, 15, 20, 15, 18, 22, 19, 18, 22, 22, 28, 9, 12, 14, 12, 15, 20, 25, 1, 2, 2, 4, 4, 4, 5, 3, 5, 5, 5, 7, 5, 5, 9, 13, 12, 14, 16, 18, 15, 15, 16, 15, 17, 11, 15, 16, 16, 19, 18, 20, 17, 27, 30, 27, 23, 26, 22, 17, 26, 25, 27, 22, 25, 21, 22, 19, 17, 21, 20, 17, 20, 23, 15, 17, 16, 16, 14, 15, 16, 12, 11, 13, 15, 15, 11, 15, 15, 13, 14, 15, 14, 19, 21, 23, 15, 23, 23, 26, 32, 35, 29, 29, 32, 36, 24, 31, 38]
#
# experiment_4_front_nums =  [3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_4_n_nds = [5, 10, 12, 3, 5, 6, 13, 4, 7, 11, 15, 7, 4, 5, 10, 9, 8, 6, 2, 1, 2, 1, 4, 4, 2, 3, 4, 5, 11, 11, 11, 15, 15, 11, 9, 19, 9, 13, 8, 8, 10, 13, 9, 15, 15, 13, 11, 14, 20, 19, 16, 6, 2, 6, 8, 8, 6, 7, 1, 1, 1, 1, 3, 5, 7, 9, 11, 10, 12, 14, 17, 16, 11, 12, 15, 14, 17, 16, 15, 20, 24, 20, 29, 22, 26, 21, 17, 15, 18, 20, 14, 15, 15, 15, 15, 16, 17, 18, 17, 19, 17, 19, 13, 15, 13, 15, 18, 20, 23, 7, 13, 6, 11, 10, 12, 10, 11, 10, 13, 15, 16, 19, 18, 19, 14, 15, 15, 20, 6, 6, 6, 6, 6, 7, 9, 6, 9, 10, 13, 17, 21, 19, 17, 18, 20, 15, 15, 16, 16, 17, 20, 20, 17, 21, 21, 21, 19, 18, 17, 13, 17, 22, 16, 20, 24, 22, 23, 24, 23, 23, 27, 26, 26, 27, 26, 28, 22, 21, 27, 25, 25, 22, 23, 23, 22, 21, 25, 25, 14, 21, 11, 12, 11, 13, 11, 11, 13, 15, 13, 13]
#
# experiment_5_front_nums = [3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_5_n_nds = [6, 11, 9, 7, 5, 12, 6, 7, 7, 10, 14, 4, 5, 5, 11, 9, 7, 9, 22, 17, 17, 15, 15, 9, 8, 17, 17, 20, 20, 27, 11, 8, 10, 13, 14, 13, 11, 11, 12, 13, 18, 19, 27, 25, 14, 12, 14, 23, 25, 22, 30, 29, 30, 21, 28, 30, 26, 24, 17, 23, 18, 25, 22, 17, 22, 21, 23, 18, 14, 13, 14, 15, 15, 17, 20, 17, 22, 14, 11, 14, 12, 13, 13, 13, 13, 17, 16, 22, 10, 12, 12, 12, 10, 17, 17, 15, 12, 11, 13, 18, 21, 23, 23, 27, 22, 24, 20, 24, 27, 19, 27, 21, 33, 28, 28, 34, 22, 21, 18, 18, 18, 24, 21, 24, 27, 27, 31, 32, 31, 34, 18, 6, 5, 3, 4, 7, 5, 5, 8, 6, 8, 11, 9, 16, 8, 13, 14, 12, 11, 18, 12, 18, 17, 18, 23, 18, 21, 18, 19, 21, 19, 20, 21, 19, 18, 22, 18, 21, 23, 28, 30, 29, 26, 25, 18, 29, 33, 17, 14, 17, 18, 19, 19, 20, 19, 20, 26, 11, 11, 13, 18, 11, 11, 4, 4, 4, 6, 6, 5, 8]
#
# experiment_6_front_nums =  [3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_6_n_nds = [5, 9, 7, 12, 11, 14, 10, 8, 5, 4, 4, 7, 6, 4, 5, 7, 10, 13, 3, 5, 7, 12, 10, 6, 5, 5, 6, 7, 10, 15, 9, 18, 14, 16, 11, 11, 9, 13, 9, 13, 7, 8, 4, 10, 10, 12, 7, 15, 13, 12, 15, 18, 19, 14, 15, 16, 24, 17, 8, 8, 10, 11, 16, 17, 15, 16, 18, 19, 13, 18, 14, 20, 17, 18, 9, 5, 8, 8, 10, 12, 10, 15, 22, 20, 22, 23, 26, 20, 25, 28, 25, 16, 14, 16, 17, 19, 17, 16, 17, 22, 28, 24, 31, 30, 19, 21, 16, 18, 21, 21, 15, 17, 19, 23, 20, 23, 18, 27, 24, 28, 21, 26, 33, 33, 37, 33, 21, 20, 18, 19, 20, 17, 16, 19, 16, 19, 14, 20, 13, 12, 20, 29, 32, 32, 27, 27, 26, 23, 20, 25, 10, 18, 19, 19, 20, 22, 25, 28, 15, 12, 13, 14, 15, 15, 12, 15, 17, 19, 18, 16, 17, 17, 19, 19, 18, 31, 22, 30, 29, 26, 25, 25, 26, 25, 28, 33, 29, 31, 30, 14, 27, 28, 30, 37, 30, 29, 17, 16, 20, 24]

# experiment_1_front_nums = [4, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_1_n_nds = [3, 5, 8, 12, 15, 9, 1, 4, 4, 6, 6, 7, 10, 9, 14, 13, 8, 11, 7, 9, 12, 11, 9, 10, 5, 5, 4, 4, 6, 7, 8, 14, 7, 14, 5, 6, 6, 7, 7, 13, 12, 14, 15, 3, 5, 6, 8, 9, 9, 8, 7, 9, 8, 9, 11, 12, 16, 16, 12, 18, 16, 17, 19, 17, 14, 13, 18, 13, 16, 19, 18, 20, 22, 12, 25, 22, 14, 15, 17, 16, 16, 21, 15, 18, 21, 22, 33, 33, 25, 32, 23, 26, 23, 24, 20, 21, 15, 18, 23, 19, 23, 23, 29, 18, 20, 24, 23, 26, 18, 25, 24, 10, 12, 9, 8, 13, 14, 14, 14, 8, 18, 18, 16, 15, 20, 14, 15, 15, 17, 20, 20, 17, 18, 20, 18, 19, 20, 17, 24, 12, 12, 5, 10, 14, 11, 16, 22, 1, 2, 4, 5, 5, 6, 6, 5, 6, 9, 12, 9, 10, 15, 16, 13, 14, 12, 15, 8, 8, 9, 4, 6, 9, 12, 15, 20, 22, 22, 18, 21, 24, 19, 23, 26, 30, 25, 28, 34, 30, 25, 27, 25, 26, 26, 20, 24, 20, 22, 28, 23, 19]
#
# experiment_2_front_nums = [4, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_2_n_nds = [4, 5, 10, 10, 1, 1, 5, 3, 2, 7, 6, 10, 15, 7, 9, 10, 9, 12, 12, 9, 11, 14, 15, 7, 13, 12, 10, 12, 11, 14, 10, 17, 15, 20, 24, 23, 15, 11, 15, 11, 11, 12, 25, 17, 14, 13, 12, 18, 20, 17, 16, 23, 18, 24, 21, 20, 22, 22, 17, 15, 19, 17, 19, 4, 4, 8, 6, 7, 8, 12, 11, 10, 10, 11, 14, 15, 14, 9, 10, 10, 14, 12, 16, 13, 10, 10, 15, 17, 17, 18, 17, 15, 16, 14, 5, 7, 6, 5, 12, 11, 10, 12, 12, 10, 10, 12, 9, 10, 14, 6, 11, 11, 11, 13, 14, 15, 12, 13, 16, 15, 21, 18, 19, 21, 19, 17, 16, 16, 15, 17, 17, 22, 19, 20, 24, 21, 15, 23, 25, 24, 19, 16, 18, 22, 16, 18, 20, 22, 17, 18, 23, 17, 18, 20, 23, 21, 22, 21, 22, 9, 9, 10, 11, 11, 13, 9, 9, 9, 12, 15, 11, 12, 12, 14, 15, 17, 14, 16, 17, 18, 9, 12, 8, 10, 11, 15, 17, 19, 14, 13, 14, 20, 8, 9, 8, 8, 8, 7, 9, 11]
#
# experiment_3_front_nums = [4, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_3_n_nds = [3, 4, 5, 9, 8, 6, 6, 11, 15, 11, 5, 9, 9, 13, 15, 6, 9, 7, 7, 9, 13, 8, 12, 8, 8, 5, 7, 8, 11, 11, 8, 9, 6, 7, 8, 5, 8, 4, 5, 5, 3, 5, 6, 9, 8, 9, 9, 11, 10, 12, 11, 10, 14, 14, 17, 10, 12, 15, 14, 15, 14, 11, 17, 19, 17, 16, 22, 20, 15, 12, 7, 9, 19, 18, 16, 16, 20, 16, 22, 17, 11, 16, 16, 13, 18, 13, 16, 17, 15, 19, 18, 13, 9, 11, 12, 11, 12, 14, 17, 18, 13, 14, 10, 12, 14, 15, 16, 19, 20, 18, 20, 21, 21, 19, 20, 22, 15, 24, 21, 21, 21, 19, 19, 15, 15, 20, 18, 20, 20, 17, 14, 18, 13, 16, 16, 14, 13, 15, 11, 8, 8, 11, 11, 13, 15, 11, 13, 13, 14, 14, 15, 19, 23, 25, 19, 19, 22, 11, 15, 14, 14, 13, 18, 17, 20, 22, 22, 24, 17, 15, 16, 17, 18, 18, 22, 16, 21, 21, 21, 20, 24, 21, 23, 20, 24, 23, 26, 21, 28, 23, 16, 16, 17, 16, 16, 18, 21, 20, 23, 22]
#
# experiment_4_front_nums = [3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_4_n_nds = [8, 11, 11, 6, 10, 19, 4, 7, 6, 7, 7, 9, 7, 1, 1, 1, 1, 2, 2, 3, 3, 5, 7, 8, 10, 10, 5, 6, 6, 6, 8, 8, 6, 8, 9, 9, 11, 10, 16, 20, 12, 13, 16, 9, 2, 4, 6, 8, 5, 6, 5, 8, 9, 11, 11, 10, 10, 11, 8, 8, 9, 9, 10, 12, 11, 13, 15, 20, 17, 13, 16, 15, 15, 12, 17, 13, 11, 10, 15, 15, 21, 11, 12, 14, 17, 22, 16, 16, 19, 20, 13, 10, 9, 10, 12, 15, 16, 16, 16, 17, 19, 17, 22, 21, 16, 14, 16, 17, 17, 18, 16, 9, 10, 12, 11, 9, 12, 13, 14, 12, 17, 18, 17, 18, 23, 22, 24, 25, 23, 28, 28, 24, 28, 30, 29, 26, 31, 32, 24, 26, 28, 19, 16, 18, 18, 18, 20, 21, 21, 16, 21, 19, 16, 17, 16, 14, 17, 20, 21, 23, 12, 20, 21, 19, 4, 7, 6, 7, 8, 5, 8, 6, 4, 6, 10, 8, 11, 10, 10, 7, 8, 8, 10, 12, 11, 8, 10, 10, 12, 14, 12, 15, 14, 16, 11, 7, 9, 13, 14, 11]
#
# experiment_5_front_nums = [3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_5_n_nds = [6, 11, 9, 7, 5, 12, 6, 7, 7, 10, 14, 4, 5, 5, 11, 9, 7, 9, 22, 17, 17, 15, 15, 9, 8, 17, 17, 20, 20, 27, 11, 8, 10, 13, 14, 13, 11, 11, 12, 13, 18, 19, 27, 25, 14, 12, 14, 23, 25, 22, 30, 29, 30, 21, 28, 30, 26, 24, 17, 23, 18, 25, 22, 17, 22, 21, 23, 18, 14, 13, 14, 15, 15, 17, 20, 17, 22, 14, 11, 14, 12, 13, 13, 13, 13, 17, 16, 22, 10, 12, 12, 12, 10, 17, 17, 15, 12, 11, 13, 18, 21, 23, 23, 27, 22, 24, 20, 24, 27, 19, 27, 21, 33, 28, 28, 34, 22, 21, 18, 18, 18, 24, 21, 24, 27, 27, 31, 32, 31, 34, 18, 6, 5, 3, 4, 7, 5, 5, 8, 6, 8, 11, 9, 16, 8, 13, 14, 12, 11, 18, 12, 18, 17, 18, 23, 18, 21, 18, 19, 21, 19, 20, 21, 19, 18, 22, 18, 21, 23, 28, 30, 29, 26, 25, 18, 29, 33, 17, 14, 17, 18, 19, 19, 20, 19, 20, 26, 11, 11, 13, 18, 11, 11, 4, 4, 4, 6, 6, 5, 8]
#
# experiment_6_front_nums = [3, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# experiment_6_n_nds = [5, 11, 7, 5, 6, 3, 8, 13, 15, 19, 7, 17, 11, 12, 12, 9, 9, 9, 9, 5, 7, 3, 3, 4, 4, 5, 10, 7, 6, 6, 4, 8, 10, 8, 8, 10, 11, 13, 15, 13, 13, 7, 3, 5, 8, 12, 12, 14, 18, 6, 7, 9, 8, 13, 10, 14, 16, 19, 16, 17, 15, 8, 10, 13, 13, 11, 9, 10, 11, 14, 18, 20, 27, 25, 28, 29, 27, 28, 29, 28, 24, 9, 17, 23, 19, 27, 22, 22, 25, 31, 16, 17, 22, 13, 20, 21, 18, 19, 22, 17, 16, 19, 16, 18, 18, 15, 20, 16, 14, 23, 27, 27, 32, 37, 36, 37, 25, 26, 29, 29, 28, 27, 22, 24, 25, 22, 18, 18, 19, 15, 19, 23, 20, 21, 19, 7, 9, 6, 6, 6, 8, 20, 20, 20, 20, 10, 18, 15, 14, 15, 16, 17, 16, 18, 17, 18, 10, 20, 17, 21, 14, 16, 21, 23, 23, 28, 24, 26, 23, 24, 24, 25, 10, 12, 26, 22, 5, 11, 10, 8, 4, 6, 6, 8, 9, 7, 14, 16, 14, 17, 17, 18, 16, 17, 22, 18, 18, 9, 14, 21]

def plot_multiple_lines(x, y_arrays):
    plt.figure(figsize=(20, 8))

    # Updated line styles list to include 6 styles
    # line_styles = ['-', '--', '-.', ':', 'dashed', 'dashed']
    # num_styles = len(line_styles)

    # for i, y in enumerate(y_arrays):
    #     style = line_styles[i % num_styles]  # Cycle through the line styles
    #     plt.plot(x, y, linestyle=style, label=f'Line {i+1}')

    marker_styles = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h']
    line_colors = ['r', 'm', 'b', 'c', 'y', 'g', 'k', 'orange', 'purple', 'brown']
    # line_colors = ['r', 'r', 'r', 'orange', 'orange', 'orange', 'orange']
    num_markers = len(marker_styles)
    num_lines = len(y_arrays)
    # for i, y in enumerate(y_arrays):
    #     marker = marker_styles[i % num_markers]  # Cycle through the marker styles
    #     plt.plot(x, y, linestyle='-', marker=marker, label=f'Line {i+1}')

    # for i, y in enumerate(y_arrays):
    #     # Plot the line
    #     plt.plot(x, y, linestyle='-', label=f'Line {i+1}')
    #     # Add a single marker at the midpoint of the line
    #     midpoint = len(x) // 2
    #     # if i % 2 == 0:
    #     #     midpoint = midpoint // 2
    #     plt.plot(x[midpoint], y[midpoint], marker=marker_styles[i % num_markers], markersize=10, label=f'Line {i+1}')

    for i, y in enumerate(y_arrays):
        line_name = f'Line {i+1}'
        if i == 0:
            line_name = 'Cardinality = 249'
        elif i == 1:
            line_name = 'Cardinality = 249 / 2'
        elif i == 2:
            line_name = 'Cardinality = 249 / 4'
        elif i == 3:
            line_name = 'Cardinality = 100'
        elif i == 4:
            line_name = 'Cardinality = 100 / 2'
        elif i == 5:
            line_name = 'Cardinality = 100 / 4'
        color = line_colors[i % len(line_colors)]  # Cycle through the line colors
        # Plot the line
        plt.plot(x, y, linestyle='-', label='', color=color)
        # Add a single marker at different positions to avoid overlap
        marker_position = len(x) // (num_lines + 1) * (i + 1)
        plt.plot(x[marker_position], y[marker_position], marker=marker_styles[i % num_markers], markersize=10, label=line_name, color=color)


    # Add labels and title
    plt.xlabel('Generation', fontsize=16)
    plt.ylabel('Non-dominated solution count', fontsize=16)
    plt.title('The relationship between non-dominated solution count and cardinality constraints', fontsize=16)
    plt.legend(fontsize=14)

    plt.tick_params(axis='y', labelsize=14)
    plt.tick_params(axis='x', labelsize=14)

    # Show the plot
    plt.show()


# Example usage
x = list(range(1, 201))  # Array from 1 to 200
# y1 = experiment_1_front_nums
# y2 = experiment_2_front_nums
# y3 = experiment_3_front_nums
# y4 = experiment_4_front_nums
# y5 = experiment_5_front_nums
# y6 = experiment_6_front_nums

y1 = experiment_1_n_nds
y2 = experiment_2_n_nds
y3 = experiment_3_n_nds
y4 = experiment_4_n_nds
y5 = experiment_5_n_nds
y6 = experiment_6_n_nds

# List of y arrays
y_arrays = [y1, y2, y3, y4, y5, y6]

plot_multiple_lines(x, y_arrays)
