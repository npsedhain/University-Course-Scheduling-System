from ortools.linear_solver import pywraplp

def main():

	solver = pywraplp.Solver('SolveAssignmentProblemMIP',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)


	instructor_count=3
	course_count=3
	classroom_count=2
	days_count=2

	i=range(1,instructor_count+1)
	j=range(1,course_count+1)
	k=range(1,classroom_count+1)
	t=range(1,days_count+1)
	h=range(1,4)
	p=range(1,4)

	#The utility of instructor i teaching course j : 3 instructors, 3 courses
	utility1=[[0,1,1],[1,0,1],[1,1,0]]

	#The utility of instructor i in day t : 3 instructors, 2 days
	utility2=[[1,1],[1,1],[1,1]]

	#The utility of course j in day t : 3 courses, 2 days
	utility3=[[1,1],[1,1],[1,1]]


	#The utility of course j with class p: 3 different classes 3 courses
	utility4=[[0,1,1],[1,0,1],[1,1,0]]






	#The following code creates binary integer variables for the problem. 
	X={}

	for instructor in i:
		for course in j:
			for day in t:
				for classroom in k:
					for time in h:
						for classes in p:
							X[instructor,course,day,classroom,time,classes]=solver.BoolVar('x[%i,%i,%i,%i,%i,%i]' % (instructor,course,day,classroom,time,classes))



	Y={}

	for instructor in i:
		for day in t:
			Y[instructor,day] = solver.BoolVar('x[%i,%i]' % (instructor,day))




    #creating the objective function

	solver.Maximize(solver.Sum([utility1[instructor-1][course-1]*X[instructor,course,day,classroom,time,classes] 
		for instructor in i for course in j for day in t for classroom in k for time in h for classes in p]
		)+solver.Sum([utility3[course-1][day-1]*X[instructor,course,day,classroom,time,classes] 
		for instructor in i for course in j for day in t for classroom in k for time in h for classes in p])+
		solver.Sum([utility4[course-1][classes-1]*X[instructor,course,day,classroom,time,classes] 
		for instructor in i for course in j for day in t for classroom in k for time in h for classes in p])+
		solver.Sum([utility2[instructor-1][day-1]*Y[instructor,day] for instructor in i for day in t]))


    #constraint no.1 : assures that each course is taught
	for course in j:
		solver.Add(solver.Sum([X[instructor,course,day,classroom,time,classes] for instructor in i for day in t for classroom in k for time in h for classes in p]) >= 1)

    #constraint no.4 :prevents from cross assignment, that is, at most one course can be presented in each classroom at a time.
	
	for instructor in i:
		for course in j:
			solver.Add(solver.Sum([X[instructor,course,day,classroom,time,classes] for day in t for classroom in k for time in h for classes in p])<=1)

	
	#constraint n0. 2 : specifies days an instructor has courses to teach
	for instructor in i:
		for day in t:
			for time in h:
				solver.Add(solver.Sum([X[instructor,course,day,classroom,time,classes] for course in j for classroom in k for classes in p])<=Y[instructor,day])

	#constraint n0. 3 : ensures instructors are invited on days they prefer
	for instructor in i:
		for day in t:
			solver.Add(Y[instructor,day]<=utility2[instructor-1][day-1])

			'''
	#constraint no. 5 :is to make sure that each instructor is assigned to courses of expertise.
	for instructor in i:
		for course in j:
			solver.Add(solver.Sum([X[instructor,course,day,classroom,time,classes] for classroom in k for time in h for day in t for classes in p])== utility1[instructor-1][course-1])
			'''

	#constraint no 6 : to make sure every class gets the subject they want
	
	for course in j:
		for classes in p:
			solver.Add(solver.Sum([X[instructor,course,day,classroom,time,classes] for instructor in i for classroom in k for time in h for day in t ])== utility4[course-1][classes-1])
	


	



	sol = solver.Solve()

	print('Total cost = ', solver.Objective().Value())
	print()
	for classes in p:
		print ("For class ",classes) 
		for instructor in i:
			for course in j:
				for day in t:
					for classroom in k:
						for time in h:
							if X[instructor,course,day,classroom,time,classes].solution_value() > 0:
								print('Teacher %d assigned to course %d on day %d on classroom %d in time %d.  ' 
									% (instructor,course,day,classroom,time))

	print()
	print("Time = ", solver.WallTime(), " milliseconds")




main()
