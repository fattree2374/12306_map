
---

# 概论
pandas基于numpy
NaN，not a number 在pandas中表示缺失或NA值
```py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

# pd函数 
## 文件交互
### chunk 分块
### read_csv;to_csv
```py
pd.read_csv('a.csv',encoding='utf8')
    read_csv(sep分隔符, delimiter定界符,  header, names列名列表, index_col用作行索引的列编号或列名
    usecols使用到的列, dtype每一列的数据类型{'a':np.float64,'b':np.int32} ，converters列转换函数的字典

data.to_csv('guangdong_station.csv', index=False, encoding='gbk')
```
### read_sql
`read_sql(sql,conn,params={'name':'value'})`
sql为SQL语句，conn为连接，params为传入参数
### [追加写入](https://stackoverflow.com/questions/17530542/how-to-add-pandas-data-to-an-existing-csv-file)
```python
df.to_csv('my_csv.csv', mode='a', header=False)

with open('my_csv.csv', 'a') as f:
    df.to_csv(f, header=False)
```
## set_option()
`pd.set_option('expand_frame_repr', False)` 不允许换行显示数据
`pd.set_option('display.max_rows', None)` 全部显示
`pd.set_option('display.max_columns', None)` 全部显示
## 逻辑判断函数
`pd.isnull(Series)`
`pd.notnull(Series)`

# 数据结构
## Series
&emsp;Series 一组数据以及索引组成，算术运算中自动对齐索引
Sereis的一个重要功能是会在算术运算中自动对齐不同索引的数据
1. 创建对象
`obj = Series([4,7,-5,3], index=['d','b','a','c'])`
也可以用字典创建Series对象： obj=Series(sdata)
2. 属性及值
`obj.values`
`obj.index`
`obj.isnull()` 检测缺失数据
`obj[obj>0]` 返回obj序列中大于0的数据
`'b' in obj` 返回True或False
`obj.name='x'` 修改列名
`obj.index.name='y'` 修改索引名
3. 方法
* 排序
`Series.sort_index()`
`Series.sort_values()` 如果有缺失值将被置于末尾
* 映射
map()只要是作用将函数作用于一个Series的每一个元素，如果传入的是字典，就将序列和字典通过共有键连接起来
```py
format = lambda x: '%.2f' % x #函数的作用是将元素转换为规定的小数格式
frame['e'].map(format) #作用于序列的每个元素
```
* str类方法
`contains()` 是否包含表达式
## DataFrame
### 创建对象
``` python
segment = DataFrame({'station_start':station_start,
        'station_end':station_end,
        'longitude_start':longitude_start,
        'latitude_start':latitude_start,
        'longitude_end':longitude_end,
        'latitude_end':latitude_end},
        columns=['station_start','station_end','longitude_start','latitude_start','longitude_end','latitude_end'])

 df2 = pd.DataFrame({ 
     'A' : 1.,
     'B' : pd.Timestamp('20130102'),
     'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
     'D' : np.array([3] * 4,dtype='int32'),
     'E' : pd.Categorical(["test","train","test","train"]),
     'F' : 'foo' })
 
 df_empty = pd.DataFrame(columns=['s', 'i', 'r'])  #空的DF

DataFrame(data,columns=[],index=[])
嵌套字典传给DataFrame时，外层字典的键作为列，内层键作为行索引

获取列： frame['state']  frame.state  列可赋值修改
获取行：frame.ix['three']
del frame['eastern'] 删除列
df.drop('a') 删除df索引为a的行
```
### 查看数据
查看对象的方法对于Series来说同样适用
``` python
1.
a=DataFrame(data);
a.head(6)表示显示前6行数据，若head()中不带参数则会显示全部数据。
a.tail(6)表示显示后6行数据，若tail()中不带参数则也会显示全部数据。
2.
a.index ; a.columns ; a.values 即可
3.
a.describe()对每一列数据进行统计，包括计数，均值，std，各个分位数等。
4.对数据的转置
a.T
5.对轴进行排序
a.sort_index(axis=1,ascending=False,inplace=True)；
其中axis=1表示对所有的columns进行排序，下面的数也跟着发生移动。后面的ascending=False表示按降序排列，参数缺失时默认升序。inplace=True代表会替换掉原来的DF
6.对DataFrame中的值排序
a.sort_values(by='x') sort函数已被抛弃
即对a中的x这一列，从小到大进行排序。注意仅仅是x这一列，而上面的按轴进行排序时会对所有的columns进行操作。
7.df2.dtypes
显示每一列的类型，如float64,category...
8.df.empty
返回True或False
```
### 选择对象
1. 选择特定列和行的数据
``` python
a['x'] 那么将会返回columns为x的列，注意这种方式一次只能返回一个列。a.x与a['x']意思一样。
取行数据，通过切片[]来选择
如：a[0:3] 则会返回前三行的数据。
```

2. 使用标签选择数据
`loc`
``` python
a.loc['one']则会默认表示选取行为'one'的行；
a.loc[:,['a','b'] ] 表示选取所有的行以及columns为a,b的列；
a.loc[['one','two'],['a','b']] 表示选取'one'和'two'这两行以及columns为a,b的列；
a.loc['one','a']与a.loc[['one'],['a']]作用是一样的，不过前者只显示对应的值，而后者会显示对应的行和列标签。
```
at的使用方法与loc类似，但是比loc有更快的访问数据的速度，而且只能访问单个元素，不能访问多个元素。
``data_fecha.at[fecha_1,'rnd_1']``

3. 使用位置选择数据
`iloc`
``` python
a.iloc[1:2,1:2] 则会显示第一行第一列的数据;(切片后面的值取不到)
a.iloc[1:2] 即后面表示列的值没有时，默认选取行位置为1的数据;
a.iloc[[0,2],[1,2]] 即可以自由选取行位置，和列位置对应的数据。
```
iat对于iloc的关系就像at对于loc的关系，是一种更快的基于索引位置的选择方法，同at一样只能访问单个元素。
``data_fecha.iat[1,0]``

4. 使用条件来选择
``` python
使用单独的列来选择数据
a[a.c>0] 表示选择c列中大于0的数据
使用where来选择数据
a[a>0] 表直接选择a中所有大于0的数据
使用isin()选出特定列中包含特定值的行
a1=a.copy()
a1[a1['one'].isin(['2','3'])] 表显示满足条件：列one中的值包含'2','3'的所有行。
```
### 设置值（赋值）
1. 赋值操作在上述选择操作的基础上直接赋值即可。
 `sir_data.loc[index,['s','i','r']]=[s,i,r]` 对指定行写入数据
3. 修改列名
``coordinates.rename(columns={'city':'station'},inplace=True)``
3. 修改索引名称
 `df.index.rename('times',inplace=True)`
### 缺失值处理
在pandas中，使用np.nan来代替缺失值，这些值将默认不会包含在计算中。
1. reindex()方法
用来对指定轴上的索引进行改变/增加/删除操作，这将返回原始数据的一个拷贝。
``` python
a.reindex(index=list(a.index)+['five'],columns=list(a.columns)+['d'])
a.reindex(index=['one','five'],columns=list(a.columns)+['d'])
```
即用index=[]表示对index进行操作，columns表对列进行操作。
2. 对缺失值进行填充
``a.fillna(value=x)``
表示用值为x的数来对缺失值进行填充
3. 去掉包含缺失值的行
``a.dropna(how='any')``
表示去掉所有包含缺失值的行
4. 判断缺失值
``pd.isna(df1)``
### 相关操作
1. 描述性统计
`a.mean()` 默认对每一列的数据求平均值
`a.mean(1)`则对每一行求平均值
2. 统计某一列x中各个值出现的次数
`a['x'].value_counts()`
3. `apply`，`applymap`
表示返回所有列中最大值-最小值的差，默认对列，对行则设置`axis=1`
`a.apply(lambda x:x.max()-x.min())`
对指定列应用函数
`data.ix[:,['0','1']].apply(f)`
对指定行应用函数
`data.ix[[0,1],:].apply(f)`
对数据框内每个元素应用
`format = lambda x: '%.2f' % x`
`frame.applymap(format)`
4. 字符串相关操作
`a['gender1'].str.lower()`
将gender1中所有的英文大写转化为小写，注意dataframe没有str属性，只有series有，所以要选取a中的gender1字段。
5. 行数；列数
`frame.index.size`
`frame.column.size`
6. 去重
`data.drop_duplicates(['k2'])`
对指定列去重，若为空则按全部列去重，`inplace=True`表示替换掉原来的DF
7. 分组
`frame.groupby('gender').size()`
`data.groupby(['col1', 'col2'])['col3'].mean()`
可以对各个gender下的数目进行计数，也可以使用其他方法
8. 合并
* `contact`可以将数据根据不同的轴作简单的融合

`contact(a1,axis=0/1，keys=['xx','xx','xx',...])`
其中a1表示要进行进行连接的列表数据,即将几个数据框放进列表,axis=1在横轴方向连接。axis=0或不指定时在竖轴方向连接。a1中要连接的数据有几个则对应几个keys，设置keys是为了在数据连接以后区分每一个原始a1中的数据。例：
```py
a1=[b['a'],b['c']]
result=pd.concat(a1,axis=1，keys=['1','2'])
```
* Append 将一行或多行数据连接到一个DataFrame上

`df.append(a[2:],ignore_index=True)`
表示将a中的第三行以后的数据全部添加到df中，若不指定ignore_index参数，则会把添加的数据的index保留下来，若ignore_index=Ture则会对所有的行重新自动建立索引。
append之后需要重新赋值给dataframe，否则添加不成功

* merge类似于SQL中的join

设a1,a2为两个dataframe,二者中存在相同的键值，两个对象连接的方式有下面几种：
内连接 `pd.merge(a1, a2, on='key')`
左连接 `pd.merge(a1, a2, on='key', how='left')`
右连接 `pd.merge(a1, a2, on='key', how='right')`
外连接  `pd.merge(a1, a2, on='key', how='outer')`

9. 重构
* `stack`将行索引变成了外层索引，列索引变成了内层索引，返回series类型
`stacked = df_obj.stack()`
* `unstack`会默认多层索引的series转变为DataFrame，默认情况下是对内索引进行操作，即将内所有转变为DataFrame的列索引,`level=0`表示操作外层索引
`stacked.unstack()`

* pivot_table()

`lc` 数据；`index` 生成透视表的索引；`values` 需要透视的数据；`aggfunc` 透视的方法；`fill_value` 将NaN值处理为0；`columns` 增加列维度
当对`aggfunc`传入字典时：`aggfunc={"Quantity":len,"Price":np.sum}`，可以对指定列使用指定方法
```python
pd.pivot_table(lc,index=["grade","term"],values=["loan_amnt","total_rec_int"],columns=["home_ownership","term"],aggfunc=[np.sum,np.mean,len],fill_value=0)
```
只查看一个管理者的数据:``table.query('Manager == ["Debra Henley"]')``

10. 遍历数据
* 按行遍历
`for index, row in data.iterrows():`   # 获取每行的index、row
* 按列遍历
`for ix, col in df.iteritems():`
   
11. 离散化与面元划分
为了便于分析，连续数据常常离散化或拆分为“面元”（bin）。例如，需要将其划分为“18到25”, “26到35”，“36到60”以及“60以上”几个面元;可以通过right=False指定哪端是开区间或闭区间
```py
In [106]: ages = [20, 22,25,27,21,23,37,31,61,45,41,32]
In[37]: bins = [18, 25, 35, 60, 100]
In[43]: group_name = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior'] #指定面元名称
In[38]: cats = pd.cut(ages, bins, labels=group_name)
>>> cat # cat是一个Categorical(类别型)类型  
[(0, 25], (50, 75], (25, 50], (75, 100], (50, 75], (25, 50], (25, 50], NaN, (75, 100], NaN]  
Categories (4, interval[int64]): [(0, 25] < (25, 50] < (50, 75] < (75, 100]]  
>>> cat.codes # 数组原来的元素数据第几个面元  
array([ 0,  2,  1,  3,  2,  1,  1, -1,  3, -1], dtype=int8)  
>>> pd.value_counts(cat) # 每个面元有多少个元素  
(25, 50]     3  
(75, 100]    2  
(50, 75]     2  
(0, 25]      1  
dtype: int64  
还可以不指定面元的界限，直接传入一个整数参数，cut()会按照指定的数字，将元素划分为相应的几部分。  
>>> pd.cut(array, 5)  
cut()函数划分得到的面元，每个面元的数量不同。而qcut()可以保证每个面元的数量相同，且每个面元的区间大小不等。  
>>> pd.qcut(array, 5)  
```



### 特殊类型
#### Categorical
按某一列重新编码分类
如六中要对a中的gender进行重新编码分类，将对应的0，1转化为male，female，过程如下：
``` python
a['gender1']=a['gender'].astype('category')
a['gender1'].cat.categories=['male','female']  #即将0，1先转化为category类型再进行编码
```

#### 时间序列
##### pandas.Timestamp类
&emsp;常用属性：`year`,`month`,`day`,`hour`,`minute`,`second`,`quarter`,`weekday_name`,`value`,`dayofweek`,

用`pd.date_range('xxxx',periods=xx,freq='D/M/Y....')`函数生成连续指定天数的的日期列表。
例如`pd.date_range('20000101',periods=10)`,其中periods表示持续频数；
`pd.date_range('20000201','20000210',freq='D')`也可以不指定频数，只指定起始日期。

日期序列格式转换
``index=pd.to_datetime(index)``
`timestamp.strftime(format = '%Y%m%d')`转换为指定格式的字符串；
当然如果不需要特定格式，可直接`str(timestamp)`





## 索引对象Index
不可修改immutable,可安全共享
### Multiindex 层次索引
对带多重索引的dataframe取值一般使用xs，取到一个交叉片段，若想取特定位置，可以使用两次xs
`df.xs(1, level='b')`
#### 层次索引作图
### 设置列为索引
`df.set_index('column_name',inplace=Ture)`


# 错误异常
#### ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
在pandas中使用布尔运算时,会发生如上错误
`解决方案`:将各项用括号,且用&代替and
#### TypeError: pivot_table() got multiple values for argument 'values'
原语句：
`pivot_data=station_data.pivot_table(station_data,index=['train_id'],values=['train_no'],columns=['station'])`
解决方案：将多余的参数去掉`station_data`
`pivot_data=station_data.pivot_table(index=['train_id','station'],values=['train_no'])`
#### UserWarning: This pattern has match groups. To actually get the groups, use str.extract
原代码是用于在DataFrame中match字符串，警告的意思是match只会返回True或False，不会返回对应条目;要想消去警告，可以使用：
```py
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')
```
#### SettingWithCopyWarning
对原数据进行直接重写时会触发，可以直接新建一个数据框

# 未分类
## shift()
shift函数可以返回某一列的所有前一行，功能与ORACLE的lag和lead（有分组）类似，但shift本身没有分组，不过可以通过groupby实现同样的功能
```py
db["Data_lagged"] = db.Data.shift(1) #新增Data_lagged列，其值等于Data列每行的前一行，缺失值为NaN
df['Data_lagged'] = df.groupby(['Group'])['Data'].shift(1) #实现与ORACLE的lag和lead相同的功能
```
## add()
`a.add(b, fill_value=0)`等价于a+b，但可以将缺失值补充为指定值。
## cumsum()
`df.cumsum(axis=1)` 返回累加和

