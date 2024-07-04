import math

INITIAL_CASH = 100000  # 1 BLN VND # NOTE if change plz update the same variable at nsga3.py as well, because they are two seperate projects
DURATION = 4  # 6 MONTHS # NOTE if change plz update the same variable at nsga3.py as well, because they are two seperate projects
WAVELET_LEVEL = 1  # 12, 6, 4 months => 3, 2, 1 todo change me if change DURATION


BANK_INTEREST_RATE = 0.0045  # NOTE if change plz update the same variable at nsga3.py as well, because they are two seperate projects

INVESTMENT_INTEREST_EXPECTED = 0.3
TRANS_FEE = 0.0015

BANK_INTEREST_RATE_AFTER_N_INVESTMENT_PERIOD = math.pow(1+BANK_INTEREST_RATE, DURATION)-1
BENCHMARK_FINAL_RETURN = (BANK_INTEREST_RATE_AFTER_N_INVESTMENT_PERIOD + 1) * INITIAL_CASH

MAX_STOCKS = 100  # CARDINALITY CONSTRAINT
TERMINATION_GEN_NUM = 200
TAIL_PROBABILITY_EPSILON = 0.1  # can change to 10%, 2.5%, and 1%

LOT_SIZE = 100

REBUILD_Y_SCALING_FACTOR = 1000

