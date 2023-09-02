from time import sleep
from supp.db_human import Sql
import datetime
from supp import dt_human

columns = [("event_id", "text"),
    ("user_id", "text"),
    ("event", "text"),
    ("description", "text"),
    ("created", "text"),
    ("expires", "text"),
    ("extra", "text"),
    ("channel_src", "text"),
    ("channel_dst", "text"),
    ("status", "text"),
    ]

for i in range(10):

    columns = [("event_id", dt_human.sid()),
        ("user_id", "926846583788687402"),
        ("event", f"test10"),
        ("description", f"test10"),
        # ("created", dt_human.sft(src=datetime.datetime.utcnow(), fmt="f")),
        # ("expires", dt_human.sft(datetime.datetime.utcnow()+datetime.timedelta(hours=10), fmt="f")),
        ("created", str(datetime.datetime.utcnow())),
        ("expires", str(datetime.datetime.utcnow()+datetime.timedelta(hours=10))),
        ("extra", "extra"),
        ("channel_src", "941248155415093260"),
        ("channel_dst", "952299623886749696"),
        ("status", "1"),
        ]

    Sql().insert(table='reminder', columns=columns)
    sleep(60)


# Sql().create_table(table='reminder_arc', columns=columns, replace=False)
query = "UPDATE reminder SET status = '0' where event_id = '20220323022709189860'"
query = "INSERT INTO reminder_arc SELECT * FROM reminder where event_id = '20220323022709189860';"
query = "DELETE FROM reminder_arc where event_id = '20220323022709189860'"
query = "SELECT * FROM reminder_arc LIMIT 3"
# query = "DELETE FROM reminder_arc"
# aa = Sql().fetch(query)
# Sql().clear(table='reminder')