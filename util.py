from datetime import timezone, timedelta

def get_jst_str(datetime_utc):
	datetime_jst = datetime_utc.astimezone(timezone(timedelta(hours=+9)))
	str_jst = datetime_jst.strftime('%H:%M')
	return str_jst
