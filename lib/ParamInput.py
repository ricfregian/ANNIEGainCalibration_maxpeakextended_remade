
def GetInitialParameters(fittype):
    initial_params = []
    if fittype in ["Gauss2","Gauss3"]:
        initial_params.append(input("1PE amplitude: "))
        initial_params.append(input("1PE mean: "))
        initial_params.append(input("1 PE sigma: "))
        initial_params.append(input("2PE amplitude scale factor: "))
        initial_params.append(input("2PE mean scale factor: "))
        initial_params.append(input("2PE sigma scale factor: "))
    else:
        print("Fit type not recognized for inputting initial parameters!")
    return initial_params
