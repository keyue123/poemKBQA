# 基于知识图谱的KBQA
# 上手教程

环境配置
    Python版本为3.7
    jena和fuseki为3.9

准备数据
    sql文件已经提供，直接导入mysql中即可

目录说明
    demo文件夹包含的是完成整个问答demo流程所需要的脚本。
        data文件夹是结巴外部词典的数据
            dynasty.txt朝代
            extendWords.txt扩展词
            poem.txt诗词名
            poet.txt诗人名
            verse.txt诗句
        fileHandle.py
            文件处理，诗句与诗对应，作者与作品对应
        poet_main.py
            main函数，在运行poet_main.y之前，读者需要启动Fuseki或者D2RQ服务
        questionMapping.py
            定义SPARQL模板和匹配规则
        questionSearch.py
            完成SPARQL请求与解析
        questionSparql.py
            将自然语言转为对应的SPARQL查询
        wordHandle.py
            简单语言处理
            
    poemData.sql
        诗词数据存放在mysql的结构及数据
    poem_demo_mapping.ttl
        sql数据导出的映射文件
    poem_kbqa.nt
        利用d2rq，根据mapping文件转换得到的RDF数据
    poem_kbqa.owl
        通过protege构建的本体文件

