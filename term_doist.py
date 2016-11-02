#!/usr/bin/python3
"""
.. module:: term_doist
   :platform: Linux, Windows
   :synopsis: A Todoist python cli library/tool.

.. moduleauthor:: Ryan Parkyn <ryan@ryanparkyn.ca>

This module is intended as a stand-alone interface
to add and read Todoist tasks.

Config goes in ``/etc/term-doist/tdconfig.py``

The file contains::

    api_key = '<YourKeyHere12345>'

"""

import todoist
import argparse
import sys
sys.path.insert(0, '/etc/term-doist/')  # import api key and options
import tdconfig

def reset_sync(api):
    """Reload the sync with Todoist.

     Args:
       api (obj):  The api object.

     Returns:
       Modifies the api object.

    """
    api.reset_state()
    results = api.sync(commands=[])
    print("Reset")
    return results


def task_list(api, results):
    """Display the task list.

    Args:
       api (obj):  The api object.
       results (dict): Results from the latest sync

    Returns:
       int:  The return code::

          0 -- Success!
          !0 -- Uh oh!

    """
    print('┌{:─^3}─┰{:─<3}┰{:─^51}┰{:─^7}┐'.format("", "", "", ""))
    print('│{0:^3} ┃{2:<3}┃{1:^51}┃{3:^}│'.format("#", "Task Notes", "Pr⬆", "Project"))
    print('┝{:━^3}━╇{:━<3}╇{:━^51}╇{:━^7}┥'.format("", "", "", ""))

    for i in range(0, len(results['items'])):
        if results['items'][i]['item_order'] != 14:
            prio = "➡" * (results['items'][i]['priority'] - 1)
            for j in range(0, len(results['projects'])):
                if results['items'][i]['project_id'] == results['projects'][j]['id']:
                    proj = results['projects'][j]['name'][0:7]
            if (results['items'][i]['priority'] - 1) == 3:

                print('│\033[7m{0:<3d} │{2:<3}┝ {1:50}│{3:<7}\033[1;m│'.format(i, results['items'][i]['content'][0:40],
                                                                               prio, proj))
                
            else:

                print('│{0:<3d} │{2:<3}┝ {1:50}│{3:<7}│'.format(i, results['items'][i]['content'], prio, proj))

    print('└{:─^3}─┴{:─<3}┴{:─^51}┴{:─^7}┘'.format("", "", "", ""))


def task_add(api, results, task_list, project, priority):
    """Add a task to the list.

    Args:
       api (obj):  The api object.
       results (dict): Results from the latest sync
       task_list (list): Task converted to list
       project (int): The project (folder) number
       priority (int): 1-4 priority, effort based.

    Returns:
       list:  The returned ID and data

    """
    print("task added")
    task = (" ".join(task_list))
    print("task", task)
    print("priority", priority)
    proj = ""
    for j in range(0, len(results['projects'])):
        if results['projects'][j]['name'] == project:
            proj = results['projects'][j]['id']
    print("proj:", project, "(", proj, ")")
    api.items.add(task, proj, priority=priority)
    api.commit()


def main():                                                                                                        
                                                                                                                        
# Get a first run of the sync results.                                                                                  
    api = todoist.TodoistAPI(tdconfig.api_key)
    api.reset_state()
    results = api.sync(commands=[])
                                                                                                                        
    parser = argparse.ArgumentParser(description='A tool to allow you to add and list tasks from Todoist.\
                                               The default behaviour is to list your tasks. (defaults) are in ()\'s. ')
    parser.add_argument('-a', '--add',
                        help='Add task',
                        action='store',
                        dest='task',
                        nargs='*')
    parser.add_argument('-p', '--project',
                        help='Project (Inbox)',
                        action='store',
                        dest='project',
                        default="Inbox")
    parser.add_argument('-P', '--priority',
                        help='Priority 1 - 4 Low Med High Urgent (1 "Low Energy")',
                        type=int,
                        action='store',
                        dest='priority',
                        default=1)

    args = parser.parse_args()

    if args.task:
        task_add(api, results, args.task, args.project, args.priority)                    
        results = reset_sync(api)                                                      
        task_list(api, results)                                                                
    else:                                                                                                   
        task_list(api, results)                                                                           
                                                                                                                        
                                                                                                                        
if __name__ == "__main__":                                                                                             
    main()

