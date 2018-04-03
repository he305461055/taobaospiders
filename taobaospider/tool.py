import urllib
import time
import os


log_dir='C:/Users/Administrator/Desktop/taobao/log/'
img_dir='D:/photo/taobao/'
config_dir='C:/Users/Administrator/taobaospider/taobaospider/file_config/'
data_dir='C:/Users/Administrator/Desktop/taobao/休闲男装/'
#data_dir='C:/Users/Administrator/Desktop/DAIYUYING/'
channel_name='taobao'
contentfilename='user_content'

#写入日志
def GetLog(name,data):
    datetime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    date=time.strftime("%Y-%m-%d",time.localtime())
    data='[%s]%s:::::%s' %(str(datetime),str(date),data)
    file = '%s%s_%s_%s.txt' % (log_dir,name, 'LOG',str(date))
    with open(file, 'a', encoding='utf-8') as f:
        f.write(data)
        f.write('\n')

#下载图片
def GetImg(dir,url,img_name):

    urllib.request.urlretrieve(url, '%s%s' % (dir, img_name))
    '''
    try:
         #conn = urllib.request.urlopen(url)
         urllib.request.urlretrieve(url,'%s%s' %(img_dir, img_name))
    except Exception as e:
         print(e)
         print(url)
         print('无法下载请检查路径')
         GetLog('dzdp_deatail','%s:%s' %(url,'无法下载请检查路径'))
         return None
    '''
    #img = conn.read()
    #with open('%s%s' %(img_dir, img_name), 'wb') as f:
     #   f.write(img)

#写入文件
def GetFile(filename,data,type,count):
    # 没有文件夹生成
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    # 没有文件的话生成文件
    if not os.path.exists(r'%s%s_variable.txt' %(config_dir,filename)):
        with open('%s%s_variable.txt' %(config_dir,filename), 'w', encoding='utf-8') as f:
            pass

    variable = len(open('%s%s_variable.txt' %(config_dir,filename),encoding='utf-8').readlines())
    file='%s%s_%s_%d.txt' % (data_dir,channel_name, filename,variable)
    # 没有文件的话生成文件
    if os.path.exists(r'%s' % file):
        pass
    else:
        with open(file, 'w', encoding='utf-8') as f:
            pass

    if type==1:
        with open(file, 'a', encoding='utf-8') as f:
           f.write(data)
           f.write('\n')
    if type==3:
        sum = -1
        for sum, line in enumerate(open(r"%s" % file, 'rU', encoding='utf-8')):
            pass
        sum += 1
        if sum<count:
            with open(file, 'a', encoding='utf-8') as f:
                f.write(data)
                f.write('\n')
        else:
            with open('%s%s_variable.txt' %(config_dir,filename), 'a', encoding='utf-8') as f:
                f.write('global')
                f.write('\n')
            variable = len(open('%s%s_variable.txt' %(config_dir,filename),encoding='utf-8').readlines())
            file = '%s%s_%s_%d.txt' % (data_dir,channel_name, filename, variable)
            with open(file, 'a', encoding='utf-8') as f:
                f.write(data)
                f.write('\n')