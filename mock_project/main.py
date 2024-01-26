import gradio as gr
import pandas as pd

# Hàm get_data mẫu
def get_data(input_text):
    # Xử lý dữ liệu tùy thuộc vào input_text
    # ...

    # Trả về một DataFrame với các cột tùy chọn
    custom_columns = ['column1', 'column2']  # Thay thế bằng tên các cột bạn muốn
    data = {'column1': ['value1', 'value2'],
            'column2': ['value3', 'value4']}  # Thay thế bằng dữ liệu thực tế

    return pd.DataFrame(data, columns=custom_columns)

# Tạo Gradio Interface
iface = gr.Interface(
    fn=get_data,
    inputs=gr.Textbox(),
    outputs=gr.Dataframe()  # Chú ý: Dataframe, không phải Dataframe()
)

# Chạy Gradio Interface
iface.launch()