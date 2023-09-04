from subs.Factory import assemble

import time
import traceback

ep, prp, pop, asparagusProcessor, pather, viz, coms, camera, output = assemble(config_path ='config.yaml')
print('CLASSES LOADED')


try:
    while True:


        data = {}
        camera.getData()
        image = camera.image
        image_data = prp.process(image)
        net_output = ep.process(image_data)
        boxes, masks, classid = pop.process(net_output)

        if len(classid) != 0:


            spears, data = asparagusProcessor.process(boxes, masks) #filtered on camera reach and camera distance
            data1 = pather._filter_height_distance(spears) #filtered on length and min/max distance

            print(data1)



            image = viz.process_tests(image, data1)

        output.renderImage(image)

except Exception as e:
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