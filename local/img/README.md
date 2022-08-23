# Moment/local/img

This is the default directory which stores all pictures.

Usually, the directory looks like:



```
- img
  - 0_pic_num_file
  - 1
  - 2
  - ...
```



`0_pic_num_file` will be created the first time you use `Moment` and it records the number of pictures.



## 附

`Moment` 的图片删除策略是懒惰删除，也即它只删除 json 文件中的图片索引数据，不删除 `img` 文件底下的图片。因此在长期使用时会出现一部分 “没有被任何地方引用” 的图片（可以叫野图片）。野图片在实际使用过程不会太多，也不影响正常使用，可以放任不管。当然，也可以使用脚本选择清理。