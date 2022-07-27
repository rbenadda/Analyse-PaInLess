#! /bin/bash

ls $1 | grep "selected" | grep "time" | xargs mv -t /data/rbenadda/painless-sat-competition-2022/painless/data/logs_after_time_selection/
ls $1 | grep "selected" |  xargs mv -t /data/rbenadda/painless-sat-competition-2022/painless/data/logs_after_selection/
ls $1 | grep "time" |  xargs mv -t /data/rbenadda/painless-sat-competition-2022/painless/data/logs_before_time_selection/
ls $1 | xargs mv -t /data/rbenadda/painless-sat-competition-2022/painless/data/logs_before_selection/