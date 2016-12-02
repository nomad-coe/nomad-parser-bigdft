# from yaml import CLoader as Loader
from yaml import Loader

with open("node_data.yml", "r") as fin:
    loader = Loader(fin)

    node = loader.compose_node()
    print(node)

    # while(True):
        # token = loader.get_token()
        # if token is None:
            # break
        # print(token)
