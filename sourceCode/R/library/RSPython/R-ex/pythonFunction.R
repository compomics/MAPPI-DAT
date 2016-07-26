###--- >>> `pythonFunction' <<<----- Python Method Information

	## alias	 help(pythonFunction)

##___ Examples ___:

 pythonFunction("call", module="RS")

 els <- pythonModuleTypes("RS")
 RS.functionNames <- names(els[els == "function"])
 RS.functionDescriptions <- lapply(RS.functionNames, function(x) pythonFunction(x, module="RS"))
 names(RS.functionDescriptions) <- RS.functionNames

 # Just get the documentation string.
 RS.docs <- lapply(RS.functionNames, function(x) pythonFunction(x, module="RS")[["doc"]])
 names(RS.docs) <- RS.functionNames

## Keywords: 'Inter-system Interface', 'Python'.


