        // Function to perform AJAX request to Flask server
        function performAction(action) {
            // Replace 'YOUR_FLASK_ROUTE' with your actual Flask route URL
            fetch('/your-flask-route/' + action, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    // Handle the response data here, if needed
                    console.log(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }

        // Event listeners for the clickable images
        document.getElementById('comment').addEventListener('click', function() {
            performAction('comment');
        });

        document.getElementById('heart').addEventListener('click', function() {
            performAction('heart');
        });

        document.getElementById('dislike').addEventListener('click', function() {
            performAction('dislike');
        });

        document.getElementById('share').addEventListener('click', function() {
            performAction('share');
        });

        // closing pop ups
        function togglePopUp(popUpId) {
            var popUp = document.getElementById(popUpId);
            if (popUp.style.display === "none") {
                popUp.style.display = "block";
            } else {
                popUp.style.display = "none";
            }
        }

        // showing adding comment action
        var addCommentImage = document.getElementById('add_comment');

        // Add a click event listener to the image
        addCommentImage.addEventListener('click', function () {
            var popUp = document.getElementById('pop_up2');
            if (popUp.style.display === "none") {
                popUp.style.display = "block";
            } else {
                popUp.style.display = "none";
            }
        });