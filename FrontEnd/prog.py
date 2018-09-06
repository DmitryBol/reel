import os
import ntpath


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


directory = os.path.dirname('D:\\PyCharm\\PycharmProjects\\reel\\Front-end\\sas.json')
leaf = path_leaf('D:\\PyCharm\\PycharmProjects\\reel\\Front-end\\sas.json')
print(directory)
print(leaf)
name = leaf.split('.')[0]
print(name)
print(os.path.exists(directory + '\\' + name + '_reels.json'))
