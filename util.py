from datetime import timezone, timedelta

def get_jst_HM(datetime_utc):
	datetime_jst = datetime_utc.astimezone(timezone(timedelta(hours=+9)))
	str_jst = datetime_jst.strftime('%H:%M')
	return str_jst

def get_jst_YMDHM(datetime_utc):
	datetime_jst = datetime_utc.astimezone(timezone(timedelta(hours=+9)))
	str_jst = datetime_jst.strftime('%y/%-m/%-d %-H:%M')
	return str_jst
