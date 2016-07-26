###--- >>> `.PythonNew' <<<----- Create an instance of a Python class

	## alias	 help(.PythonNew)

##___ Examples ___:

u <- .PythonNew("urlopen", "http://www.omegahat.org/index.html", .module="urllib")
.PythonMethod(u, "geturl")  
txt <- u$read()
u$geturl()
u$close()

## Keywords: 'Inter-system Interface', 'Python'.


