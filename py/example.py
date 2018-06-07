# -*- coding: utf-8 -*-

from qa import QA

doc_dir = "../docs"
q = QA(doc_dir)

res = q.predict("2017年“9元享看”活动开展时间？",2,3)
print(res)

res = q.predict("365活动线上和线下一共可以有几次权益？",2,3)
print(res)

res = q.predict_single_doc("365活动线上和线下一共可以有几次权益？", "精彩365线上平台（餐券平台）活动知识库原文档.docx", 3)
print(res)

# Tips: 问题最好包含文档标题的关键字
