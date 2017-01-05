import os, re, praw
import datetime


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def get_date(date_str):
	origin_time = datetime.datetime.fromtimestamp(date_str)
	dif = datetime.datetime.utcnow() - origin_time
	dif = dif - datetime.timedelta(hours=5)
	return strfdelta(dif, "{hours} {minutes}")

def user_friendly_time(date):
	date_tokens = date.split(" ")
	if date_tokens[0] == "0":
		if date_tokens[1] != "1":
			return_date = date_tokens[1] + " minutes ago"
			return return_date
		else:
			return_date = date_tokens[1] + " minute ago" 
			return return_date
	if date_tokens[0] == "1":
		return_date = date_tokens[0] + " hour and "
		if date_tokens[1] != "1":
			return_date += date_tokens[1] + " minutes ago"
			return return_date
		else:
			return_date = date_tokens[1] + " minute ago" 
			return return_date
	else:
		return_date = date_tokens[0] + " hours and "
	if date_tokens[1] != "1":
		return_date += date_tokens[1] + " minutes ago"
		return return_date
	else:
		return_date = date_tokens[1] + " minute ago" 
		return return_date


def create_msg(title, date):
	final_msg = "\"" + title + "\" was submitted " + user_friendly_time(date)
	return final_msg


# main

# create reddit instance
user_agent = ("")
r = praw.Reddit(client_id='2',
				client_secret='',
				password='',
				username='',
				user_agent=user_agent)

# open file, get subs
with open("sub_list.txt", "r") as f:
	subs = f.readlines()

# loop through subs and get newest post
final_msgs = []
for sub in subs:
	subr = r.subreddit(sub.strip('\n'))
	new_posts = subr.new(limit=5)
	for post in new_posts:
		# gather post information	
		post_title = post.title 
		post_date = get_date(post.created_utc)
		# create message
		final_msgs.append(create_msg(post_title.encode("utf-8"), post_date))

i_subs = 0
i_msgs = 0 
msg_to_sub = ""
for sub in subs:
	msg_to_sub += "In r/" + subs[i_subs].strip('\n') + ":\n"
	for i in range(0, 5):
		msg_to_sub += "\t" + final_msgs[i_msgs] + "\n"
		i_msgs += 1
		if i_msgs % 5 == 0:
			break
	i_subs += 1

print msg_to_sub
# send PM 