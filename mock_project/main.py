import gradio as gr
import pandas as pd

with gr.Blocks() as demo:
    error_box = gr.Textbox(label="Error", visible=False)

    keyword_box = gr.Textbox(label="Search Text")
    submit_btn = gr.Button("Search")

    with gr.Column(visible=False) as output_col:
        links_table = gr.Dataframe()  # Thay đổi từ gr.HTML sang gr.Dataframe()
        links_table.style = "compact"
        
    def submit(keyword):
        if len(keyword) == 0:
            return {error_box: gr.Textbox(value="Search Text", visible=True)}
        
        links = []
        if "gradio_learn" in keyword:
            links.append({"kết quả": "https://www.gradio.app/custom-components/gallery"})
            links.append({"kết quả": "https://www.gradio.app/docs/chatinterface/"})
        if "gradio_example" in keyword:
            links.append({"kết quả": "https://www.gradio.app/docs/chatinterface/"})
        if "gradio_quick_start" in keyword:
            links.append({"kết quả": "https://www.gradio.app/docs/interface#interface-queue-example-usage"})

        # Tạo DataFrame từ danh sách liên kết
        df = pd.DataFrame(links)

        # Chuyển DataFrame thành gr.Dataframe để hiển thị
        links_table.value = df if not df.empty else pd.DataFrame()

        return {
            output_col: gr.Column(visible=True),
            links_table: links_table.value,
        }

    submit_btn.click(
        submit,
        [keyword_box],
        [error_box, links_table, output_col],
    )

demo.launch()
