from datetime import datetime, timezone, timedelta

def get_datetime_str(datetime_utc):
	now = datetime.now(timezone(timedelta(hours=+9)))
	datetime_jst = datetime_utc.astimezone(timezone(timedelta(hours=+9)))
	if now.year != datetime_jst.year:
		str_jst = datetime_jst.strftime('%y/%-m/%-d %H:%M')
	elif now.month != datetime_jst.month or now.day != datetime_jst.day:
		str_jst = datetime_jst.strftime('%-m/%-d %H:%M')
	else:
		str_jst = datetime_jst.strftime('%H:%M')
	return str_jst
