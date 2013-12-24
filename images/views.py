# -*-coding:utf-8-*-

from django.shortcuts import render
from django.http import HttpResponse
from images.models import ResultImages
from django.core.exceptions import ObjectDoesNotExist
import json
import os
import os.path
import sys

DATA_DIR = './imagesdb/'

# 上传的文件保存起来
def save_uploaded_file(f, filename):
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    return HttpResponse("Hello, world. You're at the images index.")


# 查询是否有新的请求，查找状态为0的记录
# 有的话，取出该记录，然后解析出来各个参数并返回
def get_parameter(request):
    if request.method == 'GET':
        todos = ResultImages.objects.filter(status=0)
        result = {'parameters': []}
        for todo in todos:
            result['parameters'].append(todo.paraName)
        return HttpResponse(json.dumps(result), content_type='application/json')


# 判断参数是否有效
def is_paras_valid(paras):
    try:
        numbers = [float(_) for _ in paras]
        if 0.0 <= numbers[0] <= 1.0 and 0.0 <= numbers[1] <= 1.0 and \
            1.0 <= numbers[2] <= 100.0 and 1.0 <= numbers[3] <= 50.0 and \
            0.0 <= numbers[4] <= 1.0 and 10.0 <= numbers[5] <= 300.0 and \
            0.0 <= numbers[6] <= 1.0:
            return True
        else:
            return False
    except:
        print(sys.exc_info()[0])


# 接收到各个参数，然后生成一个统一的名字（可解析），然后存入数据库
# 状态初始化为0
def post_parameter(request):
    if request.method == 'POST':
        paras = []
        # keep in order!
        paras.append(request.POST['ambient'])#环境光
        paras.append(request.POST['cdom'])#
        paras.append(request.POST['depth'])#水深
        paras.append(request.POST['frame_step'])#渲染速度
        paras.append(request.POST['fresnel_coeff'])#参数
        paras.append(request.POST['influx'])#流量
        paras.append(request.POST['wave_scale'])#水波
        if is_paras_valid(paras):
            paras_str = '_'.join(paras)
            image_dir = DATA_DIR + paras_str
            if not os.path.exists(image_dir):
                os.mkdir(image_dir)
            ri = ResultImages(paraName=paras_str, status=0,
                              imageDir=image_dir, imageNum=0)
            ri.save()
            result = {'status': 'ok'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {'status': 'bad parameter'}
            return HttpResponse(json.dumps(result), content_type='application/json')


# 上传一张图片，参数为paraname，和第几张图片，
# 把图片存入到与参数相对应的文件夹
def post_image(request):
    if request.method == 'POST':
        para_name = request.POST['paraname']
        image_order = request.POST['imageorder']
        result = {}
        try:
            obj = ResultImages.objects.get(paraName=para_name)
            target_dir = obj.imageDir
            if request.FILES:
                fp = request.FILES['upload']
                save_uploaded_file(fp, target_dir+'/'+image_order+'.jpg')
                result['status'] = 'ok'
            else:
                result['status'] = 'no image uploaded.'
        except ObjectDoesNotExist:
            print('this is object does not exists.')
        except:
            print('some exceptions happened.')
        finally:
            return HttpResponse(json.dumps(result), content_type='application/json')


# 根据参数名查找图片所在文件夹
# 根据图片的次序量来获取图片
def get_image(request):
    if request.method == 'GET':
        if 'paraname' in request.GET:
            para_name = request.GET['paraname']
            entry = ResultImages.objects.get(paraName=para_name)
            target_dir = entry.imageDir
            image_order = request.GET['imageorder']
            filename = '%s/%s.jpg' % (target_dir, image_order)
            if os.path.exists(filename):
                fp = open(filename, 'rb').read()
                return HttpResponse(fp, mimetype='image/jpeg')
            else:
                return HttpResponse(
                    json.dumps({'status':"Image doesn't exists."}),
                    content_type='application/json'
                )
        else:
            result = {'status':'No such parameter. You must create first.'}
            return HttpResponse(json.dumps(result),
                                content_type='application/json')


# 清空数据库
def clear_database(request):
    if request.method == 'GET':
        ResultImages.objects.all().delete()
        return HttpResponse("<h1>database cleared!</h1>")

#用来测试
def test(request):
    if request.method == 'POST':
        if request.FILES:
            fp = request.FILES['upload']
            save_uploaded_file(fp, './imagesdb/111222/test.jpg')
            result = {'status':'ok'}
            print(json.dumps(result))
            return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        para_name = request.GET['paraname']
        image_name = request.GET['imagename']
        filename = '%s/%s/%s' %('imagesdb', para_name, image_name)
        if os.path.exists(filename):
            fp = open(filename, 'rb').read()
            return HttpResponse(fp, mimetype='image/jpeg')
        else:
            return HttpResponse(
                json.dumps({'status':"image doesn't exists"}),
                content_type='application/json'
            )
