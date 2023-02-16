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
    try:
        repo = git.Repo(os.path.dirname(__file__))
        current = repo.head.commit
        logging.info(f"Current version: {current}")
        repo.remotes.origin.pull()
        new = repo.head.commit
        if current != new:
            logging.info(f'Updated to {new}')
    except Exception as e:
        logging.error(e)
        logging.error('Cannot update')

if __name__ == "__main__":
    update()