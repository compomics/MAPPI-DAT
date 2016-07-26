###--- >>> `importPythonModule' <<<----- Loads a Python Module

	## alias	 help(importPythonModule)

##___ Examples ___:

  importPythonModule("sys")
  .PythonEval("version")

  importPythonModule("sys", all=F)
  .PythonEval("sys.version")

##Don't run: 
##D   importPythonModule("urllib", all=F)
##D   pythonModuleTypes("urllib")


## Keywords: 'Inter-system Interface', 'Python'.


