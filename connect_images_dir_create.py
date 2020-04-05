import sys
import os
import json
from PIL import Image, ImageFilter

def generate_base_16_16_png (filename):
    size = (16, 16)
    saved = "connect_icon.png"
    try:
        img = Image.open(filename)
        width, height = img.size
        if (width != height):
            print ("Error: Aspect ratio of image must be 1:1")
            return
        img.thumbnail(size)
        img.save(saved)

        return img

    except:
        print( "Error: Unable to load image " + filename)

def generate_grayscale_png (img):
    img = img.convert('LA')
    img.save("gray_connect_icon.png")
    return

def generate_failed_png(img):
    try:
        filename = "failed.png"
        img_failed = Image.open(filename, 'r')
        final_img = Image.new('RGBA', (16,16), (0, 0, 0, 0))
        final_img.paste(img, (0,0))
        final_img.paste(img_failed, (0,11))
        final_img.save("failed_connect_icon.png", format="png")
    except:
        print("Error: Unable to crate failed_connect.png verify base failed.png is present")


def generate_waitting_png(img):
        try:
            filename = "waiting.png"
            img_waiting = Image.open(filename, 'r')
            final_img = Image.new('RGBA', (16,16), (0, 0, 0, 0))
            final_img.paste(img, (0,0))
            final_img.paste(img_waiting, (0,11))
            final_img.save("waiting_connect_icon.png", format="png")
        except:
            print("Error: Unable to crate waiting_connect.png verify base waiting.png is present")

def generate_path(path):
    # split head folder (appName) from file (property.conf)
    head, tail = os.path.split(path)
    
    # rejoin imagesPath with head + images/
    imagesPath = os.path.join(head, 'images/')
    
    # if images folder does not exist in appName makdir the images folder  
    if not os.path.exists(imagesPath):
        os.mkdir(imagesPath)
    
    if path.lower().endswith(('.conf', '.json')):
        with open (path) as json_file:
            if not os.path.exists(os.path.join(imagesPath, "np_ng")):
                os.makedirs(os.path.join(imagesPath, "np_ng"))
            data = json.load (json_file)
            try:
                for ag in data['action_groups']:
                    if not os.path.exists(imagesPath+"np_ng/action_groups/" +ag['name']+"/"):
                        os.makedirs(imagesPath+"np_ng/action_groups/" + ag['name']+"/")
                    filename = imagesPath+"np_ng/action_groups/" + ag['name']+"/" + ag['name'] +".png"
                    final_img = Image.new('RGBA', (16,16), (0, 0, 0, 0))
                    final_img.save(filename, format="png")
            except:
                print ("No Action Groups created")
            try:
                for a in data['actions']:
                    if not os.path.exists(imagesPath+"np_ng/actions/" + a['name'] + "/"):
                        os.makedirs(imagesPath+"np_ng/actions/"+ a['name'] + "/")

                    filename1 = imagesPath+"np_ng/actions/" + a['name'] +"/" + a['name'] + ".png"
                    filename2 = imagesPath+"np_ng/actions/" + a['name'] +"/failed_" + a['name'] + ".png"
                    filename3 = imagesPath+"np_ng/actions/" + a['name'] +"/gray_" + a['name'] + ".png"
                    filename4 = imagesPath+"np_ng/actions/" + a['name'] +"/waiting_" + a['name'] + ".png"
                    final_img = Image.new('RGBA', (16,16), (0, 0, 0, 0))
                    final_img.save(filename1, format="png")
                    final_img.save(filename2, format="png")
                    final_img.save(filename3, format="png")
                    final_img.save(filename4, format="png")
            except:
                print("No Actions created")
            try:
                for g in data['groups']:
                    if not os.path.exists(imagesPath+"np_ng/field_groups/" + g['name'] + "/"):
                        os.makedirs(imagesPath+"np_ng/field_groups/"+ g['name'] + "/")
                    filename = imagesPath+"np_ng/field_groups/"+ g['name'] + "/" + g['name'] + ".png"
                    final_img = Image.new('RGBA', (16,16), (0, 0, 0, 0))
                    final_img.save(filename, format="png")
            except:
                print("No Field Groups created")
            try:
                for policy in data['policy_template']['policies']:
                    if not os.path.exists(imagesPath+"np_ng/templatedirs/" + data['policy_template']['policy_template_group']['name'] + "/"):
                        os.makedirs(imagesPath+"np_ng/templatedirs/"+ data['policy_template']['policy_template_group']['name'] + "/")

                    if not os.path.exists(imagesPath+"np_ng/templatedirs/"+ data['policy_template']['policy_template_group']['name'] + "/" + policy['title_image']):
                        filename = imagesPath+"np_ng/templatedirs/"+ data['policy_template']['policy_template_group']['name'] + "/" + policy['title_image']
                        final_img = Image.new('RGBA', (16,16), (0, 0, 0, 0))
                        final_img.save(filename, format="png")
            except:
                print("No policy template templatedirs created")


    else:
        print ("Invalid File type: connect iamges can accept .conf and .json")
        return
    
    
            
def main():
    try:
        path = sys.argv[1]
    except:
        print ("Error: Exception Must pass in the property.conf filename")
    if (len(sys.argv) != 2):
        print("Error: Must pass in exactly one argument")
        return

    if not os.path.exists(path):
        print ("Error: No such file")
        return
    
    generate_path(path)


if __name__ == "__main__":
    main()
