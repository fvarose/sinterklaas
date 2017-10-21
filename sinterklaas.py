#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Helper script for "Secret Santa"-like events. """

import argparse
import configparser
import copy
import random

class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.target = None
    def __str__(self):
        return "<%s: %s>" % (self.name, self.email)
    def __repr__(self):
        return "<%s: %s>" % (self.name, self.email)

def parse_arguments():
    ''' Define and parse command line arguments '''
    parser = argparse.ArgumentParser(description='Random Secret Santa assignements \
                                                  and email sending.')
    parser.add_argument('action', metavar='action',
                        type=str, nargs='+',
                        choices=['test', 'execute'],
                        help='the action to perform')
    return parser.parse_args()

def interpret_arguments(args):
    ''' Warn the user if test mode is off.
        Return whether test mode is enabled '''
    if 'test' in args.action:
        test = True
    else:
        print('/!\\ Warning /!\\')
        print('This will perform the final draw and send out emails to everyone.')
        print('Are you sure you want to continue?')
        response = input('[y/n]')
        if response is not 'y':
            print('No action performed, exiting')
            exit()
        else:
            test = False
    return test

def read_config():
    ''' Read the config.ni file '''
    config = {
        'participants' : [],
    }
    parser = configparser.ConfigParser()
    parser.optionxform = str # don't convert keys to lower-case
    if not parser.read('config.cfg', encoding='utf-8'):
        print('-- Error: could not find config.cfg file, exiting.')
        exit()
    config['participants'] = [Person(name, email) for (name, email) in list(parser['Participants'].items())]
    return config

def draw(people, test):
    ''' Draw Secret Santas '''
    print("--- Draw in progress ---")
    print("{} people are in the list:".format(len(people)))
    for person in people: print(person)

    # Create a randomized version of the list of people
    randomized_people = copy.deepcopy(people)
    random.shuffle(randomized_people)
    
    # Each person's target is their successor in the randomized list
    for i, person in enumerate(randomized_people):
        person.target = randomized_people[(i+1) % len(randomized_people)]

    print("--- Draw finished ---")
    for person in randomized_people: print("{} picked {}".format(person.name, person.target.name))

    return randomized_people

def notify(test):
    ''' Notify participants by email '''
    print('notify (test: {})'.format(test))

def main():
    ''' Main '''
    args = parse_arguments()
    config = read_config()
    test = interpret_arguments(args)

    people = config['participants']
    people = draw(people, test)
    notify(test)

if __name__ == "__main__":
    main()
