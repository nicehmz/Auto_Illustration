import os

import numpy as np
from PIL import Image
import base64
import io
import requests
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from show_res import show_img_res
import streamlit as st


df1 = pd.read_csv('res1.csv')
df2 = pd.read_csv('res2.csv')
df = pd.concat([df1,df2])
df.to_csv('encode_res.csv',index=False)

# from  load_model import *


def load_url_imgage(url):
    res = requests.get(url)
    img_bytes = res.content
    return Image.open(io.BytesIO(img_bytes))


@st.cache(allow_output_mutation=True)
def load_model():
    text_model = SentenceTransformer('clip-ViT-B-32-multilingual-v1')
    image_model = SentenceTransformer('clip-ViT-B-32')

    return text_model, image_model


st.write('载入模型中...')
# text_model = SentenceTransformer('clip-ViT-B-32-multilingual-v1')
# image_model = SentenceTransformer('clip-ViT-B-32')
try:
    # text_model,image_model = load_model()
    text_model, image_model = load_model()
    st.success('模型载入成功！')
except:
    pass
    st.write('载入异常')

img_num = 6840


@st.cache
def load_img_data():
    data_file_path = 'encode_res.csv'
    df = pd.read_csv(data_file_path)
    img_url_lst = df['img_url'][:img_num]

    # img_url_lst = df['img_url'][:100]

    # img_lst = [load_url_imgage(url) for url in img_url_lst]
    col_512 = df.columns[1:]
    # image_vectors = image_model.encode(img_lst)
    # image_vectors = np.array([df.loc[i,col_512] for i in range(len(df))])
    image_vectors = np.array([df.loc[i, col_512] for i in range(img_num)])
    return img_url_lst, image_vectors


img_url_lst, image_vectors = load_img_data()


# st.write(img_url_lst)
# st.write(image_vectors)


# img_url_lst = img_url_lst[:100]
# image_vectors = image_vectors[:100]


def mathch_paragraph(paragraph, p_index, img_url_lst):
    if paragraph:
        text_vectors = text_model.encode([paragraph])

        score_lst = text_vectors @ image_vectors.transpose()

        # st.write(image_vectors)

        dic = {}

        for i in range(len(score_lst[0])):
            score = score_lst[0][i]
            dic[i] = score
        # print(dic)
        sorted_dic_lst = sorted(dic.items(), key=lambda x: x[1], reverse=True)
        # 取前6个分高者
        # st.write(sorted_dic_lst)
        index_6_lst = [i[0] for i in sorted_dic_lst[:6]]
        score_6_lst = [i[1] for i in sorted_dic_lst[:6]]

        res_img_url_lst = [img_url_lst[i] for i in index_6_lst]
        # print(res_img_url_lst)
        # st.write(res_img_url_lst)
        # res_img_lst = [load_url_imgage(i) for i in res_img_url_lst]
        selected_img_index = show_img_res(res_img_url_lst, score_6_lst, p_index)
        img_url_lst = [res_img_url_lst[int(i)] for i in selected_img_index]

        return img_url_lst


###############################
# input sentence
# sentence = '海边坐着一个人'
###############################
# from streamlit_ace import st_ace

# article = st_ace()


article = st.text_area(label='文章内容：', height=600)

paragraph_lst = article.split('\n  ')

tmp = [f'第{i + 1}段' for i in range(len(paragraph_lst))]
tmp.insert(0, '全选')
selected_p = st.multiselect('选择配图段落：', tmp)

if '全选' in selected_p:
    selected_p_index = [i + 1 for i in range(len(paragraph_lst))]
else:

    selected_p_index = [int(i[-2]) for i in selected_p]

# article = st.text_area("文章内容：",height=800)

paragraph_img_dict = {}

for p in paragraph_lst:
    if p.strip() == "":
        continue

    p_index = paragraph_lst.index(p) + 1

    if p_index not in selected_p_index:
        continue

    st.header(f'第{p_index}段：')
    st.text(p)

    paragraph_img_dict[p_index] = mathch_paragraph(p, p_index, img_url_lst)

    # st.write(paragraph_img_dict)

if paragraph_img_dict != {}:

    # st.write(paragraph_img_dict)
    st.header('结果预览如下：')
    st.write('\n')

    res_markdown = ""

    all_content = []

    for i in range(len(paragraph_lst)):
        # st.write(paragraph_lst[i])
        res_markdown = res_markdown + (f"<p>　　{paragraph_lst[i]}</p>")

        # prepare for pdf
        all_content.append(('p', paragraph_lst[i]))

        # res_markdown = res_markdown+(f"{paragraph_lst[i]}" + '<br>')
        if i + 1 not in paragraph_img_dict.keys():
            continue
        for img in paragraph_img_dict[i + 1]:
            # st.image(img)
            # res_markdown = res_markdown + f' ![图片]({img}#pic_left)<br>'
            # res_markdown = res_markdown + f"<img src={img} width='400' height='400' />"
            res_markdown = res_markdown + f"<img src={img} width=100% height=100% />"
            all_content.append(('img', img))

    # print(res_markdown)
    st.markdown(res_markdown, unsafe_allow_html=True)
    # st.write(res_markdown)

    isExists = os.path.exists('output')
    if not isExists:
        os.makedirs('output')

    with open('output/res.md', 'w', encoding='utf-8') as f:
        f.write(res_markdown)

    input_path = st.text_input('Markdown文件保存路径：')
    save_path = 'output/res.md'
    if save_path != '':
        save_path = input_path
    if st.button('保存MD', ):
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(res_markdown)
            st.success('Markdown格式文件保存成功')

    with open('output/res.md', 'rb') as f:
        if st.download_button('下载MD', f, file_name='res.md'):
            st.success('Markdown格式文件下载成功')

    # 导出 markdown
