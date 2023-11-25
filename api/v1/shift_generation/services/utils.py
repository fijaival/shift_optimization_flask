# 連続勤務の取得
def get_consecutive_work_days(shifts):
    count = 0
    for shift in reversed(shifts):
        if shift in ['日勤', 'N']:
            count += 1
        else:
            break
    return count

# 最終日が夜勤か否か


def is_last_day_n(shifts):
    return 1 if shifts[-1] == 'N' else 0
