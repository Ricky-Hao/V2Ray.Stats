# V2Ray.Stats
Collect V2Ray traffic stats by API.

## Install
`pip install v2ray_stats`

## Usage
```
usage: v2ray_stats [-h] [-d [database]] [-c [config_path]] [--debug]
                   [-s [server]] [--interval [INTERVAL]] [-q] [-y [YEAR]]
                   [-m [MONTH]] [-e]

Collect V2Ray user traffic stats.

optional arguments:
  -h, --help            show this help message and exit

General:
  General settings.

  -d [database]         Database file path.
  -c [config_path]      Config file path.
  --debug               Debug mode.

Daemon:
  Daemon settings.

  -s [server]           V2Ray API server address.
  --interval [INTERVAL]
                        Collector interval.

Query:
  Query settings.

  -q                    Query mode, with -y and -m to specific month.
  -y [YEAR]             Query year.
  -m [MONTH]            Query month.
  -e                    Send traffic report email to user.
```

Start daemon to collect v2ray account's traffic stats.  
```
python -m v2ray_stats -s 127.0.0.1:2335
[INFO][2019-03-24 22:35:14] [V2Ray.Stats][utils]: Running in background.
```

Query account's traffic stats.  
```
python -m v2ray_stats -q -y 2019 -m 3
Table: outband
+------------------+---------+
|      Email       |  Usage  |
+==================+=========+
| a959695@live.com |  38.61M |
+------------------+---------+

Table: inbound
+------------------+---------+
|      Email       |  Usage  |
+==================+=========+
| a959695@live.com |   8.90M |
+------------------+---------+
```

Query account's traffic stats and send email to user. (Only outbound)
```
python -m v2ray_stats -c /etc/v2ray_stats/config.json -q -m 3 -e
Table: outband
+------------------+---------+
|      Email       |  Usage  |
+==================+=========+
| a959695@live.com |  38.61M |
+------------------+---------+

Table: inbound
+------------------+---------+
|      Email       |  Usage  |
+==================+=========+
| a959695@live.com |   8.90M |
+------------------+---------+

[INFO][2019-03-24 22:33:07] [V2Ray.Stats][utils]: Start to send email.
[INFO][2019-03-24 22:33:08] [V2Ray.Stats][utils]: Send traffic to: a959695@live.com.
[INFO][2019-03-24 22:33:08] [V2Ray.Stats][utils]: Done.
```
