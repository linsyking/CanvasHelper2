# coding=utf-8
'''
@Author: King
@Date: 2023-02-16 12:12:05
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''


import git
import os
import logging

'''
Update git repo automatically
'''


def update():
    repo = git.Repo(os.path.dirname(__file__))
    current = repo.head.commit
    if current != repo.head.commit:
        logging.info(f"Found new commit: {repo.head.commit}, pulling")
        repo.remotes.origin.pull()
    else:
        logging.info(f"Current version: {current}")
        logging.info("No updates found.")

if __name__ == "__main__":
    update()