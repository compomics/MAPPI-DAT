\name{PythonReference Element Access}
\alias{$.PythonReference}
\title{Syntactic convenience for calling a Python references's method}
\description{
This allows one to call a method of a Python object
from R in a simple form such as \code{pyObj$method(arg1, arg2, ...)}.
This provides an overloading of the \code{$} operator
for R objects of class \code{PythonReference} to return
a simplified call to \code{.PythonMethod}
}
\usage{
$.PythonReference(obj, name)
}
\arguments{
  \item{obj}{the \code{PythonReference} object whose method is to be called.}
  \item{name}{the name of the method in the Python object which is to be called.}
}
\details{
 When calling a Python object's method from R, one specifies the
reference to the Python object and the name of the method along with
the arguments to that method in a call to \code{\link{.PythonMethod}}. 
This function/method returns  function object containing sufficient
information to call the specified method on the given reference.
These two pieces of information are stored in an R closure instance
and this can then be called as a regular function whose
body calls \code{\link{.PythonMethod}}.
}
\value{
 A function closure instance whose body consists
of a call to \code{.PythonMethod} for the 
specified \code{PythonReference} object
and method name. 
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{
\code{\link{.PythonMethod}}
\code{\link{.Python}}
\code{\link{.PythonNew}}
\code{\link{.PythonEval}}
\code{\link{.PythonEvalFile}}
}

\examples{
 x <- .PythonNew("") 
 x$foo()

\dontrun{

}
}
\keyword{Inter-system Interface}
\keyword{Python}

\name{[[.PythonReference}
\alias{[[.PythonReference}
%- Also NEED an `\alias' for EACH other topic documented here.
\title{ ~~function to do ... ~~ }
\description{
  ~~ A concise (1-5 lines) description of what the function does. ~~
}
\usage{
[[.PythonReference(x, i, ..., .convert=T)
}
%- maybe also `usage' for other objects documented here.
\arguments{
  \item{x}{the \code{PythonReference} object in which to find the field
named \code{name}.}
  \item{i}{a character vector specifiying the name of the field to retrieve.}
  \item{\dots}{ignored, but present for compatability with the generic.}
  \item{.convert}{a logical value indicating whether to attempt to
     convert the resulting Python object to R (TRUE) or leave as a reference (FALSE)}
}

\value{
 The value of the Python field
 named \code{name} in the specified object,
 converted to an R object or exported to
 R as a reference to the Python object.
}

\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\note{
One can get the names of the different
fields that are accessible in a Python reference
\code{x} using the command
\code{x[["__dict__", .convert=F]]$keys()}
}

\seealso{
\code{\link{$.PythonReference}}
}

\examples{
\dontrun{
  p <- .PythonNew("SDefsParser", "foo.defs", .module="Sgenerate")
  p[["functions"]]


  p[["__dict__", .convert=F]]$keys()
}
}
\keyword{ ~kwd1 }% at least one, from doc/KEYWORDS
\keyword{ ~kwd2 }% __ONLY ONE__ keyword per line
\name{.Python}
\alias{.Python}
\alias{.PythonMethod}
\title{Invoke a Python function or instance method}
\description{
 These are the functions that invoke a Python function
or a method of a Python object.
They transfer the S arguments to their corresponding
Python values and invoke the identified function object.
The resulting Python value is transferred back as an 
S object using the default converters.
}
\usage{
.Python(func, ..., .module=NULL, .convert=T, .sig=NULL)
.PythonMethod(ref, method, ..., .convert=T, .sig=NULL)
}
\arguments{
  \item{func}{usually, a string specifying the name of the Python function to invoke.
This can also be a \code{PythonReference} object which refers to a previously
``computed'' function object.}
  \item{ref}{The Python object whose instance method is to be invoked. This is the 
\code{self} object in Python terms.}
  \item{method}{the name of the instance method to be invoked.}
  \item{\dots}{the arguments to the Python function or method, given as S objects
and converted to Python using the default converters.}
  \item{.module}{the name of the module in which to find to find and resolve the
 Python function}
  \item{.convert}{a logical value indicating whether an attempt to convert 
the result from the Python function or method to a regular R value
should be made, or whether the object should be left on the Python side of
the interface and a reference to it returned. Avoiding conversion can be useful
when the value will be used in subsequent calls Python functions or methods.}
  \item{.sig}{}
}
\details{
 These functions use the standard conversion mechanism for
translating R objects to Python values and vice versa.
These can be augmented by 
}
\value{
 The return value resulting from calling the Python function
or method. This is converted to an R object or 
returned as a reference  to the Python object
in the form of an object \code{PythonReference}.
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{ 
\code{\link{.PythonEval}}
\code{\link{.PythonEvalFile}}
\code{\link[RSPerl]{.Perl}}
\code{\link[SJava]{.Java}}
\code{\link[CORBA]{.CORBA}}
}

\examples{
 .Python("version", .module="sys")
 .Python("path", .module="sys")
}
\keyword{Inter-system Interface}
\keyword{Python}
\name{.PythonEvalFile}
\alias{.PythonEvalFile}
\alias{.PythonEval}
\title{Evaluate a Python script from a string or file.}
\description{
 These two functions allow one to evaluate Python scripts
which are given in the Python syntax. These can be specified
as a string or as a file containing the Python code.
This approach to evaluating Python commands is less
flexible than those offered by \code{\link{.Python}}
and related functions.
}
\usage{
.PythonEvalFile(cmd, ..., .module=NULL, .convert=T)
.PythonEval(cmd, ..., .module=NULL, .convert=T)
}
\arguments{
  \item{cmd}{the Python expression to parse and evaluate.}
  \item{\dots}{Any number of name-value pairs that are converted to a Python
  dictionary or context which will be used when evaluating the expression. }
  \item{.module}{the name of the module whose dictionary is used to provide the name
  space for resolving symbols in the Python expressions.}
  \item{.convert}{a logical value indicating whether the result of evaluating the Python
object should be converted to a regular R object, if possible, or explicitly left
within Python and returned as a \code{PythonReference} object.}
}
\details{

}
\value{
  The value returned from evaluating the Python expression(s),
converted to R using the standard conversion mechanism, including
any user-level converters currently registered.
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{
\code{\link{.Python}}
\code{\link{.PythonMethod}}
\code{\link{.PythonNew}}
}

\examples{
 .PythonEval("from sys import *")
 .PythonEval("argv")
}
\keyword{Inter-system Interface}
\keyword{Python}

\name{.PythonInit}
\alias{.PythonInit}
\alias{.PythonTerminate}
\title{Initialize the Python interpreter.}
\description{
 These functions allow one to initializes the Python engine and creates an interpreter
 and also to discard it and its contents.
 The \code{.PythonInit} function  must be called before invoking a Python function or method.
 One can start, stop and restart the Python interpreter any number of times.
}
\usage{
.PythonInit(path=NULL, merge=T)
.PythonTerminate()
}
\argumens{
 \item{path}{if specified, this should be a string specifying the directories
 in which to find Python modules. The directory names should be separated by the appropriate
 directory separator (":" on Unix). If this is missing, the current value fo 
 the \code{PYTHONPATH} environment variable is used.}
 \item{merge}{a logical value indicating whether the basic elements needed
 to locate the Python modules used to implement this package should be appended
 to the value of the system variable \code{PYTHONPATH}}
}
\details{
 \code{.PythonInit} passes its arguments
to \code{\link{.PythonPath}} to determine the
appropriate value for the \code{PYTHONPATH} environment
variable. It then uses the returned value to set
this environment variable and then initializes the python
interpreter.
}
\value{
 NULL or an error occurs.
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}
\Note{Very bad things will happen if you stop the interpreter and then access a
Python object, function, method, etc. Python will terminate.}

\seealso{\code{\link{.PythonPath}}}
\examples{
\dontrun{
  .PythonInit()
}
}
\keyword{Inter-system Interface}
\keyword{Python}

\name{.PythonNew}
\alias{.PythonNew}
\title{Create an instance of a Python class}
\description{
 This function creates an instance of a Python class.
Generally, this returns a reference to that object
so that it can be used in subsequent Python calls 
from R.
}
\usage{
.PythonNew(className, ..., .module=NULL, .convert=F)
}
\arguments{
  \item{className}{the name of the class of which an  new instance is to be created}
  \item{\dots}{any arguments to the \code{\_\_init\_\_} method of the class, including
   named arguments}
  \item{.module}{the ``name'' of the module in which the class is defined. This is
  usually a single string, but for nested modules is a character vector whose elements
  are in the top-level to sub-module order; e.g. if a class C is defined in the module B
  which is in A (i.e. A.B.C in Python terms), the \code{.module} is given as
   \code{c("A","B")}}
  \item{.convert}{a logical value indicating whether to attempt to convert the newly created object
    or not. This is usually only \code{FALSE} when creating the object has a useful side-effect.}
}
\value{
 If \code{.convert} is \code{FALSE}, a reference to the 
 newly created object is returned. This is an object of
 class \code{}. Otherwise, an attempt to convert the newly created
 object using the built-in and the current user-specified converters
 is performed. The result depends on what these return. If no converter
 is found, a reference to the newly created object is  returned, just
  as if \code{.convert} was specified as \code{FALSE}.
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{
\code{\link{.PythonMethod}}
\code{\link{.Python}}
}

\examples{
u <- .PythonNew("urlopen", "http://www.omegahat.org/index.html", .module="urllib")
.PythonMethod(u, "geturl")  
txt <- u$read()
u$geturl()
u$close()
}
\keyword{Inter-system Interface}
\keyword{Python}

\name{.PythonPath}
\alias{.PythonPath}
\title{Create Python Load Path}
\description{
 This function handles creating a suitable value for
the \code{PYTHONPATH} environment variable which controls
how the Python interpreter finds its modules.
}
\usage{
.PythonPath(path=NULL, merge=T)
}
\arguments{
 \item{path}{if specified, this should be a string specifying the directories
 in which to find Python modules. The directory names should be separated by the appropriate
 directory separator (":" on Unix). If this is missing, the current value fo 
 the \code{PYTHONPATH} environment variable is used.}
 \item{merge}{a logical value indicating whether the basic elements needed
 to locate the Python modules used to implement this package should be appended
 to the value of the system variable \code{PYTHONPATH}}
}
\details{
The following is the algorithm used to determine the
path.
 If there is no PYTHONPATH set, then we set our version so that
 one can find the RS modules.

 If there is a PYTHONPATH already set, then we take it and append
 our value to it. This can be inhibited by specifying `merge = F'

 Finally, if there is a non-null value for the path argument, then 
 we use that as the value for PYTHONPATH. Again, if merge = T, we 
 append the RS directories to it.

 If merge is T, then we take whatever value for path is given
 and append it to the current value of PYTHONPATH
}
\value{
 A string (i.e. character vector of length 1) giving the 
appropriate setting for the \code{PYTHONPATH} environment variable.
}

\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{\code{\link{.PythonInit}}

\examples{
 .PythonPath(system.file("tests", pkg="RSPython"))

 .PythonPath(c(.PythonPath(), system.file("tests", pkg="RSPython")))

\dontrun{
 .PythonInit(system.file("tests", pkg="RSPython"))
}
}
\keyword{Inter-system Interface}
\keyword{Python}\name{Python Reflectance}
\alias{pythonMethods}
\alias{getSuperClasses}
\alias{pythonModuleNames}
\title{Information about Python classes and methods}
\description{
  These functions return information about a python class
  and its methods. From this we 
}
\usage{
pythonMethods(obj, all=F)
getSuperClasses(obj, all=F)
pythonModuleNames(obj, all=F)
}
%- maybe also `usage' for other objects documented here.
\arguments{
  \item{obj}{a character vector giving the name of a Python class,
   given in the form \code{c("className", "moduleName")}}
  \item{all}{controls how inherited methods and attributes are
    processed. If \code{TRUE} is specified, the inherited methods are
    also reported. Otherwise, these are ignored and only those methods
    defined within the class are returned.}
}
\details{
 This uses the code 
}
\value{

}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\Note{This will be implemented differently in the future
and will make use of the Signature module for Python}
\seealso{}

\examples{

}
\keyword{Inter-system Interface}
\keyword{Python}

\name{foreignReference}
\alias{foreignReference}
\title{Creates a reference for an S object}
\description{
 This function creates a reference from an S object and optionally
registers it with the foreign reference manager.  This reference can
then be used to identify the S object  in a foreign
system, passing it as either an argument in a function call
to that foreign system or as the result of a call to an
S function from that system.
The reference can be given additional information
such as a name by which to identify it, one or more
target classes in the foreign system that it should 
masquerade as.
}
\usage{
foreignReference(obj, id=NULL, className=NULL, targetClasses=NULL, register=T)
}
\arguments{
  \item{obj}{the S object which the new reference is to identify}
  \item{id}{an optional name to use to identify this reference and value.
This should be unique and if omitted will be generated by the reference manager
so that it is unique. It can be specified here to provide a convenient way to 
refer to an object and also to simplify garbage collection.}
  \item{className}{?}
  \item{targetClasses}{the names of any classes in the foreign system 
that this reference should ``implement'' when it is instantiated in this system.
This is a way of controlling the conversion of the reference to an object
in the foreign system.}
  \item{register}{a logical value indicating whether the reference
  and object should be registered with the current foreign reference manager. }
}
\value{
An object of class 
\code{NamedRReference} or
\code{AnonymousRReference} depending on whether
\code{id} is specified or not.
The object contains the following fields
  \item{id}{the name for the reference}
  \item{value}{the object or value (\code{obj} in the call) associated with this reference}
  \item{className}{}
  \item{targetClasses}{the value of \code{targetClasses} in the call}
  \item{type}{the type of the object being referenced, computed by \code{\link{typeof}}}
  \item{classes}{the class(es) of the object being referenced, computed by \code{\link{class}}}
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{
\code{\link{referenceManager}}
\code{\link{.Python}}
\code{\link{.PythonNew}}
\code{\link{.PythonMethod}}
}

\examples{
}
\keyword{Inter-system Interface}
\keyword{Python}

\name{getNumPythonConverters}
\alias{getNumPythonConverters}
\alias{getPythonConverterDescriptions}
\title{Query the currently registered object converters between R and Python.}
\description{
 These functions allow the user to examine what C routines
and R and Python functions are currently registered
to implement the conversion between R and Python objects.
These control how values in one system are converted
to objects in the other system as they are transferred
as arguments to functions in the foreign system
and returned as results to the calling system.
These functions give both the number 
and descriptions of each of the converters registered
in either direction (i.e., from R to Python and vice-versa.)
The descriptions are usually specified by the registrant when the converters are
registered.
}
\usage{
getNumPythonConverters(which=c(fromPython = F, toPython = T))
getPythonConverterDescriptions(which=c(fromPython = F, toPython = T))
}
\arguments{
  \item{which}{the direction(s) of the conversion of interest, i.e. 
 from Python to R and/or from R to Python}
}
\details{
 Converters are registered at the C level as pairs
of C routines given by a matching routine that determines
whether the converter is appropriate for the object to be converted
and the  converter routine itself which performs the translation from one
system to the other. Additionally, 
}
\value{
 \code{getNumPythonConverters} returns an integer vector
giving the number of converters in the list for each of
the specified directions.
 \code{getPythonConverterDescriptions} returns a list
with an element for each of the directions specified.
Each element in this list is a character vector 
containing the description string for each of the 
different (match, converter) pairs.
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{
\code{\link{.Python}}
\code{\link{.PythonNew}}
\code{\link{.PythonMethod}}
}

\examples{
}
\keyword{Inter-system Interface}
\keyword{Python}

\name{getPythonReferenceIDs}
\alias{getPythonReferenceIDs}
\title{Python Foreign Reference Information}
\description{
This returns the names of the currently active
foreign Python reference objects being managed by 
the Python reference manager.
}
\usage{
getPythonReferenceIDs()
}
\details{
This probes the reference manager in which the 
exported Python objects are actually stored
and gets information about each element.
}
\value{
  A character vector giving the identifiers (i.e. names) of
the currently active foreign references exported from the Python
session.
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{\code{\link{.Python}},
\code{\link{.PythonNew}}
}

\examples{
\dontrun{
  before <- getPythonReferenceIDs()
   # do something that creates Python reference objects
  after <-  getPythonReferenceIDs()
   # Now cleanup the new ones.
}
}
\keyword{Inter-system Interface}
\keyword{Python}

\name{importPythonModule}
\alias{importPythonModule}
\title{Loads a Python Module}
\description{
 This loads the Python module into the Python interpreter,
 making its functions and classes available to the Python, and hence R,
 session. This is equivalent to the Python command
 \code{from <name> import *}. 
}
\usage{
importPythonModule(name, all=T)
}
\arguments{
  \item{name}{}
  \item{all}{}
}
\value{

}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{
\code{\link{pythonModuleTypes}}
}

\examples{
  importPythonModule("sys")
  .PythonEval("version")

  importPythonModule("sys", all=F)
  .PythonEval("sys.version")

\dontrun{
  importPythonModule("urllib", all=F)
  pythonModuleTypes("urllib")
}
}
\keyword{Inter-system Interface}
\keyword{Python}\name{isPythonInitialized}
\alias{isPythonInitialized}
\title{Is Python Interpreter Initialized}
\description{
 This function tests whether the Python interpreter is in an initialized state
and optionally initializes it if it is not (using default settings).
}
\usage{
isPythonInitialized(init=F)
}
\arguments{
  \item{init}{a logical value indicating whether to perform the default initialization
 if the Python interpreter is not already initialized.
  }
}
\details{
 This checks the internal state of the Python library and queries if the
interpreter is already initialized. If not and \code{init} is \code{TRUE},
the function \code{\link{.PythonInit}} is called with no arguments.
}
\value{
 A logical value indicating what the current status of the Python interpreter
is. If \code{init} is \code{FALSE}, this is the state before the call.
Otherwise, the interpreter should have been started, except if an error occurs.
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{\code{\link{.PythonInit}}

\examples{
 isPythonInitialized(init)

 if(isPythonInitialized())
}
\keyword{Inter-system Interface}
\keyword{Python}\name{pythonFunction}
\alias{pythonFunction}
\title{Python Method Information}
\description{
This returns information describing a Python
method or function within a Python module.
It gives reflectance information allowing one to determine
the number and types of arguments, which are keywords, 
and what the default values are, if any.
Additionally, this returns the documentation string of the object.
}
\usage{
pythonFunction(obj, module=NULL)
}
\arguments{
  \item{obj}{the name of the function or method being queried}
  \item{module}{the name of the module in which the function/method is to be found. This can be
 a character vector of one or more names identifying the module.}
}
\details{

}
\value{
An object of classes
\code{Function} and  \code{PythonReference}.
It contains
  \item{name}{Description of `comp1'}
  \item{code}{a description of the function definition (i.e. ``signature'' and body)
       giving the names of the arguments and giving a count of how many local and external
       values 
   }
  \item{defaults}{a list of the default values of the different arguments. This is a named list
  whose names correspond to the argument names.}
  \item{doc}{the documentation string associated with the Python function/method}
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{
 \code{\link{pythonModuleTypes}}
}

\examples{
 pythonFunction("call", module="RS")

 els <- pythonModuleTypes("RS")
 RS.functionNames <- names(els[els == "function"])
 RS.functionDescriptions <- lapply(RS.functionNames, function(x) pythonFunction(x, module="RS"))
 names(RS.functionDescriptions) <- RS.functionNames

 # Just get the documentation string.
 RS.docs <- lapply(RS.functionNames, function(x) pythonFunction(x, module="RS")[["doc"]])
 names(RS.docs) <- RS.functionNames
}
\keyword{Inter-system Interface}
\keyword{Python}

\name{pythonModuleTypes}
\alias{pythonModuleTypes}
\title{Python Module Elements and Types}
\description{
 This function provides reflective information about the
 contents of a module by returning a list of all the
 entries in that module and the type of object it (currently) is.
 This allows one to differentiate the functions or methods
 and the fields of a module  and to understand what the fields
 contain.
 Essentially it describes the elements of the module's dictionary
 (\code{\_\_dict\_\_})
}
\usage{
pythonModuleTypes(name)
}
\arguments{
  \item{name}{the name of the module in question. This is given as a single string or
a character vector containg the hierarchy of module names in a top-down or top-first form.}
}
\details{
 
}
\value{
 A named character/string vector whose name-value pairs
 give the name of each  entry in the module and its type.
 The types are 
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{
}

\examples{
 pythonModuleTypes("sys")
 pythonModuleTypes("RS")
}
\keyword{Inter-system Interface}
\keyword{Python}
\name{referenceManager}
\alias{referenceManager}
\title{Create instance of the standard Reference Manager}
\description{

}
\usage{
referenceManager()
}

\details{
 If no reference manager is available when it is first needed
by a call from Python to R, this function is called to create
a \code{referenceManager} instance and is then registered
at the C level.
}
\value{
 A closure that stores R objects and returns
references to them. The closure provides a variety of different
functions to operate on these R objects:
  \item{handler}{}
  \item{createReference}{}
  \item{addReference}{}
  \item{remove}{}
  \item{getReference}{}
  \item{references}{}
  \item{total}{}
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}


\seealso{
\code{\link{setPythonHandler}}
\code{\link{getPythonHandler}}
}

\examples{

}
\keyword{Inter-system Interface}
\keyword{Python}

\name{setPythonHandler}
\alias{setPythonHandler}
\alias{getPythonHandler}
\title{Get or set the R to Python foreign reference handler.}
\description{
The R-Python reference manager/handler is responsible for caching and
resolving R objects that are exported to Python as references to R
objects. The manager accepts these R objects and stores them with a
given unique name, and returns an object that identifies it. When the
object is used in Python, the reference is passed back to R and
resolved by this handler.  This handler is implemented as a collection
of basic R functions with different functions handling the storing and
resolving of references, calling functions on that reference.  Usually
this is a closure that shares access to the pool of objects being
exported.  These two functions allow one to get the currently
registered handler and also to set the handler.
}
\usage{
setPythonHandler(handler)
getPythonHandler(handler)
}
\arguments{
  \item{handler}{the handler to be registered as the active one.}
}
\details{
Currently, the form of the handler is quite restricted.
It should be a list with the same length and functions 
in the same order as those in the default handler
returned by \code{\link{referenceManager}}}.
}
\value{
 Both functions return the reference handler that was registered
before the function was called. In the case of the
\code{setPythonHandler}, this is the value that is being replaced.
}
\references{\url{http://www.omegahat.org/RSPython},
\url{http://www.python.org}}
\author{Duncan Temple Lang}

\seealso{
\code{\link{referenceManager}}
}

\examples{

}
\keyword{Inter-system Interface}
\keyword{Python}

