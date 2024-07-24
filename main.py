import streamlit as st
from PIL import Image
import pandas as pd
import plotly.graph_objects as go
data = {
    "替代率（甲醇比例）%": [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0],
    "热流辐射强度（W/m²）": [4105, 4692, 5126, 5394, 6602, 6881, 7368, 8270, 8501, 9150, 9711],
    "PM10测量浓度（μg/m³）": [9.2, 58.2, 114.04, 121.46, 158.88, 176.3, 243.72, 251.14, 308.56, 345.98, 383.4]
}
st.title(":green[Green Methanol] Mixed Combustion System Demo :sunny")
df = pd.DataFrame(data)

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["替代率（甲醇比例）%"],
    y=df["热流辐射强度（W/m²）"],
    mode='lines+markers',
    name='热流辐射强度（W/m²）',
    yaxis='y1',
    line=dict(color='#23BAC5')  # 指定线条颜色
))

fig.add_trace(go.Scatter(
    x=df["替代率（甲醇比例）%"],
    y=df["PM10测量浓度（μg/m³）"],
    mode='lines+markers',
    name='PM10测量浓度（μg/m³）',
    yaxis='y2',
    line=dict(color='#A5C2E2')  # 指定线条颜色
))
# Create axis objects
fig.update_layout(
    xaxis=dict(title='替代率（甲醇比例）%'),
    yaxis=dict(title='热流辐射强度（W/m²）', titlefont=dict(color='blue'), tickfont=dict(color='blue')),
    yaxis2=dict(title='PM10测量浓度（μg/m³）', titlefont=dict(color='red'), tickfont=dict(color='red'),
                anchor='x', overlaying='y', side='right')
)


prev_ratio=0.1
ratio=st.select_slider("Mixing Ratio(Methanol/Fuel)", [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
def overlay_images(imageA_path, imageB_path, imageA_size,imageB_size):
    # 打开图像A和图像B
    imageA = Image.open(imageA_path)
    imageB = Image.open(imageB_path)
    
    # 调整图像B的大小
    imageA = imageA.resize(imageA_size)
    imageB = imageB.resize(imageB_size)
    
    # 获取图像A和图像B的尺寸
    widthA, heightA = imageA.size
    widthB, heightB = imageB.size
    
    # 计算图像B的粘贴位置，使其横向中心对齐并与图像A右对齐
    paste_x = widthA - widthB
    paste_y = (heightA - heightB) // 2
    
    # 创建一个新的图像，复制图像A
    new_image = imageA.copy()
    
    # 将图像B粘贴到新图像
    new_image.paste(imageB, (paste_x, paste_y), imageB)
    
    return new_image.transpose(Image.FLIP_LEFT_RIGHT)

# 示例使用
imageA_path = './static/mol6.png'
imageB_path = './static/mol5.png'
imageB_size = (200, 100)  # 设定图像B的大小
placeholder = st.empty()

    
result_image = overlay_images(imageA_path, imageB_path, (int(100*(0.1-ratio))+600,250),(int(300*(ratio-0.1))+200,100))
placeholder.image(result_image)
# Streamlit display
pp=st.popover("Display Combustion Data")
pp.plotly_chart(fig,use_container_width=True)
cols=st.columns(3)
with cols[1]:
    st.image('./static/mol8.png',caption='Radiation', use_column_width=True)
placeholder1=st.empty()
placeholder1.image('./static/oristate.png', use_column_width=True)

cols4= st.columns(3)
with cols4[1]:
    st.image('./static/mol8.png', use_column_width=True)
st.image('./static/mol7.png',caption='Smelter', use_column_width=True)

if( ratio!=prev_ratio):
    result_image = overlay_images(imageA_path, imageB_path, (int(100*(0.1-ratio))+600,250),(int(300*(ratio-0.1))+200,100))
    placeholder.image(result_image)
    prev_ratio=ratio
if(ratio>0.6):
    placeholder1.image('./static/wstate.png', use_column_width=True)
elif (ratio>0.3):
    placeholder1.image('./static/oristate.png', use_column_width=True)
else:
    placeholder1.image('./static/cstate.png', use_column_width=True)
