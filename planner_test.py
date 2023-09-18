from subs.Factory import assemble

import time
import traceback






try:
    ep, prp, pop, asparagusProcessor, pather, viz, coms, camera, output, endEffector, planner = assemble(
        config_path='config.yaml')
    print('CLASSES LOADED')
    while True:


        data = {}
        coms._readSignalFromArm()
        camera.getData()
        image = camera.image
        image_data = prp.process(image)
        net_output = ep.process(image_data)
        boxes, masks, classid = pop.process(net_output)

        if len(classid) != 0:


            spears, data = asparagusProcessor.process(boxes, masks) #filtered on camera reach and camera distance

            _ = pather._calc_rob_pickofs(spears)
            spears = pather.filterHD(spears)  # height filter max reach filter

            a, target, sid = planner.process(spears)
            print(f' ANGLE: {a}')
            print(f' COMS:  {coms.ARM_IS_READY}')
            print(f' TARGET: {target}')
            if a is not None and coms.ARM_IS_READY:
                coms._sendCoordsAngle(target, a*-1)
                print(f'SENT: {target}    {a}')
                time.sleep(5)

        # output.Render(image, data)

except Exception as e:
    print(e)
    traceback.print_exc()
    ep.deinitialize()
finally:
    ep.deinitialize()

'''
try:
    while True:


        data = {}
        camera.getData()
        image = camera.image
        image_data = prp.process(image)
        net_output = ep.process(image_data)
        boxes, masks, classid = pop.process(net_output)

        if len(classid) != 0:


            spears, data = asparagusProcessor.process(boxes, masks)
            print(spears)




            if len(spears) != 0:
                image = viz.process(image, spears)

        output.Render(image, data)

except Exception as e:
    traceback.print_exc()
    ep.deinitialize()
finally:
    ep.deinitialize()

'''