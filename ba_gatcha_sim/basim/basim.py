#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2026 mizma <omoikane@path-works.net>
# All rights reserved.

from enum import IntEnum


from pprint import pformat
import click
import random

class Level(IntEnum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

def pout(msg=None, Verbose=0, level=Level.INFO, newline=True):
    """stdout support method
    All Error, Critical and Info are printed out.
    while Warning and Debug are printed only with verbosity setting.
    INFO -- Intended for standard output. output to STDOUT
    DEBUG -- Intended for debug output. Shown only in verbosity>=2 output to STDOUT
    WARNING -- Intended to show detailed warning. Shown only in verbosity>=1.  output to STDERR
    ERROR -- Intended to show error.  output to STDERR
    CRITICAL -- Intended to show critical error. output to STDERR

    Keyword Arguments:
        msg (string) -- message to print (default: {None})
        Verbose (Int) -- Set True to print DEBUG message (default: {0})
        level (Level) -- Set message level for coloring (default: {Level.INFO})
        newline (bool) -- set to False if trailing new line is not needed (default: {True})
    """
    error=False
    if level in {Level.NOTSET, Level.DEBUG}:
        # blah
        if Verbose < 2:
            return
        fg = 'magenta'
    elif level == Level.INFO:
        fg = 'green'
    elif level == Level.WARNING:
        if Verbose < 1:
            return
        fg = 'yellow'
        error=True
    elif level in {Level.ERROR, Level.CRITICAL}:
        fg = 'red'
        error=True
    else:
        fg = 'white'
        pass
    click.echo(click.style(str(msg), fg=fg), nl=newline, err=error)

def old_pull(count, Verbose=0):
    if count >= 199:
        return True # TODO: この場合200連目でピックアップ排出が0.7%のほうで出た場合、１体目ならそこで終了できる事が考慮できていない。
    elif random.random() < 0.007:
        return True
    else:
        return False

def old_sim(target=2, cycles=10000, reset=False, rcount=2, Verbose=0):
    pout("Starting Old Gatcha Simulation")
    pout(f"target={target}, cycles={cycles}", Verbose, Level.DEBUG )
    MAX_PULLS = (target * 200)

    histogram = [0] * (MAX_PULLS + 1)
    cumulative = [0] * (MAX_PULLS + 1)
    for _ in range(cycles):
        pulls   = 0 # initialize current pull count
        p_cnt     = 0 # initialize the pitty count
        # run simulation for cycles times

        for pull in range(MAX_PULLS):
            if old_pull(p_cnt, Verbose):
                p_cnt += 1
                pout(f"Success at pull={pull}, p_cnt={p_cnt}", Verbose, Level.DEBUG)
                pulls += 1
                if reset and pulls == rcount:
                    p_cnt = 0
                if pulls == target:
                    histogram[pull+1] += 1
                    break
            else:
                p_cnt += 1
            if p_cnt == 200:
                p_cnt = 0
        pass
    pout(f"OLD: {histogram}",Verbose,Level.DEBUG)
    cumul = 0
    for i in range(MAX_PULLS + 1):
        cumul += histogram[i]
        cumulative[i] = cumul
    pout(f"OLD: {cumulative}", Verbose, Level.DEBUG)

    results = {}
    results["hist"] = histogram
    results["cumul"] = cumulative
    return results

def new_pull(count, Verbose=0):
    if count >= 199:
        return True
    elif count == 99 and random.random() < 0.5:
        return True
    elif random.random() < 0.007:
        return True
    else:
        return False

def new_sim(target=2, cycles=10000, count=0, reset=False, rcount=2, Verbose=0):
    pout("Starting New Gatcha Simulation")
    pout(f"target={target}, cycles={cycles}, count={count}", Verbose, Level.DEBUG )
    MAX_PULLS = (target * 200)

    histogram = [0] * (MAX_PULLS + 1)
    cumulative = [0] * (MAX_PULLS + 1)
    for _ in range(cycles):
        pulls   = 0 # initialize current pull count
        p_cnt     = count # initialize the pitty count
        tickets = 0
        tickets_used = 0
        mileage = 0
        mileage_bonus = {
            70, 130, 150, 170,
            270, 330, 350, 370
        }
        # run simulation for cycles times

        for pull in range(MAX_PULLS):
            pout(f"[{pull}] : pulls={pulls} p_cnt={p_cnt} tickets={tickets} utickets={tickets_used} mile={mileage}",
                 Verbose, Level.DEBUG )
            if tickets > 0:
                success = False
                for _ in range(tickets):
                    mileage += 1
                    tickets -= 1
                    tickets_used += 1
                    if new_pull(p_cnt, Verbose):
                        p_cnt = 0
                        success = True
                    else:
                        p_cnt += 1
                pout(f"[{pull}] : TICKET pulls={pulls} p_cnt={p_cnt} tickets={tickets} utickets={tickets_used} mile={mileage}",
                    Verbose, Level.DEBUG )
                if success:
                    pulls += 1
                    if reset and pulls == rcount:
                        mileage = 0
                    if pulls == target:
                        pout(f"RECORD: {pull+tickets_used}", Verbose, Level.DEBUG)
                        histogram[pull] += 1
                        break

            if new_pull(p_cnt, Verbose):
                pout(f"Success at pull={pull+1}, p_cnt={p_cnt}", Verbose, Level.DEBUG)
                p_cnt   = 0     # Reset pitty count every successful pull
                mileage += 1
                if mileage in mileage_bonus:
                    tickets += 10
                pulls   += 1
                if reset and pulls == rcount:
                    mileage = 0
                if pulls == target:
                    pout(f"RECORD: {pull+1+tickets_used}", Verbose, Level.DEBUG)
                    histogram[pull+1] += 1
                    break
            else:
                p_cnt += 1
                mileage += 1
                if mileage in mileage_bonus:
                    tickets += 10
        pass
    pout(f"NEW: {histogram}",Verbose,Level.DEBUG)
    cumul = 0
    for i in range(MAX_PULLS + 1):
        cumul += histogram[i]
        cumulative[i] = cumul
    pout(f"NEW: {cumulative}", Verbose, Level.DEBUG)

    results = {}
    results["hist"] = histogram
    results["cumul"] = cumulative
    return results

def cmd(kwargs):
    """BlueArchive gatcha monte-carlo simulation
    Implementation.

    Args:
        kwargs (dict): command line arguments parsed by Click library
    """
    verbose = kwargs["verbose"]
    pout("Command line arguments:", verbose, Level.INFO)
    pout(pformat(kwargs,depth=3,indent=4), verbose, Level.INFO)


    # 1. Now parse kwargs
    count   = kwargs['count']
    cycles  = kwargs['cycles']
    run_new = kwargs['new']
    run_old = kwargs['old']
    target  = kwargs['target']
    reset   = kwargs['reset']
    rcount  = kwargs['reset_count']
    Verbose = kwargs['verbose']

    # 2. and do it's bidding
    if run_new:
        new_res = new_sim(target, cycles, count, reset, rcount, Verbose)

    if run_old:
        old_res = old_sim(target, cycles, reset, rcount, Verbose)

    MAX_PULLS = (target * 200)
    if run_new and run_old:
        print("PULLS,NEW HIST,NEW CUMUL(%),OLD HIST,OLD CUMUL(%)")
        for i in range(MAX_PULLS + 1):
            print(f"{i},{(new_res['hist'][i]/cycles)*100},{(new_res['cumul'][i]/cycles)*100},{(old_res['hist'][i]/cycles)*100},{(old_res['cumul'][i]/cycles)*100}")
    elif run_new:
        print("PULLS,NEW HIST,NEW CUMUL(%)")
        for i in range(MAX_PULLS + 1):
            print(f"{i},{(new_res['hist'][i]/cycles)*100},{(new_res['cumul'][i]/cycles)*100}")
    elif run_old:
        print("PULLS,OLD HIST,OLD CUMUL(%)")
        for i in range(MAX_PULLS + 1):
            print(f"{i},{(old_res['hist'][i]/cycles)*100},{(old_res['cumul'][i]/cycles)*100}")
    pass
