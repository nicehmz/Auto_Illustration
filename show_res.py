from PIL import Image
import streamlit as st


def show_img_res(res_img_url_lst, score_6_lst, p_index):
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    url1, url2, url3, url4, url5, url6 = res_img_url_lst
    col1.markdown(f"图片1 ： `{score_6_lst[0]}`")
    # col1.header(score_6_lst[0])
    col1.image(url1, use_column_width=True)

    col2.markdown(f"图片2 ： `{score_6_lst[1]}`")
    # col2.header(score_6_lst[1])
    col2.image(url2, use_column_width=True)

    col3.markdown(f"图片3 ： `{score_6_lst[2]}`")
    # col3.header(score_6_lst[2])
    col3.image(url3, use_column_width=True)

    col4.markdown(f"图片4 ： `{score_6_lst[3]}`")
    # col4.header(score_6_lst[3])
    col4.image(url4, use_column_width=True)

    col5.markdown(f"图片5 ： `{score_6_lst[4]}`")
    # col5.header(score_6_lst[4])
    col5.image(url5, use_column_width=True)

    col6.markdown(f"图片6 ： `{score_6_lst[5]}`")
    # col6.header(score_6_lst[5])
    col6.image(url6, use_column_width=True)

    # select_img_index_lst = st.multiselect('选择该段配图：', label = ['图片1', '图片2', '图片3', '图片4', '图片5', '图片6'],key=[p_index+str(i) for i in range(1,7)])
    tmp = [f'第{p_index}段_图{i}' for i in range(1, 7)]
    tmp.insert(0, f'第{p_index}段_全选')
    select_img_index_lst = st.multiselect('选择该段配图：', tmp)
    # st.write(select_img_index_lst)

    if f'第{p_index}段_全选' in select_img_index_lst:
        return [i for i in range(0, 6)]
    else:
        return [int(i[-1]) - 1 for i in select_img_index_lst]

if __name__ == '__main__':
    url1 = 'https://c.pxhere.com/photos/9a/2e/legs_woman_heels_sexy_skin_knees_feet_high_heels-836491.jpg!s1'
    url2 = 'https://c.pxhere.com/photos/5c/82/beach_alone_lonely_ocean_sea-112608.jpg!s1'
    url3 = 'https://c.pxhere.com/photos/3b/aa/sun_autumn_nature_fall_colors_sunlight_landscape_colors_lighting-1030003.jpg!s1'
    url4 = 'https://c.pxhere.com/photos/e8/13/bathtub_faucet_white_bathroom_clean_water_modern_tap-865136.jpg!s1'
    url5 = 'https://c.pxhere.com/photos/93/25/moon_night_full_moon_gespenstig_mystical_midnight_creepy_atmosphere-744076.jpg!s1'
    url6 = 'https://c.pxhere.com/photos/85/59/ice_winter_cold_frozen_nature_cool_weather_tree-1086896.jpg!s1'

    res_img_url_lst = [url1, url2, url3, url4, url5, url6]

    show_img_res(res_img_url_lst)
