from yaml import CLoader as Loader

from pympler import tracker
tr = tracker.SummaryTracker()
tr.print_diff()
tr.print_diff()

with open("data.yml", "r") as fin:
    loader = Loader(fin)
    # data = loader.get_data()
    # tr.print_diff()
    index = 0
    while(loader.check_data()):
        token = loader.get_token()
        index += 1
        if index % 100 == 0:
            tr.print_diff()
            print(token)
