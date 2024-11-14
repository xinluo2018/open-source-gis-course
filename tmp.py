import numpy 

print('hellow world!')




#导入ogr模块
from osgeo import ogr

def read(path, area_field='dt_name'):
    '''使用 ogr 读取矢量数据，并返回字段名、字段数量、要素数量以及所有不同区域的名称。'''
    
    # 以只读模式打开数据源，0表示只读，1表示可写
    ds = ogr.Open(path, 0)  
    # 获取数据源中的第一个图层
    layer = ds.GetLayer(0)
    
    # 统计并打印要素数量，GetFeatureCount() 方法返回图层中的要素数量
    count_features = layer.GetFeatureCount()
    # 输出要素数量进行查看
    print('要素数量:', count_features)
    
    # 获取字段名，遍历图层的所有字段，获取每个字段的名称
    fields = [layer.GetLayerDefn().GetFieldDefn(i).GetName() 
              for i in range(layer.GetLayerDefn().GetFieldCount())]
    # 计算字段的数量
    count_fields = len(fields)  
    # 输出字段名进行查看
    print('字段名:', fields)
    
    # 获取所有区域名称，从指定的字段中提取区域名称
    # 使用集合去重，避免重复的区域名称
    area_names = set()  
    for feature in layer:
        area_names.add(feature.GetField(area_field))  # 此处区域名称字段是 'dt_name'
    
    # 将集合转换为列表
    area_names = list(area_names)
    # 输出所有区域的名称进行查看
    print('所有区域名称:', area_names)
    
    # 返回字段名、字段数量、要素数量以及所有区域名称
    return fields, count_fields, count_features, area_names


def vec_sel(path, path_out, selected_areas, selected_fields=None):
    '''根据多个区域的名称选择要素，并将它们输出到一个 Shapefile 文件中。'''

    # 如果未指定选择字段，默认选择所有字段
    if selected_fields is None:
        selected_fields = []  # 没有指定字段，则选择所有字段

    # 打开原始数据，以只读方式打开数据源
    ds = ogr.Open(path, 0)  # 0表示只读，1表示可写
    # 获取数据源中的第一个图层
    layer = ds.GetLayer(0)  
    
    # 获取字段名，遍历图层的所有字段，获取每个字段的名称
    fields = [layer.GetLayerDefn().GetFieldDefn(i).GetName() 
              for i in range(layer.GetLayerDefn().GetFieldCount())]
    print('原始字段名:', fields)
    
    # 打印已选择的区域名
    print('选择的区域:', selected_areas)
    print('选择的字段:', selected_fields)
    
    # 释放只读数据源
    ds = None
    
    # 获取区域的数据源，创建驱动对象，使用 ESRI Shapefile 驱动
    driver = ogr.GetDriverByName('ESRI Shapefile')
    # 打开输入的 Shapefile 文件
    in_ds = ogr.Open(path, 0)
    in_layer = in_ds.GetLayer()  # 获取图层
    
    # 创建新的 Shapefile 数据源，并指定字符集为 'UTF-8'（用于中文支持）
    ds_out = driver.CreateDataSource(path_out)
    # 创建新的图层，使用原图层的空间参考
    layer_out = ds_out.CreateLayer('selected_areas', geom_type=ogr.wkbPolygon,
                                    srs=in_layer.GetSpatialRef(), options=['ENCODING=UTF-8'])

    # 如果没有指定选择字段，创建所有字段
    if not selected_fields:  # 如果没有指定字段，选择所有字段
        selected_fields = fields

    # 动态创建字段：根据选定的字段创建字段
    for field_name in selected_fields:
        if field_name in fields:  # 只创建已存在的字段
            # 创建字符串类型的字段
            field_defn = ogr.FieldDefn(field_name, ogr.OFTString)  
            layer_out.CreateField(field_defn)  # 在输出图层中创建字段
        else:
            # 如果字段不存在，打印警告
            print(f"警告: 字段 '{field_name}' 不存在。")
    
    # 获取新的要素定义
    fea_defn = layer_out.GetLayerDefn()

    # 复制符合条件的要素到新文件
    for i in range(in_layer.GetFeatureCount()):  # 遍历输入图层的所有要素
        in_fea = in_layer.GetFeature(i)  # 获取第i个要素
        # 根据区域名称筛选要素
        if str(in_fea.GetField('dt_name')) in selected_areas:  # 根据区域名称字段（dt_name）过滤
            in_geo = in_fea.geometry()  # 获取要素的几何形状
            # 创建新的要素
            fea_out = ogr.Feature(fea_defn)  
            fea_out.SetGeometry(in_geo)  # 设置几何信息
                
            # 复制选定的字段值
            for field_name in selected_fields:
                if field_name in fields:  # 只复制指定的字段
                    field_value = in_fea.GetField(field_name)  # 获取字段值
                    fea_out.SetField(field_name, field_value)  # 设置字段值

            # 将新的要素添加到输出图层
            layer_out.CreateFeature(fea_out)

    # 关闭并保存输出数据源
    ds_out = None  

    # 关闭输入数据源
    in_ds = None  

    return "处理完成"  # 返回处理完成的消息