POPULATION_SIZE = 339
REFERENCES_POINTS_NUM = 339
STOCK_DATA_2023_INPUT_29_STOCKS = [
    {
        "symbol": "BCC",
        "companyName": "CTCP Xi măng Bỉm Sơn",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 11.6,
                "matchedTradingVolume": 16898285
            },
            {
                "month": 2,
                "value": 12.7,
                "matchedTradingVolume": 26045742
            },
            {
                "month": 3,
                "value": 12.4,
                "matchedTradingVolume": 20300759
            },
            {
                "month": 4,
                "value": 12.4,
                "matchedTradingVolume": 13811487
            },
            {
                "month": 5,
                "value": 13.3,
                "matchedTradingVolume": 20730116
            },
            {
                "month": 6,
                "value": 14.5,
                "matchedTradingVolume": 24793471
            },
            {
                "month": 7,
                "value": 14.6,
                "matchedTradingVolume": 22653644
            },
            {
                "month": 8,
                "value": 14.6,
                "matchedTradingVolume": 21295205
            },
            {
                "month": 9,
                "value": 13,
                "matchedTradingVolume": 9862493
            },
            {
                "month": 10,
                "value": 12.2,
                "matchedTradingVolume": 6465571
            },
            {
                "month": 11,
                "value": 9.8,
                "matchedTradingVolume": 5608050
            },
            {
                "month": 12,
                "value": 9.6,
                "matchedTradingVolume": 3821733
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 8,
                "value": 500
            }
        ]
    },
    {
        "symbol": "BVS",
        "companyName": "CTCP Chứng khoán Bảo Việt",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 21,
                "matchedTradingVolume": 1438111
            },
            {
                "month": 2,
                "value": 19,
                "matchedTradingVolume": 1854612
            },
            {
                "month": 3,
                "value": 19.1,
                "matchedTradingVolume": 3134602
            },
            {
                "month": 4,
                "value": 20.2,
                "matchedTradingVolume": 3958340
            },
            {
                "month": 5,
                "value": 23.8,
                "matchedTradingVolume": 9386680
            },
            {
                "month": 6,
                "value": 25.3,
                "matchedTradingVolume": 14453718
            },
            {
                "month": 7,
                "value": 27,
                "matchedTradingVolume": 13688213
            },
            {
                "month": 8,
                "value": 28.8,
                "matchedTradingVolume": 13880792
            },
            {
                "month": 9,
                "value": 30.7,
                "matchedTradingVolume": 9906439
            },
            {
                "month": 10,
                "value": 26.9,
                "matchedTradingVolume": 6689071
            },
            {
                "month": 11,
                "value": 26,
                "matchedTradingVolume": 3668846
            },
            {
                "month": 12,
                "value": 26.1,
                "matchedTradingVolume": 3959357
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 10,
                "value": 1000
            }
        ]
    },
    {
        "symbol": "CAP",
        "companyName": "CTCP Lâm Nông sản Thực phẩm Yên Bái",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 73.2,
                "matchedTradingVolume": 113106
            },
            {
                "month": 2,
                "value": 76.3,
                "matchedTradingVolume": 135358
            },
            {
                "month": 3,
                "value": 83.9,
                "matchedTradingVolume": 136556
            },
            {
                "month": 4,
                "value": 91.5,
                "matchedTradingVolume": 342827
            },
            {
                "month": 5,
                "value": 91.7,
                "matchedTradingVolume": 400862
            },
            {
                "month": 6,
                "value": 70.3,
                "matchedTradingVolume": 319155
            },
            {
                "month": 7,
                "value": 76.8,
                "matchedTradingVolume": 848052
            },
            {
                "month": 8,
                "value": 74.4,
                "matchedTradingVolume": 808393
            },
            {
                "month": 9,
                "value": 79,
                "matchedTradingVolume": 720323
            },
            {
                "month": 10,
                "value": 84.3,
                "matchedTradingVolume": 897248
            },
            {
                "month": 11,
                "value": 76.2,
                "matchedTradingVolume": 420061
            },
            {
                "month": 12,
                "value": 78.4,
                "matchedTradingVolume": 593973
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "CEO",
        "companyName": "CTCP Tập đoàn C.E.O",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 24.6,
                "matchedTradingVolume": 127064933
            },
            {
                "month": 2,
                "value": 23.4,
                "matchedTradingVolume": 175287235
            },
            {
                "month": 3,
                "value": 22.2,
                "matchedTradingVolume": 136584726
            },
            {
                "month": 4,
                "value": 25.5,
                "matchedTradingVolume": 186700486
            },
            {
                "month": 5,
                "value": 27.2,
                "matchedTradingVolume": 160517931
            },
            {
                "month": 6,
                "value": 27.6,
                "matchedTradingVolume": 165627114
            },
            {
                "month": 7,
                "value": 23.9,
                "matchedTradingVolume": 202780930
            },
            {
                "month": 8,
                "value": 26.2,
                "matchedTradingVolume": 329295960
            },
            {
                "month": 9,
                "value": 28.4,
                "matchedTradingVolume": 179469034
            },
            {
                "month": 10,
                "value": 21.6,
                "matchedTradingVolume": 208279320
            },
            {
                "month": 11,
                "value": 24.1,
                "matchedTradingVolume": 401348366
            },
            {
                "month": 12,
                "value": 23.9,
                "matchedTradingVolume": 256520459
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "DTD",
        "companyName": "CTCP Đầu tư Phát triển Thành Đạt",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 14.4,
                "matchedTradingVolume": 5950842
            },
            {
                "month": 2,
                "value": 13.7,
                "matchedTradingVolume": 6378838
            },
            {
                "month": 3,
                "value": 16.6,
                "matchedTradingVolume": 7311940
            },
            {
                "month": 4,
                "value": 18.1,
                "matchedTradingVolume": 10294297
            },
            {
                "month": 5,
                "value": 31.9,
                "matchedTradingVolume": 22655048
            },
            {
                "month": 6,
                "value": 32.5,
                "matchedTradingVolume": 18129994
            },
            {
                "month": 7,
                "value": 36.7,
                "matchedTradingVolume": 15735536
            },
            {
                "month": 8,
                "value": 32.5,
                "matchedTradingVolume": 16086212
            },
            {
                "month": 9,
                "value": 30.9,
                "matchedTradingVolume": 11056539
            },
            {
                "month": 10,
                "value": 30.5,
                "matchedTradingVolume": 18741944
            },
            {
                "month": 11,
                "value": 24,
                "matchedTradingVolume": 18315410
            },
            {
                "month": 12,
                "value": 26.3,
                "matchedTradingVolume": 24949081
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "DXP",
        "companyName": "CTCP Cảng Đoạn Xá",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 10.4,
                "matchedTradingVolume": 912739
            },
            {
                "month": 2,
                "value": 10.3,
                "matchedTradingVolume": 917376
            },
            {
                "month": 3,
                "value": 9.8,
                "matchedTradingVolume": 787279
            },
            {
                "month": 4,
                "value": 9.9,
                "matchedTradingVolume": 885375
            },
            {
                "month": 5,
                "value": 12.8,
                "matchedTradingVolume": 1782047
            },
            {
                "month": 6,
                "value": 13.5,
                "matchedTradingVolume": 3439863
            },
            {
                "month": 7,
                "value": 14,
                "matchedTradingVolume": 1994362
            },
            {
                "month": 8,
                "value": 13.8,
                "matchedTradingVolume": 2432178
            },
            {
                "month": 9,
                "value": 14.1,
                "matchedTradingVolume": 4273324
            },
            {
                "month": 10,
                "value": 14.8,
                "matchedTradingVolume": 9033438
            },
            {
                "month": 11,
                "value": 13.3,
                "matchedTradingVolume": 10391949
            },
            {
                "month": 12,
                "value": 13.4,
                "matchedTradingVolume": 6974255
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "HLD",
        "companyName": "null",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 29.8,
                "matchedTradingVolume": 231503
            },
            {
                "month": 2,
                "value": 28.2,
                "matchedTradingVolume": 226901
            },
            {
                "month": 3,
                "value": 27.4,
                "matchedTradingVolume": 140330
            },
            {
                "month": 4,
                "value": 35.6,
                "matchedTradingVolume": 496224
            },
            {
                "month": 5,
                "value": 37.2,
                "matchedTradingVolume": 307238
            },
            {
                "month": 6,
                "value": 36.6,
                "matchedTradingVolume": 339320
            },
            {
                "month": 7,
                "value": 33,
                "matchedTradingVolume": 620471
            },
            {
                "month": 8,
                "value": 32.6,
                "matchedTradingVolume": 589525
            },
            {
                "month": 9,
                "value": 31.5,
                "matchedTradingVolume": 674240
            },
            {
                "month": 10,
                "value": 27.6,
                "matchedTradingVolume": 250531
            },
            {
                "month": 11,
                "value": 26.4,
                "matchedTradingVolume": 395171
            },
            {
                "month": 12,
                "value": 26.5,
                "matchedTradingVolume": 307473
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "HUT",
        "companyName": "null",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 16.8,
                "matchedTradingVolume": 26232682
            },
            {
                "month": 2,
                "value": 15.4,
                "matchedTradingVolume": 31806604
            },
            {
                "month": 3,
                "value": 16.1,
                "matchedTradingVolume": 40121809
            },
            {
                "month": 4,
                "value": 17.2,
                "matchedTradingVolume": 39834208
            },
            {
                "month": 5,
                "value": 18.5,
                "matchedTradingVolume": 50768478
            },
            {
                "month": 6,
                "value": 20.1,
                "matchedTradingVolume": 77486457
            },
            {
                "month": 7,
                "value": 21.1,
                "matchedTradingVolume": 69055870
            },
            {
                "month": 8,
                "value": 27.4,
                "matchedTradingVolume": 121918856
            },
            {
                "month": 9,
                "value": 28.5,
                "matchedTradingVolume": 124166119
            },
            {
                "month": 10,
                "value": 24.2,
                "matchedTradingVolume": 105483677
            },
            {
                "month": 11,
                "value": 21.1,
                "matchedTradingVolume": 126796970
            },
            {
                "month": 12,
                "value": 21.3,
                "matchedTradingVolume": 120443764
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "IDC",
        "companyName": "Tổng Công ty IDICO – CTCP",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 40.4,
                "matchedTradingVolume": 42236657
            },
            {
                "month": 2,
                "value": 42.5,
                "matchedTradingVolume": 71829678
            },
            {
                "month": 3,
                "value": 41,
                "matchedTradingVolume": 55623409
            },
            {
                "month": 4,
                "value": 41.9,
                "matchedTradingVolume": 41157756
            },
            {
                "month": 5,
                "value": 41.9,
                "matchedTradingVolume": 51671490
            },
            {
                "month": 6,
                "value": 44.2,
                "matchedTradingVolume": 73655552
            },
            {
                "month": 7,
                "value": 45.7,
                "matchedTradingVolume": 62733165
            },
            {
                "month": 8,
                "value": 49.3,
                "matchedTradingVolume": 83958141
            },
            {
                "month": 9,
                "value": 50.4,
                "matchedTradingVolume": 61038327
            },
            {
                "month": 10,
                "value": 52.5,
                "matchedTradingVolume": 93609479
            },
            {
                "month": 11,
                "value": 50.5,
                "matchedTradingVolume": 57923673
            },
            {
                "month": 12,
                "value": 52.2,
                "matchedTradingVolume": 53508845
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 4,
                "value": 2000
            },
            {
                "month": 9,
                "value": 2000
            }
        ]
    },
    {
        "symbol": "L14",
        "companyName": "null",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 58.9,
                "matchedTradingVolume": 7741503
            },
            {
                "month": 2,
                "value": 53.5,
                "matchedTradingVolume": 7944098
            },
            {
                "month": 3,
                "value": 45.9,
                "matchedTradingVolume": 5681449
            },
            {
                "month": 4,
                "value": 54.2,
                "matchedTradingVolume": 10662182
            },
            {
                "month": 5,
                "value": 52.2,
                "matchedTradingVolume": 12789680
            },
            {
                "month": 6,
                "value": 48,
                "matchedTradingVolume": 13094389
            },
            {
                "month": 7,
                "value": 48,
                "matchedTradingVolume": 10732735
            },
            {
                "month": 8,
                "value": 62,
                "matchedTradingVolume": 22437095
            },
            {
                "month": 9,
                "value": 59.9,
                "matchedTradingVolume": 11478379
            },
            {
                "month": 10,
                "value": 44.5,
                "matchedTradingVolume": 6285716
            },
            {
                "month": 11,
                "value": 46.6,
                "matchedTradingVolume": 10706426
            },
            {
                "month": 12,
                "value": 48.8,
                "matchedTradingVolume": 7059836
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "L18",
        "companyName": "CTCP Đầu tư và Xây dựng Số 18",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 22.5,
                "matchedTradingVolume": 762349
            },
            {
                "month": 2,
                "value": 22.8,
                "matchedTradingVolume": 948665
            },
            {
                "month": 3,
                "value": 25.4,
                "matchedTradingVolume": 880699
            },
            {
                "month": 4,
                "value": 29.5,
                "matchedTradingVolume": 972819
            },
            {
                "month": 5,
                "value": 39.5,
                "matchedTradingVolume": 1285782
            },
            {
                "month": 6,
                "value": 37,
                "matchedTradingVolume": 890512
            },
            {
                "month": 7,
                "value": 39,
                "matchedTradingVolume": 1114914
            },
            {
                "month": 8,
                "value": 42,
                "matchedTradingVolume": 1684345
            },
            {
                "month": 9,
                "value": 41.6,
                "matchedTradingVolume": 1101101
            },
            {
                "month": 10,
                "value": 35,
                "matchedTradingVolume": 536762
            },
            {
                "month": 11,
                "value": 36,
                "matchedTradingVolume": 676349
            },
            {
                "month": 12,
                "value": 42,
                "matchedTradingVolume": 1204132
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 1,
                "value": 800
            },
            {
                "month": 3,
                "value": 700
            }
        ]
    },
    {
        "symbol": "LAS",
        "companyName": "CTCP Supe Phốt phát và Hóa chất Lâm Thao",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 9,
                "matchedTradingVolume": 3578318
            },
            {
                "month": 2,
                "value": 8.8,
                "matchedTradingVolume": 4052633
            },
            {
                "month": 3,
                "value": 8.6,
                "matchedTradingVolume": 3805041
            },
            {
                "month": 4,
                "value": 9.3,
                "matchedTradingVolume": 8152270
            },
            {
                "month": 5,
                "value": 10.6,
                "matchedTradingVolume": 15071426
            },
            {
                "month": 6,
                "value": 11.6,
                "matchedTradingVolume": 16968799
            },
            {
                "month": 7,
                "value": 13.4,
                "matchedTradingVolume": 13925595
            },
            {
                "month": 8,
                "value": 13.5,
                "matchedTradingVolume": 10302924
            },
            {
                "month": 9,
                "value": 14.7,
                "matchedTradingVolume": 12641782
            },
            {
                "month": 10,
                "value": 14.2,
                "matchedTradingVolume": 11448746
            },
            {
                "month": 11,
                "value": 14,
                "matchedTradingVolume": 13527785
            },
            {
                "month": 12,
                "value": 15,
                "matchedTradingVolume": 17700348
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 8,
                "value": 600
            }
        ]
    },
    {
        "symbol": "LHC",
        "companyName": "CTCP Đầu tư và Xây dựng Thủy lợi Lâm Đồng",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 52,
                "matchedTradingVolume": 360814
            },
            {
                "month": 2,
                "value": 51,
                "matchedTradingVolume": 158300
            },
            {
                "month": 3,
                "value": 51.8,
                "matchedTradingVolume": 534500
            },
            {
                "month": 4,
                "value": 52,
                "matchedTradingVolume": 203612
            },
            {
                "month": 5,
                "value": 49.8,
                "matchedTradingVolume": 130386
            },
            {
                "month": 6,
                "value": 50.2,
                "matchedTradingVolume": 388275
            },
            {
                "month": 7,
                "value": 57,
                "matchedTradingVolume": 891568
            },
            {
                "month": 8,
                "value": 57.5,
                "matchedTradingVolume": 283634
            },
            {
                "month": 9,
                "value": 60.7,
                "matchedTradingVolume": 272250
            },
            {
                "month": 10,
                "value": 57.9,
                "matchedTradingVolume": 95227
            },
            {
                "month": 11,
                "value": 53.9,
                "matchedTradingVolume": 397727
            },
            {
                "month": 12,
                "value": 52.9,
                "matchedTradingVolume": 177928
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 3,
                "value": 500
            },
            {
                "month": 8,
                "value": 1500
            }
        ]
    },
    {
        "symbol": "MBS",
        "companyName": "CTCP Chứng khoán MB",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 15.3,
                "matchedTradingVolume": 38321764
            },
            {
                "month": 2,
                "value": 14.8,
                "matchedTradingVolume": 38730351
            },
            {
                "month": 3,
                "value": 15.8,
                "matchedTradingVolume": 55555374
            },
            {
                "month": 4,
                "value": 17.6,
                "matchedTradingVolume": 81238888
            },
            {
                "month": 5,
                "value": 18.5,
                "matchedTradingVolume": 66965434
            },
            {
                "month": 6,
                "value": 19.5,
                "matchedTradingVolume": 74072721
            },
            {
                "month": 7,
                "value": 21.2,
                "matchedTradingVolume": 74782537
            },
            {
                "month": 8,
                "value": 21.2,
                "matchedTradingVolume": 79872284
            },
            {
                "month": 9,
                "value": 24.5,
                "matchedTradingVolume": 86962514
            },
            {
                "month": 10,
                "value": 23.5,
                "matchedTradingVolume": 109345483
            },
            {
                "month": 11,
                "value": 22,
                "matchedTradingVolume": 107702558
            },
            {
                "month": 12,
                "value": 23.4,
                "matchedTradingVolume": 83679495
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "NBC",
        "companyName": "CTCP Than Núi Béo - Vinacomin",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 11.8,
                "matchedTradingVolume": 3613717
            },
            {
                "month": 2,
                "value": 12.1,
                "matchedTradingVolume": 7089386
            },
            {
                "month": 3,
                "value": 11.5,
                "matchedTradingVolume": 3494563
            },
            {
                "month": 4,
                "value": 12.7,
                "matchedTradingVolume": 6028485
            },
            {
                "month": 5,
                "value": 12.7,
                "matchedTradingVolume": 6823417
            },
            {
                "month": 6,
                "value": 13.3,
                "matchedTradingVolume": 5858620
            },
            {
                "month": 7,
                "value": 13.6,
                "matchedTradingVolume": 7106972
            },
            {
                "month": 8,
                "value": 13.4,
                "matchedTradingVolume": 6584419
            },
            {
                "month": 9,
                "value": 12.6,
                "matchedTradingVolume": 4992643
            },
            {
                "month": 10,
                "value": 11.7,
                "matchedTradingVolume": 2871754
            },
            {
                "month": 11,
                "value": 11.2,
                "matchedTradingVolume": 2702813
            },
            {
                "month": 12,
                "value": 12.2,
                "matchedTradingVolume": 3338675
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 6,
                "value": 300
            }
        ]
    },
    {
        "symbol": "PLC",
        "companyName": "null",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 28,
                "matchedTradingVolume": 8019236
            },
            {
                "month": 2,
                "value": 32.8,
                "matchedTradingVolume": 16214208
            },
            {
                "month": 3,
                "value": 35,
                "matchedTradingVolume": 17856342
            },
            {
                "month": 4,
                "value": 34.4,
                "matchedTradingVolume": 13343638
            },
            {
                "month": 5,
                "value": 37.6,
                "matchedTradingVolume": 11009234
            },
            {
                "month": 6,
                "value": 39,
                "matchedTradingVolume": 9749548
            },
            {
                "month": 7,
                "value": 40.4,
                "matchedTradingVolume": 8317441
            },
            {
                "month": 8,
                "value": 39.5,
                "matchedTradingVolume": 6508016
            },
            {
                "month": 9,
                "value": 37.7,
                "matchedTradingVolume": 4813765
            },
            {
                "month": 10,
                "value": 34.7,
                "matchedTradingVolume": 3137853
            },
            {
                "month": 11,
                "value": 30.7,
                "matchedTradingVolume": 3341603
            },
            {
                "month": 12,
                "value": 33.2,
                "matchedTradingVolume": 2711591
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "PSI",
        "companyName": "null",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 6.1,
                "matchedTradingVolume": 563172
            },
            {
                "month": 2,
                "value": 6,
                "matchedTradingVolume": 563212
            },
            {
                "month": 3,
                "value": 5.6,
                "matchedTradingVolume": 698563
            },
            {
                "month": 4,
                "value": 7,
                "matchedTradingVolume": 2494209
            },
            {
                "month": 5,
                "value": 7.9,
                "matchedTradingVolume": 2745850
            },
            {
                "month": 6,
                "value": 9,
                "matchedTradingVolume": 3780471
            },
            {
                "month": 7,
                "value": 9,
                "matchedTradingVolume": 2673914
            },
            {
                "month": 8,
                "value": 9.8,
                "matchedTradingVolume": 5783383
            },
            {
                "month": 9,
                "value": 12.2,
                "matchedTradingVolume": 11061288
            },
            {
                "month": 10,
                "value": 9.9,
                "matchedTradingVolume": 4885496
            },
            {
                "month": 11,
                "value": 9.2,
                "matchedTradingVolume": 4076293
            },
            {
                "month": 12,
                "value": 9.5,
                "matchedTradingVolume": 2586015
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "PVC",
        "companyName": "Tổng Công ty Hóa chất và Dịch vụ Dầu khí - CTCP",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 15.6,
                "matchedTradingVolume": 35163557
            },
            {
                "month": 2,
                "value": 15.6,
                "matchedTradingVolume": 38260500
            },
            {
                "month": 3,
                "value": 16.5,
                "matchedTradingVolume": 39275747
            },
            {
                "month": 4,
                "value": 16.4,
                "matchedTradingVolume": 38379409
            },
            {
                "month": 5,
                "value": 18.5,
                "matchedTradingVolume": 47079449
            },
            {
                "month": 6,
                "value": 18.6,
                "matchedTradingVolume": 39167582
            },
            {
                "month": 7,
                "value": 19.4,
                "matchedTradingVolume": 31585006
            },
            {
                "month": 8,
                "value": 19.8,
                "matchedTradingVolume": 32294619
            },
            {
                "month": 9,
                "value": 20,
                "matchedTradingVolume": 30883423
            },
            {
                "month": 10,
                "value": 18.9,
                "matchedTradingVolume": 30460937
            },
            {
                "month": 11,
                "value": 15.2,
                "matchedTradingVolume": 36621345
            },
            {
                "month": 12,
                "value": 16.1,
                "matchedTradingVolume": 27428238
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 11,
                "value": 180
            }
        ]
    },
    {
        "symbol": "PVG",
        "companyName": "CTCP Kinh doanh LPG Việt Nam",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 8,
                "matchedTradingVolume": 1164214
            },
            {
                "month": 2,
                "value": 8.5,
                "matchedTradingVolume": 1859515
            },
            {
                "month": 3,
                "value": 8.1,
                "matchedTradingVolume": 1124560
            },
            {
                "month": 4,
                "value": 8.1,
                "matchedTradingVolume": 1783152
            },
            {
                "month": 5,
                "value": 9.2,
                "matchedTradingVolume": 3510578
            },
            {
                "month": 6,
                "value": 10.7,
                "matchedTradingVolume": 6292684
            },
            {
                "month": 7,
                "value": 10.5,
                "matchedTradingVolume": 4906952
            },
            {
                "month": 8,
                "value": 10.9,
                "matchedTradingVolume": 6233546
            },
            {
                "month": 9,
                "value": 10.4,
                "matchedTradingVolume": 3017782
            },
            {
                "month": 10,
                "value": 10,
                "matchedTradingVolume": 1405768
            },
            {
                "month": 11,
                "value": 9.3,
                "matchedTradingVolume": 662121
            },
            {
                "month": 12,
                "value": 9.2,
                "matchedTradingVolume": 656764
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 6,
                "value": 300
            }
        ]
    },
    {
        "symbol": "PVS",
        "companyName": "Tổng Công ty cổ phần Dịch vụ Kỹ thuật Dầu khí Việt Nam",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 25.6,
                "matchedTradingVolume": 86042635
            },
            {
                "month": 2,
                "value": 26.8,
                "matchedTradingVolume": 131385208
            },
            {
                "month": 3,
                "value": 27.5,
                "matchedTradingVolume": 116136499
            },
            {
                "month": 4,
                "value": 26.4,
                "matchedTradingVolume": 80120016
            },
            {
                "month": 5,
                "value": 31,
                "matchedTradingVolume": 140267109
            },
            {
                "month": 6,
                "value": 33.1,
                "matchedTradingVolume": 159161373
            },
            {
                "month": 7,
                "value": 35,
                "matchedTradingVolume": 108046493
            },
            {
                "month": 8,
                "value": 36,
                "matchedTradingVolume": 152167647
            },
            {
                "month": 9,
                "value": 39.5,
                "matchedTradingVolume": 129903345
            },
            {
                "month": 10,
                "value": 40.7,
                "matchedTradingVolume": 157780759
            },
            {
                "month": 11,
                "value": 39,
                "matchedTradingVolume": 124880714
            },
            {
                "month": 12,
                "value": 40.2,
                "matchedTradingVolume": 85316604
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 10,
                "value": 700
            }
        ]
    },
    {
        "symbol": "SHS",
        "companyName": "null",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 10,
                "matchedTradingVolume": 253793966
            },
            {
                "month": 2,
                "value": 9.3,
                "matchedTradingVolume": 251382589
            },
            {
                "month": 3,
                "value": 9.2,
                "matchedTradingVolume": 314457024
            },
            {
                "month": 4,
                "value": 10.6,
                "matchedTradingVolume": 486724587
            },
            {
                "month": 5,
                "value": 11.8,
                "matchedTradingVolume": 403628131
            },
            {
                "month": 6,
                "value": 14,
                "matchedTradingVolume": 512915603
            },
            {
                "month": 7,
                "value": 15.6,
                "matchedTradingVolume": 351958733
            },
            {
                "month": 8,
                "value": 18.6,
                "matchedTradingVolume": 505353394
            },
            {
                "month": 9,
                "value": 20.5,
                "matchedTradingVolume": 423334614
            },
            {
                "month": 10,
                "value": 18.2,
                "matchedTradingVolume": 572161445
            },
            {
                "month": 11,
                "value": 18.4,
                "matchedTradingVolume": 688673172
            },
            {
                "month": 12,
                "value": 19.7,
                "matchedTradingVolume": 423218842
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "SLS",
        "companyName": "CTCP Mía Đường Sơn La",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 141.5,
                "matchedTradingVolume": 105965
            },
            {
                "month": 2,
                "value": 153,
                "matchedTradingVolume": 371779
            },
            {
                "month": 3,
                "value": 151,
                "matchedTradingVolume": 107135
            },
            {
                "month": 4,
                "value": 175,
                "matchedTradingVolume": 243202
            },
            {
                "month": 5,
                "value": 172.5,
                "matchedTradingVolume": 214329
            },
            {
                "month": 6,
                "value": 174.3,
                "matchedTradingVolume": 161085
            },
            {
                "month": 7,
                "value": 217.5,
                "matchedTradingVolume": 317260
            },
            {
                "month": 8,
                "value": 218.4,
                "matchedTradingVolume": 460531
            },
            {
                "month": 9,
                "value": 207.9,
                "matchedTradingVolume": 338896
            },
            {
                "month": 10,
                "value": 215,
                "matchedTradingVolume": 570007
            },
            {
                "month": 11,
                "value": 158,
                "matchedTradingVolume": 344405
            },
            {
                "month": 12,
                "value": 151.3,
                "matchedTradingVolume": 273898
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 10,
                "value": 15000
            }
        ]
    },
    {
        "symbol": "TDN",
        "companyName": "CTCP Than Đèo Nai - Vinacomin",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 10.5,
                "matchedTradingVolume": 830221
            },
            {
                "month": 2,
                "value": 10.9,
                "matchedTradingVolume": 2139323
            },
            {
                "month": 3,
                "value": 10.6,
                "matchedTradingVolume": 872061
            },
            {
                "month": 4,
                "value": 12.1,
                "matchedTradingVolume": 2504970
            },
            {
                "month": 5,
                "value": 11.8,
                "matchedTradingVolume": 2689719
            },
            {
                "month": 6,
                "value": 11.3,
                "matchedTradingVolume": 2294625
            },
            {
                "month": 7,
                "value": 11.4,
                "matchedTradingVolume": 2683671
            },
            {
                "month": 8,
                "value": 11.2,
                "matchedTradingVolume": 2355125
            },
            {
                "month": 9,
                "value": 10.6,
                "matchedTradingVolume": 824593
            },
            {
                "month": 10,
                "value": 10,
                "matchedTradingVolume": 663198
            },
            {
                "month": 11,
                "value": 9.4,
                "matchedTradingVolume": 317910
            },
            {
                "month": 12,
                "value": 10.3,
                "matchedTradingVolume": 470014
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 5,
                "value": 800
            }
        ]
    },
    {
        "symbol": "TIG",
        "companyName": "CTCP Tập đoàn Đầu tư Thăng Long",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 9.4,
                "matchedTradingVolume": 14718354
            },
            {
                "month": 2,
                "value": 9.2,
                "matchedTradingVolume": 19183104
            },
            {
                "month": 3,
                "value": 8.5,
                "matchedTradingVolume": 12889752
            },
            {
                "month": 4,
                "value": 8.6,
                "matchedTradingVolume": 18732883
            },
            {
                "month": 5,
                "value": 11.5,
                "matchedTradingVolume": 33676420
            },
            {
                "month": 6,
                "value": 11.9,
                "matchedTradingVolume": 28614289
            },
            {
                "month": 7,
                "value": 12.6,
                "matchedTradingVolume": 26129853
            },
            {
                "month": 8,
                "value": 12.8,
                "matchedTradingVolume": 32215207
            },
            {
                "month": 9,
                "value": 12.1,
                "matchedTradingVolume": 15110764
            },
            {
                "month": 10,
                "value": 11.2,
                "matchedTradingVolume": 16428527
            },
            {
                "month": 11,
                "value": 12.2,
                "matchedTradingVolume": 36912427
            },
            {
                "month": 12,
                "value": 13.1,
                "matchedTradingVolume": 65307842
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "TNG",
        "companyName": "CTCP Đầu tư và Thương mại TNG",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 15.9,
                "matchedTradingVolume": 22788741
            },
            {
                "month": 2,
                "value": 18.8,
                "matchedTradingVolume": 53837540
            },
            {
                "month": 3,
                "value": 18.5,
                "matchedTradingVolume": 47327191
            },
            {
                "month": 4,
                "value": 20,
                "matchedTradingVolume": 48994383
            },
            {
                "month": 5,
                "value": 20.1,
                "matchedTradingVolume": 40664190
            },
            {
                "month": 6,
                "value": 20.5,
                "matchedTradingVolume": 37336160
            },
            {
                "month": 7,
                "value": 21.3,
                "matchedTradingVolume": 36046131
            },
            {
                "month": 8,
                "value": 21.3,
                "matchedTradingVolume": 39840949
            },
            {
                "month": 9,
                "value": 22.6,
                "matchedTradingVolume": 56823464
            },
            {
                "month": 10,
                "value": 21.6,
                "matchedTradingVolume": 57013818
            },
            {
                "month": 11,
                "value": 19.5,
                "matchedTradingVolume": 33075049
            },
            {
                "month": 12,
                "value": 20.4,
                "matchedTradingVolume": 41724689
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 1,
                "value": 400
            },
            {
                "month": 10,
                "value": 400
            }
        ]
    },
    {
        "symbol": "TVD",
        "companyName": "CTCP Than Vàng Danh - Vinacomin",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 13.6,
                "matchedTradingVolume": 4460374
            },
            {
                "month": 2,
                "value": 16.1,
                "matchedTradingVolume": 12369639
            },
            {
                "month": 3,
                "value": 15.2,
                "matchedTradingVolume": 5436677
            },
            {
                "month": 4,
                "value": 16,
                "matchedTradingVolume": 7688533
            },
            {
                "month": 5,
                "value": 16.3,
                "matchedTradingVolume": 10313929
            },
            {
                "month": 6,
                "value": 18,
                "matchedTradingVolume": 10095238
            },
            {
                "month": 7,
                "value": 16.6,
                "matchedTradingVolume": 9646606
            },
            {
                "month": 8,
                "value": 16.4,
                "matchedTradingVolume": 6320529
            },
            {
                "month": 9,
                "value": 14.9,
                "matchedTradingVolume": 2552604
            },
            {
                "month": 10,
                "value": 13.8,
                "matchedTradingVolume": 1537320
            },
            {
                "month": 11,
                "value": 12.9,
                "matchedTradingVolume": 1610533
            },
            {
                "month": 12,
                "value": 14.4,
                "matchedTradingVolume": 1243333
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 6,
                "value": 900
            }
        ]
    },
    {
        "symbol": "VC3",
        "companyName": "CTCP Tập đoàn Nam Mê Kông",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 31.9,
                "matchedTradingVolume": 3708499
            },
            {
                "month": 2,
                "value": 31,
                "matchedTradingVolume": 6255386
            },
            {
                "month": 3,
                "value": 29.8,
                "matchedTradingVolume": 6890555
            },
            {
                "month": 4,
                "value": 29.2,
                "matchedTradingVolume": 4813528
            },
            {
                "month": 5,
                "value": 32,
                "matchedTradingVolume": 10960064
            },
            {
                "month": 6,
                "value": 29.8,
                "matchedTradingVolume": 14275123
            },
            {
                "month": 7,
                "value": 25.7,
                "matchedTradingVolume": 9058122
            },
            {
                "month": 8,
                "value": 27.5,
                "matchedTradingVolume": 12952619
            },
            {
                "month": 9,
                "value": 26,
                "matchedTradingVolume": 7353372
            },
            {
                "month": 10,
                "value": 24.3,
                "matchedTradingVolume": 8545141
            },
            {
                "month": 11,
                "value": 24.4,
                "matchedTradingVolume": 11344333
            },
            {
                "month": 12,
                "value": 25,
                "matchedTradingVolume": 13213301
            }
        ],
        "dividendSpitingHistories": []
    },
    {
        "symbol": "VCS",
        "companyName": "CTCP Vicostone",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 57.8,
                "matchedTradingVolume": 1602832
            },
            {
                "month": 2,
                "value": 55,
                "matchedTradingVolume": 1419547
            },
            {
                "month": 3,
                "value": 52.4,
                "matchedTradingVolume": 733426
            },
            {
                "month": 4,
                "value": 52.2,
                "matchedTradingVolume": 1070085
            },
            {
                "month": 5,
                "value": 56.9,
                "matchedTradingVolume": 2587508
            },
            {
                "month": 6,
                "value": 61.7,
                "matchedTradingVolume": 3409753
            },
            {
                "month": 7,
                "value": 64.3,
                "matchedTradingVolume": 3504930
            },
            {
                "month": 8,
                "value": 67.5,
                "matchedTradingVolume": 4021339
            },
            {
                "month": 9,
                "value": 69,
                "matchedTradingVolume": 2404724
            },
            {
                "month": 10,
                "value": 63.8,
                "matchedTradingVolume": 2062699
            },
            {
                "month": 11,
                "value": 57.9,
                "matchedTradingVolume": 1492424
            },
            {
                "month": 12,
                "value": 57.3,
                "matchedTradingVolume": 859008
            }
        ],
        "dividendSpitingHistories": [
            {
                "month": 6,
                "value": 2000
            },
            {
                "month": 12,
                "value": 2000
            }
        ]
    },
    {
        "symbol": "VIG",
        "companyName": "null",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {
                "month": 1,
                "value": 6.1,
                "matchedTradingVolume": 3000777
            },
            {
                "month": 2,
                "value": 6.1,
                "matchedTradingVolume": 2827039
            },
            {
                "month": 3,
                "value": 5.8,
                "matchedTradingVolume": 6426854
            },
            {
                "month": 4,
                "value": 6.5,
                "matchedTradingVolume": 12815084
            },
            {
                "month": 5,
                "value": 7.7,
                "matchedTradingVolume": 13108227
            },
            {
                "month": 6,
                "value": 8.7,
                "matchedTradingVolume": 15290969
            },
            {
                "month": 7,
                "value": 8.6,
                "matchedTradingVolume": 16843152
            },
            {
                "month": 8,
                "value": 8.9,
                "matchedTradingVolume": 21454960
            },
            {
                "month": 9,
                "value": 10.8,
                "matchedTradingVolume": 26101975
            },
            {
                "month": 10,
                "value": 8.6,
                "matchedTradingVolume": 13054237
            },
            {
                "month": 11,
                "value": 7.9,
                "matchedTradingVolume": 12156118
            },
            {
                "month": 12,
                "value": 8.1,
                "matchedTradingVolume": 7288746
            }
        ],
        "dividendSpitingHistories": []
    }
]
