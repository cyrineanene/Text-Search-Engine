from elasticsearch import Elasticsearch
import gradio as gr
import requests

# Connect to the Elasticsearch instance
es = Elasticsearch("http://localhost:9200")

# Check if the Elasticsearch server is running
def check_server(client):
    try:
        if not client.ping():
            return "Elasticsearch Server is not running!"
    except Exception:
        return "Error connecting to Elasticsearch server!"
    return None

# Function to display search results from Elasticsearch
def display_results(query, search_type):
    # Check if the server is up
    server_message = check_server(es)
    if server_message:
        return server_message

    # Create the search query based on the selected search type
    search_query = {
        search_type: {"tags": query}
    }

    # Perform the search query on the specified index
    try:
        results = es.search(index="flickr_photos", query=search_query)
    except Exception as e:
        return f"Error performing search: {str(e)}"

    # Prepare the results for display
    images = []
    displayed_images = 0

    for hit in results["hits"]["hits"]:
        if displayed_images >= 16:  # Limit to 16 images
            break
        image_data = hit["_source"]
        image_url = (
            f"http://farm{image_data['flickr_farm']}.staticflickr.com/"
            f"{image_data['flickr_server']}/{image_data['id']}_"
            f"{image_data['flickr_secret']}.jpg"
        )

        # Check if the image URL is accessible
        response = requests.get(image_url)
        if response.status_code == 200:
            images.append(image_url)
            displayed_images += 1

    # Return images or a message if no images were found
    return images if images else "No images found."

# Define the Gradio interface
def create_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Image Search Engine using Elasticsearch")
        gr.Markdown(
            "Enter your search query and select the type of search (match or fuzzy) to find images."
        )

        # Input for search query
        query_input = gr.Textbox(label="Enter your search query", placeholder="Enter tags or keywords")

        # Dropdown for selecting search type
        search_type = gr.Dropdown(choices=["match", "fuzzy"], label="Select Search Type", value="match")

        # Gallery to display results
        results_gallery = gr.Gallery(label="Search Results", show_label=False).scale(grid=[4], height="auto")

        # Button to initiate search
        search_button = gr.Button("Search")
        search_button.click(display_results, inputs=[query_input, search_type], outputs=results_gallery)

    return demo

# Launch the Gradio app
if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch()
