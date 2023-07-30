function togglePopUp(popUpId) {
    var popUp = document.getElementById(popUpId);
    if (popUp.style.display === 'none') {
        popUp.style.display = 'block';
    } else {
        popUp.style.display = 'none';
    }
}

let isLiked = false; // Track the current like state

function likeBlog() {
  if (isLiked) {
    // If already liked, send a DELETE request to unlike the blog post
    fetch('/unlike', { method: 'DELETE' })
      .then(response => response.json())
      .then(data => {
        const likeCountElement = document.getElementById('like-count');
        likeCountElement.textContent = data.likes;
        isLiked = false; // Update the like state
      })
      .catch(error => console.error('Error:', error));
  } else {
    // If not liked, send a POST request to like the blog post
    fetch('/like', { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        const likeCountElement = document.getElementById('like-count');
        likeCountElement.textContent = data.likes;
        isLiked = true; // Update the like state
      })
      .catch(error => console.error('Error:', error));
  }
}


// dislike

let isdisLiked = false; // Track the current like state

function dislikeBlog() {
  if (isdisLiked) {
    // If already liked, send a DELETE request to unlike the blog post
    fetch('/undislike', { method: 'DELETE' })
      .then(response => response.json())
      .then(data => {
        const likeCountElement = document.getElementById('dislike-count');
        likeCountElement.textContent = data.dislikes;
        isdisLiked = false; // Update the like state
      })
      .catch(error => console.error('Error:', error));
  } else {
    // If not liked, send a POST request to like the blog post
    fetch('/dislike', { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        const likeCountElement = document.getElementById('dislike-count');
        likeCountElement.textContent = data.dislikes;
        isdisLiked = true; // Update the like state
      })
      .catch(error => console.error('Error:', error));
  }
}