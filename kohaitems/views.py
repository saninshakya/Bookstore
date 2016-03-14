from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from kohaitems.forms import IsbnForm
# import MySQLdb

@user_passes_test(lambda u:u.is_staff)
def display_item_from_koha(request):
	form = IsbnForm()
	if request.method == 'POST':
		return HttpResponse("form submitted")
		# KOHA database connection
		# koha_database_connection()
	else:
		return render(request, 'items/addkoha.html',{'form':form})


# def koha_database_connection(request):
# 	# connect
# 	db = MySQLdb.connect(host="192.168.1.35:22", user="root", passwd="crossword", db="koha_demo")

# 	cursor = db.cursor()

# 	# execute SQL select statement
# 	cursor.execute("SELECT * FROM items")

# 	# commit your changes
# 	db.commit()

# 	# get the number of rows in the resultset
# 	numrows = int(cursor.rowcount)

# 	# get and display one row at a time.
# 	# for x in range(0,numrows):
# 	#     row = cursor.fetchone()
# 	#     print row[0], "-->", row[1]
