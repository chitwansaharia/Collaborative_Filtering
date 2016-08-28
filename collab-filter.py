import csv
import math

ifile = open('movie-ratings.csv','r')  #Pythonic Way to Access a SpreadSheet
reader = csv.reader(ifile)

userRatings = {}  #Use of Dictionary eases the code implementation
				 
data = list(reader)
movies = (data[0])[1:]	#Copying the first row of the spreadsheet to the the movies list(list of movies) 
for row in data[1:]:
	userRatings[row[0]] = list(map(float, row[1:])) #copying the rows to the userRatings Dictionary

ifile.close() #Closing the file object

ifile = open('user_preference.csv','r') #taking user response
reader = csv.reader(ifile)
data = list(reader) 
try:
	user_input = list(zip(data[0],list(map(float,data[1])))) #storing the user-ratings in the list programUser
	programUser = [None]*len(user_input)
	for x in user_input:
		programUser[movies.index(x[0])] = x[1]
except Exception:
	exit()	# incase there is any exception in taking input the program exits

def mean(x):		# a function to return mean of a list
	temp = list()
	for a in x:
		if not(a == -1):
			temp.append(a);			
	return sum(temp)/float(len(temp))

def coVariance(x,y):	# a function to return the covariance of two lists(random variables)
	xm,ym = mean(x), mean(y)
	xs,ys = [i-xm for i in x], [i-ym for i in y]	# a pythonic way to subtract a constant from each of the members of a list
	return sum([i*j for (i,j) in zip(xs,ys)])       # using sum function to avoid loop to perform the dot product to compute the covariance

def pearsonCorr(critic):
	criticRate = []
	userRate = []
	for x,y in zip(critic[1], programUser):
		if not(x == -1 or y == -1):
			criticRate.append(x);					# taking only the movies rated by both of them
			userRate.append(y);
	sigma1 = coVariance(criticRate,criticRate)		#variance of Critic Rating
	sigma2 = coVariance(userRate,userRate)			#variance of User Rating
	try:
		return (critic[0], coVariance(criticRate, userRate)/math.sqrt(sigma1*sigma2)) # using formula for correlation coefficient
	except ZeroDivisionError:
		if((sigma1 == 0 and sigma2 != 0) or (sigma1 != 0 and sigma2 == 0)): # the implementation in case the correlation is undefined
			return(critic[0],0)
		else:
			if(mean(criticRate) == mean(userRate)):
				return(critic[0],1)
			else:
				return(critic[0],0)
		

pearsonRel = list(map(pearsonCorr, userRatings.items())) #calling function to calculate a list of correlation coefficient of the critics with respect to the user
pearsonRel = sorted(pearsonRel, key= lambda x: x[1], reverse = True) # sorting the list

pearsonRel = list(map(lambda x:(x[0],(x[1],userRatings[x[0]])), pearsonRel))# making a dictionary contating the critic name as the key 
criticRatings = dict(pearsonRel) 											# and the correlation coefficient and the list of rating of different movies as values
def weightRating(i):										###################################################################
	def rating(x):											#			Procedure for Calculating Weighted Mean				  #								
		if x[1][i] == -1:									# The weighted mean is calculated as the sum of product of 		  #	
			return (0,0)									# (rating by a user-his average rating)(if it is rated) and his   # 
															# correlation coefficient with the user.                          # 
															#                												  #
															# Finally we divide this sigma with the sum of the absolute values# 
															# of the correlations of the critics taken into account.		  #									  
		else:												#																  #
			return (x[0]*(x[1][i]-mean(x[1])),abs(x[0]))	###################################################################
												
					
					

	r = tuple(map(sum, zip(*list(map(rating, criticRatings.values())))))

	return (movies[i], r[0]/r[1]) 
# the weigted ratings are stored in the weightedRatings list and it is sorted finally
weightedRatings = sorted(list(map(weightRating, range(len(movies)))), key = lambda x:x[1], reverse = True)
# the code to display the top three movies after the weighted ratings.

count = 0
for i in range(len(weightedRatings)):
	if (programUser[movies.index(weightedRatings[i][0])] == -1 and count <3):
		print(weightedRatings[i][0])
		count += 1