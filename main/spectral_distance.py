from matplotlib import pyplot as plt
import numpy as np

def stepFunction(y):
      return 1 if y >= 0 else 0

def laplacian(D, A):
      """Returns the Laplacian matrix which is the degree matrix 
      D for a graph minus the adjacency matrix A"""
      return D - A

def degreeMatrix(graph):
      """
      D - degree matrix
      N - neighbourhood of the current node
      """
      n = len(graph)
      D = np.zeros([n, n])
      for i, N in enumerate(graph.values()):
            D[i][i] = len(N)
      return D

def adjacencyMatrix(graph):
      """
      A - adjacency matrix
      """
      n = len(graph)
      A = np.zeros([n, n])
      list_of_nodes = list(graph.keys())
      for i, N in enumerate(graph.values()):
            for v in N:
                  j = list_of_nodes.index(v)
                  A[i][j] = 1
      return A

def sortDegAdjMatrices(D, A):
      for i in range(1, D[0].size):
            for j in range(i-1, -1, -1):
                  if max(D[j]) < max(D[j+1]):
                        # Permute D so that vertices are in degree order
                        # Swap columns
                        D[:,[j+1, j]] = D[:,[j, j+1]]  
                        # Swap rows
                        D[[j+1, j],:] = D[[j, j+1],:]  
                        # Permute A so that vertices are in degree order
                        A[:,[j+1, j]] = A[:,[j, j+1]]  
                        A[[j+1, j],:] = A[[j, j+1],:]  
      return D, A

def sortAndScaleEigenvalues(eigen_zip):
      """
      Sorts the eigenvalues and eigenvectors of the Laplacian, ensuring that lambda_n is zero.
      The eigenvectors are then scaled so that the eigenvector corresponding to lambda_n is
      a column vector of 1s.
      """
      for values, vectors in eigen_zip:
            for i in range(1, values.size):
                  for j in range(i-1, -1, -1):
                        if values[j] > values[j+1]:
                              values[j+1], values[j] = values[j], values[j+1]
                              vectors[:,[j+1,j]] = vectors[:,[j,j+1]]
            # Ensure that eigenvector for lambda_n is column of 1s
            vectors[:,:] = vectors / vectors[:,0]
            # Introduce arbitrary level of precision (important later)
            vectors[:,:] = vectors.round(6)
            # Scale each vector so that min value is 0 and max value is 1
            for vector in vectors.T:
                  for i, element in enumerate(vector):
                        if max(vector) != min(vector):
                              vector[i] = (element - min(vector))/(max(vector) - min(vector))
      return eigen_zip

def cdf(eigenvector, bins):
      varrho = []
      yhat = []
      for y in (j / bins for j in range(bins + 1)):
            varrho.append(sum([stepFunction(y - x) for x in eigenvector]) / len(eigenvector)) 
            yhat.append(y)
      return varrho 

def distanceVectors(eigenvector1, eigenvector2, bins):
      D1 = cdf(eigenvector1, bins)
      D2 = cdf(eigenvector2, bins)
      return sum([abs(d1-d2) / bins for d1, d2 in zip(D1, D2)])

def distanceFull(eigenvectors1, eigenvectors2, bins=100):
      M = min(eigenvectors1.shape[1], eigenvectors2.shape[1])
      dist = [distanceVectors(eigenvectors1[:,i], eigenvectors2[:,i], bins) for i in range(1, M)]
      return sum(dist) / (M - 1)

def distanceMatrix(H, bins):
      # Create list of degree and adjacency matrices for all graphs in H
      print("Generating degree matrices...")
      D = [degreeMatrix(h) for h in H]
      print("Generating adjacency matrices...")
      A = [adjacencyMatrix(h) for h in H]
      # Create some zipped list of the sorted degree and adjacency matrices
      print("Zipping and sorting matrices...")
      DAzip = [sortDegAdjMatrices(d, a) for d, a in zip(D, A)]
      # Create the list of Laplacian matrix for each pair of degree and adjacency matrices
      print("Creating Laplacians...")
      L = [laplacian(d, a) for d, a in DAzip]
      # Calculate eigenvalues and eigenvectors for each Laplacian matrix
      eigen_zip = [np.linalg.eig(l) for l in L]
      eigen_zip = sortAndScaleEigenvalues(eigen_zip)
      # Create matrix 
      n = len(eigen_zip)
      distanceMatrix = np.zeros((n,n))
      print("Calculating distance matrix...")
      for i in range(0, n):
            for j in range(0, n):
                  print(i,j)
                  if i <= j:
                        distanceMatrix[i][j] = distanceFull(eigen_zip[i][1], eigen_zip[j][1], bins)
                  if i > j:
                        distanceMatrix[i][j] = distanceMatrix[j][i]
      return distanceMatrix