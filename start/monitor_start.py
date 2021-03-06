#!/usr/bin/env python
# -*- coding: utf-8 -*

import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler

import init_work_home

work_home = init_work_home.init()

from config.config import MonitorConfig
from utils.logger import logger
import monitor.node_monitor
import monitor.eos_process_monitor
import monitor.bp_status_monitor
import monitor.bp_block_monitor
import monitor.bidname_status

sched = BlockingScheduler()


def auto_claim():
    claim_command = str(work_home) + '/claim/auto_claim.sh'
    subprocess.call(claim_command)


def init_jobs():
    if MonitorConfig.bp_status_monitor_enable():
        sched.add_job(monitor.bp_status_monitor.main, 'interval', minutes=10, id='bp_status_monitor')
    if MonitorConfig.node_monitor_enable():
        sched.add_job(monitor.node_monitor.main, 'interval', minutes=5, id='node_monitor')
    if MonitorConfig.eos_process_monitor_enable():
        sched.add_job(monitor.eos_process_monitor.main, 'interval', seconds=30, id='process_monitor')
    if MonitorConfig.bp_block_monitor_enable():
        sched.add_job(monitor.bp_block_monitor.main, 'interval', minutes=5, id='bp_block_monitor')
    if MonitorConfig.bidname_monitor_enable():
        sched.add_job(monitor.bidname_status.main, 'interval', minutes=30, id='bidname')
    if MonitorConfig.auto_claim_enable():
        sched.add_job(auto_claim, 'interval', hours=1, id='auto_claim')


def start_jobs():
    jobs = sched.get_jobs()
    if jobs:
        logger.info(jobs)
        sched.start()


if __name__ == '__main__':
    init_jobs()
    start_jobs()
