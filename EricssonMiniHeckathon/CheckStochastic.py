#this program checks if input vector and matrix are stochastic
#if the are not stochastic, then it will return ValueError
#If they are stochastic, then it will return the product of vector and matrix
#A left stochastic matrix is a real square matrix, with each column summing to 1 
#and the elements are non-negative
#A stochastic vector is a vector with non-negative entries that add up to one 

#function to check if the vector contains any negative values
#if it contains any negative value, it will return False
def checkPositive(row):
    if all(row > 0):
        return True
    else:
        return False

   

#the below function checks whether the vector and matrix are stochastic
#if they are not, it will return ValueError
#First check is, if all the elements are positive
#second check is, if for vector, sum of the elements is 1 and
#                 for matrix, sum of each column is 1
def is_stochastic_vector(vec1, mat1):
    #check if all the values of both the arrays are positive
    #check if the vector contains negative values
    checkPositive_vector = checkPositive(vec1)
    if (checkPositive_vector!=True):
        print("The vector contains negative values and returned Error")
        retError= "ValueError"
        return retError
    else:
        print("All the elements of the vector is positive")
    
    #check if the matrix contains any negative values
    checkPositive_matrix = True
    
    for i in range(len(mat1)):
        checkPositive_matrix = checkPositive(mat1[i])
        if (checkPositive_matrix != True):
            break;
    
    if (checkPositive_matrix!=True):
        print("The matrix contains negative values and returned Error")
        retError= "ValueError"
        return retError
    else:
        print("All the elements of the matrix is positive")
        
    #check if sum of the vector elements is 1
    vect_sum = np.sum(vec1)
    print("Sum of Vector Elemenents is:")
    print(vect_sum)
    if (vect_sum !=1):
        print("Error returned from vector sum condition")
        retError= "ValueError"
        return retError
    
    #check if sum of each column is 1
    mat_sum_col = np.sum(mat1, axis = 0)#sum of columns
    print("sum of each column of the matrix is:")
    print(mat_sum_col)

    #iterate through each row of the matrix
    for i in range(len(mat_sum_col)):
        #print(mat_sum_col[i])
        if (mat_sum_col[i] != 1):
            print("Error returned from matrix sum condition")
            retError= "ValueError"
            return retError


# Driver code      
if __name__ == "__main__" : 
    import numpy as np

    #vec1 = np.array([0.2,-0.8])#non-stochastic example
    vec1 = np.array([0.2,0.8])#stochastic example
    #mat1 = np.array([[0.2,0.3],[-0.2,0.3]])#non-stochastic example
    mat1 = np.array([[0.2,0.3],[0.8,0.7]])#stochastic example
    #call the function to check if the vector and matrix are stochastic
    retError = is_stochastic_vector(vec1, mat1)
    
    if (retError != "ValueError"):
        print("The vector and matrix are stochastic and product of matrix and vector is:")
        print(vec1.dot(mat1))
    else:
        print("The vector/matrix is not stochastic: " + retError)
    
  
    