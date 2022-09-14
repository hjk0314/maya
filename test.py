import pymel.core as pm


# 79 char line ================================================================
# 72 docstring or comments line ========================================


# inputs
obj = 'pony2_wheel_Ft_L'
rad = 3

# =============================
cuv = 'cc_' + obj
jnt = cuv + '_jnt'
nullGrp = cuv + '_nullGrp'
prevGrp = obj + '_prevGrp'
nextGrp = obj + '_nextGrp'
orntGrp = obj + '_orntGrp'
exprString = f'''
float $R = {cuv}.Radius;
float $A = {cuv}.AutoRoll;
float $jntRotX = {jnt}.rotateX;
float $Round = 2 * 3.141 * $R;
float $orntGrpRotY = {orntGrp}.rotateY;
float $scale = 1;
float $prevPosX = {cuv}.PrevPosX;
float $prevPosY = {cuv}.PrevPosY;
float $prevPosZ = {cuv}.PrevPosZ;
{prevGrp}.translateX = $prevPosX;
{prevGrp}.translateY = $prevPosY;
{prevGrp}.translateZ = $prevPosZ;
float $nextPosX = {nextGrp}.translateX;
float $nextPosY = {nextGrp}.translateY;
float $nextPosZ = {nextGrp}.translateZ;
float $D = `mag<<$nextPosX - $prevPosX, $nextPosY - $prevPosY, $nextPosZ - $prevPosZ>>`;
{jnt}.rotateX = $jntRotX + (($D / $Round) * 360 * $A * 1 * sin(deg_to_rad($orntGrpRotY))) / $scale;
{cuv}.PrevPosX = $nextPosX;
{cuv}.PrevPosY = $nextPosY;
{cuv}.PrevPosZ = $nextPosZ;
'''
# print(obj)
# print(cuv)
# print(jnt)
# print(nullGrp)
# print(prevGrp)
# print(nextGrp)
# print(orntGrp)
# print(exprString)


# sel = pm.ls(sl=True)
# bbWheel = pm.xform(sel[0], q=True, boundingBox=True)
# xMin, yMin, zMin, xMax, yMax, zMax = bbWheel
# x = (xMin + xMax) / 2
# x = round(x, 3)
# y = (yMin + yMax) / 2
# y = round(y, 3)
# z = (zMin + zMax) / 2
# z = round(z, 3)
# wheelPivot = (x, y, z)
# print(wheelPivot)
cuv = pm.circle(
    n=cuv, # name
    c=(0,0,0), # center pivot
    nr=(1,0,0), # normal axis
    sw=360, # sweep angle
    r=(rad*1.1), # radius
    d=3, # degree
    ch=0, # create input channel
    s=8 # number of sections
)
jnt = pm.joint(n=jnt, p=(0,0,0))
nullGrp = pm.group(n=nullGrp, em=True, p=cuv[0])