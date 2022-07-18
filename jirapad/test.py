#!/usr/bin/env python3
"""
Test of creating Jita Cloud Issues dependency graph.
Usage:
python3 test.py > test.dot && -Tsvg -o test.svg test.dot
"""

# 1. std
import configparser
# import pprint
import os
import sys
from enum import IntEnum, auto
# 2. 3rd
from atlassian import Jira

HEAD = """digraph Jira {
rankdir=LR;
"""
# graph [autosize=false, size="11.7,8.3!"]
TAIL = "}"


class EIssueType(IntEnum):
    Task = 10001        # Задача
    Epic = 10002        # Эпик
    SubTask = 10003     # Subtask
    Bug = 10004         # Баг
    Assignment = 10005  # Задание


class EIssueStatus(IntEnum):
    Task = 10000
    InProgress = 10001
    Test = 10002
    Done = 10003


class ELinkType(IntEnum):
    Child = auto()      # task -> epic, subtask -> task
    Blocks = auto()     # blocker -> blocked


# decoration
TypeShape = {
    EIssueType.Task.value: 'rect',
    EIssueType.Epic.value: 'folder',
    EIssueType.SubTask.value: 'hexagon',
    EIssueType.Bug.value: 'octagon',
    EIssueType.Assignment.value: 'note'
}


StatusColor = {
    EIssueStatus.Task.value: 'silver',
    EIssueStatus.InProgress.value: 'yellow',
    EIssueStatus.Test.value: 'green',
    EIssueStatus.Done.value: 'blue',
}


LinkStyle = {
    ELinkType.Child.value: 'dotted',
    ELinkType.Blocks.value: 'solid',
}


class VARS(object):
    url: str
    user: str
    apikey: str


def __load_cfg():
    """
    Load app variables
    :return:
    """
    with open('jirapad.ini', "rt") as cfg:
        config = configparser.ConfigParser()
        config.read_string("[{}]\n{}".format('DEFAULT', cfg.read()))
        config_default = config['DEFAULT']
        VARS.url = config_default.get('url')
        VARS.user = config_default.get('user')
        VARS.apikey = config_default.get('apikey')
        return True


def __out_node(issue: dict):
    """Output issue as graphiviz node.
    Example: id_12345 [label="PROJ-123: Simple todo" shape=ellipse style=filled fillcolor=green];
    """
    print("id_{id} [label=\"{key}: {summary}\" shape={shape} style=filled fillcolor={color} URL=\"{url}\"];".format(
        id=issue['id'],
        key=issue['key'],
        summary=issue['fields']['summary'],
        shape=TypeShape[int(issue['fields']['issuetype']['id'])],
        color=StatusColor[int(issue['fields']['status']['id'])],
        url=os.path.join(VARS.url, 'browse', issue['key'])
    ))


def __out_link(src: dict, dst: dict, ltype: ELinkType):
    print("id_{src} -> id_{dst} [style={style}];".format(
        src=src['id'],
        dst=dst['id'],
        style=LinkStyle[ltype.value]
    ))


def main():
    if not __load_cfg():
        sys.exit()
    jira = Jira(
        url=VARS.url,
        username=VARS.user,
        password=VARS.apikey,
        cloud=True)
    # 1. load issues
    projects = jira.projects(included_archived=None)
    proj_key = projects[0]['key']
    # project = jira.project(key) - oops
    # issue_count = jira.get_project_issues_count(proj_key)  # 161
    issue_list = list()
    offset = 0
    while tmp := jira.get_all_project_issues(proj_key, start=offset, limit=50):
        offset += len(tmp)
        issue_list.extend(tmp)
    # 2. flow 1: print
    print(HEAD)
    for issue in issue_list:
        if int(issue['fields']['status']['id']) == EIssueStatus.Done.value:
            continue
        __out_node(issue)
    # 3. flow 2: links
    for issue in issue_list:
        if int(issue['fields']['status']['id']) == EIssueStatus.Done.value:
            continue
        fields = issue['fields']
        if parent := fields.get('parent'):  # epic, supertask
            __out_link(issue, parent, ELinkType.Child)
        for link in fields['issuelinks']:  # blocks
            if out := link.get('outwardIssue'):
                __out_link(issue, out, ELinkType.Blocks)
    print(TAIL)
    # pprint.pprint(jira.issue('WAXA-179'))  # subtask of waxa-177


if __name__ == '__main__':
    main()
