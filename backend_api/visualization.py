from backend_api.cloudinary_integration import cloudinary
import interpreter

interpreter.auto_run = True
interpreter.model = "gpt-3.5-turbo"
interpreter.api_key = "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"

class Visualization:
    @staticmethod
    def open_interpreter( data_visualization_json, cloudinary_folder="lexograph"):
        prompt_interpreter=f"Load the data {data_visualization_json} that I am getting from the my database.Generate a suitable chart using a plotting library (e.g., Matplotlib, Plotly)..Generate the visualization and save it as user_graph.png in the 'graph_history' folder but before saving check if graph_history folder has any file with the same name make sure to delete the older file and then save the file."
        interpreter.chat(prompt_interpreter)

        image_path ='./graph_history/user_graph.png'
        upload_response = cloudinary.uploader.upload(image_path, folder=cloudinary_folder)
        image_url = upload_response.get("url")

        return image_url