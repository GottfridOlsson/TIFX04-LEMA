#----------------------------------------------------------##
#        Name: TIFX04-22-82, parameters for used coils
#      Author: GOTTFRID OLSSON 
#     Created: 2022-04-25, 20:03
#     Updated: 2022-05-03, 11:18
#       About: Stores and formates data for each coil used
#              in the final design (XSP1, XSP2, ..., XSP5)
#              Prints code for table --> LaTeX
##---------------------------------------------------------##


## FUNCTIONS TO PRINT TABLE --> LATEX ##

def printTableDataLineAllCoils(parameterString, values, uncertainties_pm): #ad hoc, ONLY for use in this particular case!
    
    result = str(parameterString) #never trust user input :P
    also   = ' & '
    pm     = ' $\pm$ '
    newRow = ' \\\\ \\addlinespace' # "\\ \addlinespace" in Latex

    for i in range(len(values)):
        for j in range(2): # 2 coils per pair
            result += also + str(values[i][j]).replace('.', ',') + pm + str(uncertainties_pm[i][j]).replace('.', ',')

        if i == len(values)-1:
            result += newRow

    print(result)

#def printTableData(parameterStrings, r, r_pm, R, R_pm, d, d_pm, L_WireInCoil, L_WireInCoil_pm, L_coupled, L_coupled_pm, Ohm, OHm_pm, m, m_pm):
#
#    for i in range(len(parameterStrings)):
#        printTableDataLineAllCoils(parameterStrings[i], r, r_pm)
#    result = 1
#    return(result)

def printTableDataLineAllCoilsTranposed():

    return False

## VECTORS WITH DATA FROM LABLOGG ##
# coils are paired: XSPi with i = {1,2,3,4,5}
# every pair consists of two coils: N1 and N2 s.t. we have, i=4, XSP4N1 and XSP4N2

L_coupled    = [ 0, 0, 0, 0, 0 ] # [mH], inductance of one PAIR of coils when mounted on Tetrix-structure
L_coupled_pm = [ 0, 0, 0, 0, 0 ] # [mH], uncertainty plus-minus

L_wireInCoil    = [ [73.56, 73.52], [46.93, 46.93], [33.40, 33.4], [28.21, 28.18],  [23.86, 23.93] ]    # [m], wire in coil (excluding wire to connect to other things, i.e. the "legs")
L_wireInCoil_pm = [ [0.05, 0.05],   [0.05, 0.05],   [0.05, 0.05],  [0.05, 0.05],    [0.05, 0.05], ]     # [m], uncertainty plus-minus (estimated to 0.05 //2022-04-25)

t      = [ [21.0, 20.0],        [17.0, 17.0],   [14.0, 14.0],   [13.0, 13.5],       [12.5, 12.5] ]      # [mm], thickness d=t=R-r (theoretically)
t_pm   = [ [1, 0.5],            [0.4, 0.3],     [0.3, 0.5],     [0.5, 0.5],         [0.5, 0.5] ]        # [mm], uncertainty plus-minus

r      = [ [7.15, 7.25],        [7.25, 7.3],    [7.25, 7.25],   [7.25, 7.25],       [7.3, 7.25] ]       # [mm], inner radius
r_pm   = [ [0.1, 0.25],         [0.1, 0.1],     [0.25, 0.25],   [0.1, 0.1],         [0.15, 0.15] ]      # [mm], uncertainty plus-minus

R      = [ [24.5, 25.25],       [22.0, 22.0],   [21.0, 21.0],   [19.75, 19.9],      [19.5, 19.75] ]     # [mm], outer radius
R_pm   = [ [0.25, 0.3],         [0.25, 0.25],   [0.25, 0.25],   [0.25, 0.1],        [0.2, 0.25] ]       # [mm], uncertainty plus-minus

m      = [ [196.20, 195.67],    [126.8, 126.8], [86.6, 86.7],   [75.8, 75.8],       [64.8, 64.8] ]      # [g], mass (all wire and the 'gift string' used to hold the coil together)
m_pm   = [ [0.005, 0.005],      [0.05, 0.05],   [0.05, 0.05],   [0.05, 0.05],       [0.05, 0.05] ]      # [g], uncertainty plus-minus

Ohm    = [ [4.54, 4.54],        [2.90, 2.90],   [2.10, 2.10],   [1.84, 1.84],       [1.58, 1.60] ]      # [Ohm], resistance
Ohm_pm = [ [0.005, 0.005],      [0.05, 0.05],   [0.05, 0.05],   [0.005, 0.005],     [0.005, 0.005] ]    # [Ohm], uncertainty plus-minus

L      = [ [9.45, 9.54],        [4.63, 4.63],   [2.58, 2.64],   [1.969, 1.940],     [1.47, 1.50] ]      # [mH], inductance of ONE coil
L_pm   = [ [0.005, 0.005],      [0.005, 0.005], [0.005, 0.005], [0.0005, 0.0005],   [0.005, 0.005] ]    # [mH], uncertainty plus-minus


parameterStrings  = ["$\coilr$ (\si{\milli\meter})", "$\coilR$ (\si{\milli\meter})", "$\coild$ (\si{\milli\meter})", "$\wires$ (\si{\meter})", "$\genL$ (\si{\milli\henry})", "$\coilL$ (\si{\milli\henry})", "$\Omega$ ($\Omega$)", "$\projm$ (\si{\gram})"] #for table in Latex
coilNumberStrings = [ ["1A", "1B"], ["2A", "2B"], ["3A", "3B"], ["4A", "4B"], ["5A", "5B"] ]
matrixTransposed    = [r, R, t, L_wireInCoil, L, Ohm, m]
matrixTransposed_pm = [r_pm, R_pm, t_pm, L_wireInCoil_pm, L_pm, Ohm_pm, m_pm]
printTableDataLineAllCoils_bool = False
printTableDataLineAllCoilsTransposed_bool = True

if printTableDataLineAllCoils_bool:
    printTableDataLineAllCoils(parameterStrings[0], r, r_pm)
    printTableDataLineAllCoils(parameterStrings[1], R, R_pm)
    printTableDataLineAllCoils(parameterStrings[2], t, t_pm)
    printTableDataLineAllCoils(parameterStrings[3], L_wireInCoil, L_wireInCoil_pm)
    printTableDataLineAllCoils(parameterStrings[4], L, L_pm)

    printTableDataLineAllCoils(parameterStrings[6], Ohm, Ohm_pm)
    printTableDataLineAllCoils(parameterStrings[7], m, m_pm)



if printTableDataLineAllCoilsTransposed_bool:
   # print(matrixTransposed)
    also   = ' & '
    pm     = ' $\pm$ '
    newRow = ' \\\\ \\addlinespace' # "\\ \addlinespace" in Latex
    rowString = ""

    for i in range(len(coilNumberStrings)):
        rowString = ""
        for k in range(2):
            rowString = str(coilNumberStrings[i][k])

            for j in range(7):
                value    = matrixTransposed[j][i][k]
                value_pm = matrixTransposed_pm[j][i][k]
                
                if j in range(3,7): #remove uncertainty for: s, L, Ohm, m
                    rowString += str(also) + str(value).replace('.', ',')
                else:
                    rowString += str(also) + str(value).replace('.', ',') + str(pm) + str(value_pm).replace('.', ',')     
            rowString += str(newRow)
            print(str(rowString))
    
    quit()
