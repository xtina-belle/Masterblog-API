// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    const savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts(url = getInputBaseUrl()) {
    // Retrieve the base URL from the input field and save it to local storage
    const baseUrl = getInputBaseUrl();
    localStorage.setItem('apiBaseUrl', baseUrl);

    // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(url)
        .then(response => response.json())  // Parse the JSON data from the response
        .then(data => {  // Once the data is ready, we can use it
            // Clear out the post container first
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For each post in the response, create a new post element and add it to the page
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `<p><em>Written by ${post.author}</em></p>
                <h2>${post.title}</h2><p>${post.content}</p>
                <button onclick="deletePost(${post.id_})">Delete</button>
                <button id="update" onclick="redirectToUpdatePage(${post.id_})">Update</button>
                <p><em>Date: ${post.date}</em></p>
                <button id="like" onclick="likePost(${post.id_})">👍🏼 ${post.like}</button>`;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a POST request to the API to add a new post
function addPost() {
    // Retrieve the values from the input fields
    const baseUrl = getInputBaseUrl();

    // Use the Fetch API to send a POST request to the /posts endpoint
    fetch(baseUrl, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            title: document.getElementById('post-title').value,
            content: document.getElementById('post-content').value
        })
    })
    .then(response => response.json())  // Parse the JSON data from the response
    .then(post => {
        console.log('Post added:', post);
        loadPosts(); // Reload the posts after adding a new one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a POST request to the API to add a new post
function search() {
    // Retrieve the values from the input fields
    const baseUrl = getInputBaseUrl();

    const postAuthor = ((document.getElementById('post_author')||{}).value)||"";
    const postTitle = ((document.getElementById('post_title')||{}).value)||"";
    const postContent = ((document.getElementById('post_content')||{}).value)||"";

    const url = `${baseUrl}/search?${postAuthor ? 'author=' + postAuthor : ''}` +
    `${postAuthor ? '&' : ''}${postTitle ? 'title=' + postTitle : ''}` +
    `${postTitle ? '&' : ''}${postContent ? 'title=' + postContent : ''}`

    loadPosts(url)
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

function redirectToUpdatePage(postId) {
    const baseUrl = getInputBaseUrl();
    // Redirect to the update page and pass the postId as a query parameter
    window.location.href = `/${postId}/update`;
    }

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    const baseUrl = getInputBaseUrl();

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(`${baseUrl}/${postId}`, {method: 'DELETE'})
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a LIKE request to the API to like a post
function likePost(postId) {
    const baseUrl = getInputBaseUrl();

    // Use the Fetch API to send a LIKE request to the specific post's endpoint
    fetch(`${baseUrl}/${postId}/like`, {method: 'POST'})
    .then(response => {
        console.log('Post was liked:', postId);
        loadPosts(); // Reload the posts after liking one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

function getInputBaseUrl() {
    return document.getElementById('api-base-url').value;
}
