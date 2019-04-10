def setName(name):
    print(name)

try:
    setName("Yasmani")
    setName("Juan")
    params=["No se puede iniciar WF debido que fue previamente ejecutado"]
    errorkey = "error_exception"
    errorgroup = "U_SR"
    error = True
except (Exception), e:
    print(e)