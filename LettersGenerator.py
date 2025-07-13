import bpy, math, random, time
from mathutils import Euler, Color
from pathlib import Path

def randomRotate(obj):
    """ 
    Applies random rotation to given object obj
    """
    randRot = (random.random() * 2 * math.pi, random.random() * 2 * math.pi, random.random() * 2 * math.pi)
    
    bpy.context.scene.objects[obj].rotation_euler = Euler(randRot, 'XYZ')
    
def randomColor(mat):
    """
    Applies random color to given material mat.
    """
    color = Color()
    hue = random.random()
    color.hsv = (hue, 1, 1)
    rgba = [color.r, color.g, color.b, 1]
    mat.node_tree.nodes['Principled BSDF'].inputs[0].default_value = rgba


obj = ['A', 'B', 'C']
objRendersPerSplit = [('train', 500), ('val', 100), ('test', 20)]

outPath = 'C:/out/letters'          # output folder

totalRenCount = sum([len(obj) * r[1] for r in objRendersPerSplit])

for name in obj:
    bpy.context.scene.objects[name].hide_render = True

startIdx = 0

startTime = time.time()

for split, renders in objRendersPerSplit:
    print(f'Split: {split}, total images: {renders * len(obj)}')
    
    for ob in obj:
        print(f'Starting object: {split} - {ob}')
        
        obRender = bpy.context.scene.objects[ob]
        obRender.hide_render = False
        
        for i in range(startIdx, startIdx + renders):
            randomRotate(ob)
            randomColor(bpy.context.scene.objects[ob].material_slots[0].material)
            print(f'Rendering {i + 1} of {totalRenCount}')
            timePerRender = (time.time() - startTime) / (i + 1)
            timeRemaining =  timePerRender * (totalRenCount - i - 1)
            print(f'ETA {time.strftime("%H:%M:%S", time.gmtime(timeRemaining))}')
            
            bpy.context.scene.render.filepath = str(f'{outPath}/{split}/{ob}/{str(i).zfill(3)}.png')    # change .zfill() param if renders > 999
            bpy.ops.render.render(write_still = True)
        
        obRender.hide_render = True

        startIdx +=  renders
        
for name in obj:
    bpy.context.scene.objects[name].hide_render = False
