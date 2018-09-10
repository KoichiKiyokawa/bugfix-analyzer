from git import *
import datetime
import time

repo = Repo('./')
cnt = 0
sum_insertions = 0
for item in repo.iter_commits('master'):
    # print(item.stats.total['insertions']) ok
    # cnt += 1
    # if 1000 < cnt <= 2000:
    sum_insertions += item.stats.total['insertions']
    for diff_added in item.diff().iter_change_type('A'):
        print(diff_added)

print(sum_insertions)