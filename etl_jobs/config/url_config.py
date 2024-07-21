# Define the list of URLs and target folders

def get_url_list(folder_prefix):
    url_list = [
        {
            'url': 'https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q1_2016.zip', 
            'folder': f'{folder_prefix}/Q1_2016'
            },
        # Add more URLs and folders as needed
    ]
    return url_list