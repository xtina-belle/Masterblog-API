// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    const savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        loadPost(savedBaseUrl);
    }
}

// Function to fetch the post from the API and display them on the page
function loadPost(baseUrl) {
    // Retrieve the postId from the query parameter
    var urlPath = window.location.pathname;
    var postId = urlPath.split('/')[1];

     // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(`${baseUrl}/${postId}/update`, {method: 'GET'})
        .then(response => response.json())  // Parse the JSON data from the response
        .then(post => {  // Once the data is ready, we can use it
            // Clear out the post container first
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For post in the response, create a new post element and add it to the page

            const postDiv = document.createElement('div');
            postDiv.className = 'input-field';
            postDiv.innerHTML = `<label for="title">Title:</label><br>
            <p><input type="text" id="title" name="title" value="${post.title}"></p><br>
            <label for="content">Content:</label><br>
            <p><textarea id="content" name="content">${post.content}</textarea></p><br>
            <button onclick="updatePost(${post.id_})">Save</button>`;
            postContainer.appendChild(postDiv);

        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

function updatePost(postId) {

    const baseUrl = localStorage.getItem('apiBaseUrl');

    // Construct the updated post data as a JavaScript object
    var updatedPostData = {
        title: document.getElementById('title').value,
        content: document.getElementById('content').value
    };

    // Use the Fetch API to send a PUT request to the specific post's endpoint
    fetch(`${baseUrl}/${postId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedPostData)
    })
    .then(response => {
        console.log('Post updated:', postId);
        // Redirect back to the home page after updating the post
        window.location.href = '/';
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}