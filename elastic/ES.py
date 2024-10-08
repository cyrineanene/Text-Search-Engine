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

# Function to search and display images from Elasticsearch based on query input
def display_results(query):
    # Check if the server is up
    server_message = check_server(es)
    if server_message:
        return server_message

    # Define the search query to match the input in the "title" and "tags" fields
    search_query = {
        "multi_match": {
            "query": query,
            "fields": ["title", "tags"]  # Adjust fields based on your search needs
        }
    }

    # Perform the search query on the "flickr_photos" index
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
        # Construct the image URL based on the index fields
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
        gr.Markdown("# Flickr Photos Search Engine")
        gr.Markdown("Enter a search term to find images by title or tags.")

        # Input for search query
        query_input = gr.Textbox(label="Enter your search query", placeholder="Enter keywords related to title or tags")

        # Gallery to display results
        results_gallery = gr.Gallery(label="Search Results", show_label=False)

        # Button to initiate search
        search_button = gr.Button("Search")
        search_button.click(display_results, inputs=query_input, outputs=results_gallery)

    return demo

# Launch the Gradio app
if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch()