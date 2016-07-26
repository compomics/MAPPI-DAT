## checker helper
.checkMatrix <- function(res){
  checkTrue(class(res)=="matrix")
  checkTrue(nrow(res) > 0)
  checkTrue(ncol(res) > 0)
}

.checkSquareMatrix <- function(res){
  checkTrue(class(res)=="matrix")
  checkTrue(nrow(res) > 0)
  checkTrue(nrow(res) == ncol(res))
}

test_computeRecommendation  <- function(){
  A <- matrix(runif(10*10), nrow=10, ncol=10)
  A[A >  0.5] = 1
  A[A <= 0.5] = 0
  
  t1 <- computeRecommendation(A)
  .checkSquareMatrix(t1)
  
  S  <- matrix(runif(10*10), nrow=10, ncol=10)
  S1 <- matrix(runif(10*10), nrow=10, ncol=10)
  t2 <- computeRecommendation(A, S=S, S1=S1)
  .checkSquareMatrix(t2)
  
  t3 <- computeRecommendation(cbind(A,A))
  .checkMatrix(t3)
}


