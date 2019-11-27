import  os, glob
import  random, csv
import tensorflow as tf
from tqdm import tqdm


def load_csv(root, filename, name2label):
    # 从csv文件返回images,labels列表
    # root:数据集根目录，filename:csv文件名， name2label:类别名编码表
    if not os.path.exists(os.path.join(root, filename)):
        # 如果csv文件不存在，则创建
        images = []
        for name in name2label.keys(): # 遍历所有子目录，获得所有的图片
            # 只考虑后缀为png,jpg,jpeg的图片：'pokemon\\mewtwo\\00001.png
            images += glob.glob(os.path.join(root, name, '*.png'))
        # 打印数据集信息：1167, 'pokemon\\bulbasaur\\00000000.png'
        print(len(images))
        random.shuffle(images) # 随机打散顺序
        # 创建csv文件，并存储图片路径及其label信息
        with open(os.path.join(root, filename), mode='w', newline='') as f:
            writer = csv.writer(f)
            for img in tqdm(images):  # 'pokemon\\bulbasaur\\00000000.png'
                name = img.split(os.sep)[-2]
                label = name2label[name]
                # 'pokemon\\bulbasaur\\00000000.png', 0
                writer.writerow([img, label])

    # 此时已经有csv文件，直接读取
    images, labels = [], []
    with open(os.path.join(root, filename)) as f:
        reader = csv.reader(f)
        for row in reader:
            # 'pokemon\\bulbasaur\\00000000.png', 0
            img, label = row
            label = int(label)
            images.append(img)
            labels.append(label) 
    # 返回图片路径list和标签list
    return images, labels


def load_data(root, mode='train'):
    # 创建数字编码表
    name2label = {}  # "sq...":0
    # 遍历根目录下的子文件夹，并排序，保证映射关系固定
    for name in sorted(os.listdir(os.path.join(root))):
        # 跳过非文件夹
        if not os.path.isdir(os.path.join(root, name)):
            continue
        # 给每个类别编码一个数字
        name2label[name] = len(name2label.keys())

    # 读取Label信息
    # [file1,file2,], [3,1]
    images, labels = load_csv(root, 'images.csv', name2label)

    if mode == 'train':  # 60%
        images = images[:int(0.6 * len(images))]
        labels = labels[:int(0.6 * len(labels))]
    elif mode == 'val':  # 20% = 60%->80%
        images = images[int(0.6 * len(images)):int(0.8 * len(images))]
        labels = labels[int(0.6 * len(labels)):int(0.8 * len(labels))]
    else:  # 20% = 80%->100%
        images = images[int(0.8 * len(images)):]
        labels = labels[int(0.8 * len(labels)):]

    return images, labels, name2label


# # 这里的mean和std根据真实的数据计算获得，比如ImageNet
# img_mean = tf.constant([0.485, 0.456, 0.406])
# img_std = tf.constant([0.229, 0.224, 0.225])
# def normalize(x, mean=img_mean, std=img_std):
#     # 标准化
#     # x: [224, 224, 3]
#     # mean: [224, 224, 3], std: [3]
#     x = (x - mean)/std
#     return x

# def denormalize(x, mean=img_mean, std=img_std):
#     # 标准化的逆过程
#     x = x * std + mean
#     return x

def preprocess(x,y):
    # x: 图片的路径List，y：图片的数字编码List
    x = tf.io.read_file(x) # 根据路径读取图片
    x = tf.image.decode_jpeg(x) # 图片解码

    # 转换成张量
    # x: [0,255]=> 0~1
    x = tf.cast(x, dtype=tf.float32) / 255.
    # 0~1 => D(0,1)
#     x = normalize(x) # 标准化
    y = tf.convert_to_tensor(y) # 转换成张量

    return x, y


def main():


    # 加载数据集，指定加载训练集
    images, labels, table = load_data('4_Png', 'train')
    print('images:', len(images))
    print('labels:', len(labels))
    print('table:', table)

    # images: string path
    # labels: number
    db = tf.data.Dataset.from_tensor_slices((images, labels))
    db = db.map(preprocess).batch(1024)

    # 创建TensorBoard对象
    writter = tf.summary.create_file_writer('logs')
    for step, (x,y) in enumerate(db):
        # x: [32, 224, 224, 3]
        # y: [32]
        with writter.as_default():
#             x = denormalize(x) # 反向normalize，方便可视化
            # 写入图片数据
            tf.summary.image('img',x,step=step,max_outputs=9)


if __name__ == '__main__':
    main()