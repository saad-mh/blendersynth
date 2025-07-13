import bpy, math, random, time
from mathutils import Euler, Color
from pathlib import Path

def randomRotate(obj):
    """
    Randomly rotate the subject passed on as obj.
    """
    randomRot = (0, 0, random.random() * 2 * math.pi)
    obj.rotation_euler = Euler(randomRot, 'XYZ')

def randomColor(mat):
    """
    Randomly allot a color to the material input as mat.
    """
    color = Color()
    hue = random.random()
    color.hsv = (hue, 1, 1)
    rgba = [color.r, color.g, color.b, 1]
    mat.node_tree.nodes['Principled BSDF'].inputs[0].default_value = rgba
    
def randomCamera():
    bpy.context.scene.objects['CameraContainer'].constraints['Follow Path'].offset = random.random() * 100                # randomly move the camera container which is a sphere path
    bpy.context.scene.objects['CirclePathContainer'].constraints['Follow Path'].offset = random.random() * -100           # randomly rotate the sphere path containter, which in itself is an oval-shaped path along an arc
    
cup =  'Mug'
cupObj = bpy.context.scene.objects[cup]

objRendersPerSplit = [('train', 10), ('val', 10), ('test', 5)]

outPath = 'C:/out/mug'               # output path, change accordingly

totalRenCount = sum([r[1] for r in objRendersPerSplit])


startIdx = 0
startTime = time.time()              # used to calculate time taken to render each picture

for split, renders in objRendersPerSplit:
    print(f'Split: {split}, total images: {totalRenCount}')
    print(f'Starting object: {split}')
    
    cupObj.hide_render = False
    
    for i in range(startIdx, startIdx + renders):
        randomRotate(cupObj)
        randomColor(bpy.context.scene.objects[cup].material_slots[0].material)
        randomCamera()
        print(f'Rendering {i + 1} of {totalRenCount}')
        timePerRender = (time.time() - startTime) / (i + 1)
        timeRemaining =  timePerRender * (totalRenCount - i - 1)
        print(f'ETA {time.strftime("%H:%M:%S", time.gmtime(timeRemaining))}')                                      # optional - shows ETA, particularly useful in low end devices.
        
        bpy.context.scene.render.filepath = str(f'{outPath}/{split}/{cup}/{str(i).zfill(3)}.png')                  # increase the parameter inside .zfill() if number of renders > 999
        bpy.ops.render.render(write_still = True)

    startIdx +=  renders
