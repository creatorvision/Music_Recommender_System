# A dictionary of users and the feature count of a small
# set of music items
songs={'dev': {'summer of 69': 3.5, 'numb': 3.5, 'demons': 4.0, 'sugar':4.0, 'main toh jhum':3.5,
'in the end': 3.0, 'cloud nine': 3.5, '21 guns':4.0, 'wake me up':4.5, 'broken dreams':3.5, 'kabhi kabhi': 1.5,
'aanewala pal': 1.5},
'swapnil': {'summer of 69': 3.5, 'numb': 4.0, 'mockingbird': 4.0, 'lose yourself': 3.5,
'in the end': 3.5, 'cloud nine': 3.5, '21 guns':4.0, 'wake me up':4.5, 'broken dreams':3.5, 'kabhi kabhi': 1.5,
'aanewala pal': 2.0},
'kshitij': {'summer of 69': 2.5, 'numb': 2.5,
'in the end': 2.0, 'cloud nine': 2.5, 'kabhi kabhi': 3.5,
'aanewala pal': 4.5, 'woh shaam':3.5, 'jeena yahan':4.0, 'kuch toh log':3.5, 'duniya bananewale':3.5},
'prudhvi': {'summer of 69': 2.5, 'numb': 2.5, 'musaphir': 3.0, 'chalte chalte mere': 3.5,
'in the end': 2.0, 'cloud nine': 2.5, 'kabhi kabhi': 3.0,
'aanewala pal': 4.0, 'woh shaam':3.5, 'jeena yahan':4.0, 'kuch toh log':3.0, 'duniya bananewale':2.5},
'rahul': {'party all night': 3.5, 'after party': 4.0,
'bandeya': 3.5, 'agar tum saath': 3.5, '21 guns':2.0, 'wake me up':2.5, 'party tonight':3.5, 'kabhi kabhi': 2.5,
'aanewala pal': 1.0, 'tu bin bataye': 4.5, 'raabta': 3.5},
'nishant': {'party all night': 3.5, 'after party': 4.0,
'bandeya': 3.5, 'agar tum saath': 3.5, '21 guns':2.0, 'wake me up':2.5, 'party tonight':3.5, 'kabhi kabhi': 2.5,
'aanewala pal': 1.0}, 
'test': {'jiya ho':3.0}}

users={'dev': {'indian_classic':3,'pop':7,'rap':0,'romantic':3,'rock':2},
'swapnil': {'indian_classic':2,'pop':5,'rap':2,'romantic':3,'rock':2},
'kshitij': {'indian_classic':6,'pop':2,'rap':0,'romantic':3,'rock':0},
'prudhvi': {'indian_classic':8,'pop':2,'rap':0,'romantic':4,'rock':0},
'rahul': {'indian_classic':2,'pop':9,'rap':0,'romantic':6,'rock':0},
'nishant': {'indian_classic':2,'pop':7,'rap':0,'romantic':4,'rock':0}}


from math import sqrt

def hello(var):
	print "hello"

# Returns a distance-based similarity score for person1 and person2
def sim_distance_pearson(prefs,person1,p2):
	# Get the list of mutually rated items
	si={}
	for item in prefs[person1]:
		if item in prefs[p2]: si[item]=1
	# Find the number of elements
	n=len(si)
	# if they are no ratings in common, return 0
	if n==0: return 0
	# Add up all the preferences
	sum1=sum([prefs[person1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])
	# Sum up the squares
	sum1Sq=sum([pow(prefs[person1][it],2) for it in si])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
	# Sum up the products
	pSum=sum([prefs[person1][it]*prefs[p2][it] for it in si])
	# Calculate Pearson score
	num=pSum-(sum1*sum2/n)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0: return 0
	r=num/den
	return r

def sim_distance_euclidean(prefs,person1,person2):
	# Get the list of shared_items
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1
	# if they have no ratings in common, return 0
	if len(si)==0: return 0
	# Add up the squares of all the differences
	sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
	for item in prefs[person1] if item in prefs[person2]])
	return 1/(1+sum_of_squares)
	
# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=3,similarity=sim_distance_pearson):
	scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]
	# Sort the list so the highest scores appear at the top
	scores.sort( )
	scores.reverse( )
	return scores[0:n]
	
def getRecommendations(prefs,person,similarity=sim_distance_pearson):
	totals={}
	simSums={}
	for other in prefs:
		# don't compare me to myself
		if other==person: continue
		sim=similarity(prefs,person,other)
		# ignore scores of zero or lower
		if sim<=0: continue
		for item in prefs[other]:
			# only score music items I haven't seen yet
			if item not in prefs[person] or prefs[person][item]==0:
				# Similarity * Score
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				# Sum of similarities
				simSums.setdefault(item,0)
				simSums[item]+=sim
	# Create the normalized list
	rankings=[(total/simSums[item],item) for item,total in totals.items( )]
	# Return the sorted list
	rankings.sort( )
	rankings.reverse( )
	return rankings
