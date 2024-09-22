document.addEventListener('DOMContentLoaded', function(){
    const saveButton = document.getElementById('saveButton');
    const postIDElement = document.getElementById('postID');
    const userElement = document.getElementById('user_name');
    const logout = document.getElementById('logout');

    if (logout){
        logout.addEventListener('click', function(){
            alert("Zostałeś pomyślnie wylogowany.");
        });
    }

    // Ensure elements exist before using them
    if (saveButton && postIDElement && userElement){
        const postID = postIDElement.textContent.split(':')[1].trim();
        const user = userElement.textContent.trim();
        saveButton.addEventListener('click', function(){
            check_if_save(postID, user, saveButton);
        });
    }

    // Function to like the post
    const likeButton = document.getElementById("likeButton");
    if (likeButton && userElement && postIDElement) {
        const user = userElement.textContent.trim();
        const postID = postIDElement.textContent.split(':')[1].trim();      
        likeButton.addEventListener('click', function(){
            liking_post(postID, user);
        });
    }

    // Function to like the comment
    if (userElement) {
        const user = userElement.textContent.trim();
        document.querySelectorAll('[id^="commentLike-"]').forEach(button => {
            button.addEventListener('click', function(){
                like_comment(this, user);
            });
        });
    }

    // Function to edit the post
    const editButton = document.getElementById("edit_post");
    if (editButton) {
        editButton.addEventListener('click', function(){
            edit_post(editButton);
        });
    }

    // Function to edit the comment
    const editCommentButtons = document.querySelectorAll(".edit_comment");
    editCommentButtons.forEach(button => {
        button.addEventListener('click', function(){
            edit_comment(button);
        });
    });
});

// Function to check if the post is saved or not
function check_if_save(postID, user, saveButton){
    fetch(`/saved/post/detail/${postID}`)
    .then(response => response.json())
    .then(data => {
        const saved_post = data.find(saved_post => saved_post.user === user);

        if(saved_post){
            // If the post has been saved
            if(saveButton.textContent.trim() === 'Zapisz'){
                fetch(`/detail/save/post/${postID}`,{
                    method: 'PUT', 
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: user,
                        post_id: postID,
                        if_save: true
                    })
                });
                saveButton.textContent = "Usuń z zapisanych";
                saveButton.classList.remove("btn-info");
                saveButton.classList.add("btn-warning");                
            }
            // If the post has not been saved
            else{
                fetch(`/detail/save/post/${postID}`,{
                    method: 'PUT',
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: user,
                        post_id: postID,
                        if_save: false
                    })
                });
                saveButton.textContent = 'Zapisz';
                saveButton.classList.remove("btn-warning");
                saveButton.classList.add("btn-info");
            }
        }
        // If the post has never been saved
        else{
            fetch(`/detail/save/post/${postID}`,{
                method:'POST',
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: user, 
                    post_id: postID,
                    if_save: true    
                })
            });
            saveButton.textContent = 'Usuń z zapisanych';
            saveButton.classList.remove("btn-info");
            saveButton.classList.add("btn-warning");
        }
    });
};

// Function to like the post
function liking_post(postID, user){
    const likeButton = document.getElementById("likeButton");
    const likeCountElement = document.getElementById("like_counting");
    const likeCount = likeCountElement.getAttribute('data-like-count');
    let likeNumber = parseInt(likeCount, 10);

    fetch(`/detail/like/post/${postID}`)
    .then(response => response.json())
    .then(likes => {    
        const userLiked = likes.some(like => like.user === user);
        if (userLiked){
            const userLike = likes.find(like => like.user === user);
            // Unlike if the user has liked the post before
            if (userLike.if_like === true){
                fetch(`/save/like/${postID}`,{
                    method:'PUT', 
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: user, 
                        post_id: postID,
                        if_like: false
                    })
                });
                likeButton.textContent = "Lubię";
                likeButton.classList.remove("btn-danger");
                likeButton.classList.add("btn-success");
                likeNumber -= 1;
                likeCountElement.setAttribute('data-like-count', likeNumber);
                likeCountElement.innerHTML = `<strong>Polubienia:</strong> ${likeNumber}`;
            }
            // Like if the user has unliked the post before
            else{
                fetch(`/save/like/${postID}`,{
                    method: 'PUT', 
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: user, 
                        post_id: postID,
                        if_like: true
                    })
                });
                likeButton.textContent = "Nie lubię";
                likeButton.classList.remove("btn-success");
                likeButton.classList.add("btn-danger");
                likeNumber += 1;
                likeCountElement.setAttribute('data-like-count', likeNumber);
                likeCountElement.innerHTML = `<strong>Polubienia:</strong> ${likeNumber}`;
            }
        }
        // Like if the user has never liked the post before
        else{
            fetch(`/save/like/${postID}`,{
                method: "POST",
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    post_id: postID,
                    username: user,
                    if_like: true
                })
            });
            likeButton.textContent = "Nie lubię";
            likeButton.classList.remove("btn-success");
            likeButton.classList.add("btn-danger");
            likeNumber += 1;
            likeCountElement.setAttribute('data-like-count', likeNumber);
            likeCountElement.innerHTML = `<strong>Polubienia:</strong> ${likeNumber}`;
        }
    });
};

// Function to like the comment
function like_comment(button, user){
    const commentId = button.getAttribute('data-comment-id');

    const likeCountElement = document.getElementById(`like_counting_comment_${commentId}`);
    const likeCount = likeCountElement.getAttribute('data-like-comment');
    let likeNumber = parseInt(likeCount, 10);

    fetch(`/detail/comment/like/post/${commentId}`)
    .then(response => response.json())
    .then(data => {
        const userLiked = data.some(comment => comment.user === user);
        if(userLiked){
            // Toggle like status
            if(button.textContent.trim() === "Lubię"){
                fetch(`/save/comment/like/${commentId}`,{
                    method: 'PUT',
                    headers:{
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        username: user, 
                        comment_id: commentId,
                        if_like: true
                    })
                });
                button.textContent = "Nie lubię";
                button.classList.remove("btn-success");
                button.classList.add("btn-danger");
                likeNumber += 1;
                likeCountElement.setAttribute('data-like-comment', likeNumber);
                likeCountElement.innerHTML = `<strong>Polubienia:</strong> ${likeNumber}`;
            }
            else{
                fetch(`/save/comment/like/${commentId}`,{
                    method: 'PUT', 
                    headers:{
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        username: user,
                        comment_id: commentId,
                        if_like: false
                    })
                });
                button.textContent = "Lubię";
                button.classList.remove("btn-danger");
                button.classList.add("btn-success");
                likeNumber -= 1;
                likeCountElement.setAttribute('data-like-comment', likeNumber);
                likeCountElement.innerHTML = `<strong>Polubienia:</strong> ${likeNumber}`;
            }
        }
        // Like if the user has never liked the comment before
        else{
            fetch(`/save/comment/like/${commentId}`,{
                method: "POST",
                headers:{
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: user, 
                    comment_id: commentId,
                    if_like: true
                })
            });
            button.textContent = "Nie lubię";
            button.classList.remove("btn-success");
            button.classList.add("btn-danger");
            likeNumber += 1;
            likeCountElement.setAttribute('data-like-comment', likeNumber);
            likeCountElement.innerHTML = `<strong>Polubienia:</strong> ${likeNumber}`;
        }
    });
};

// Function to edit the post
function edit_post(editButton){
    const editContent = document.getElementById('edit_content');
    const postID = editButton.getAttribute('data-post-id');
    const postContentElement = document.querySelector('.post-content');

    if(editButton.textContent.trim() === "Edytuj"){
        // Create a text area to edit the post
        const postContent = editContent.getAttribute('data-edit-content');
        const textArea = document.createElement('textarea');

        // Styling the textarea
        textArea.style.fontSize = '22.4px';
        textArea.style.lineHeight = '35.84px';
        textArea.style.maxWidth = '100%'; 
        textArea.style.width = '1050px';   
        textArea.style.padding = '20px';
        textArea.style.margin = '40px auto';
        textArea.style.backgroundColor = '#fff';
        textArea.style.borderRadius = '8px';
        textArea.style.boxShadow = '0 0 15px rgba(0, 0, 0, 0.1)';
        textArea.style.border = '1px solid #ddd';
        textArea.style.height = '300px';
    
        editContent.innerHTML = "";
        postContentElement.innerHTML = "";

        textArea.value = postContent;

        editContent.append(textArea);

        editButton.textContent = "Zapisz";   
             
    }
    else{
        const textArea = editContent.querySelector('textarea');
        if(textArea){
            const userInput = textArea.value;
            
            editContent.setAttribute('data-edit-content', userInput);

            // Updating the post with the new content, and sending it into the database
            fetch(`/save/edit/post/${postID}`,{
                method: 'PUT',
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content: userInput
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    // Successfully saved
                    editButton.textContent = "Edytuj";
                    editContent.innerHTML = userInput;
                } else {
                    // Handle error response
                    console.error(data.error);
                }
            });
        }
    }
};

// Function to edit the comment
function edit_comment(element){
    const commentID = element.getAttribute('data-comment-id');
    const commentElement = document.getElementById(`comment_content_${commentID}`);
    const commentContent = commentElement.getAttribute('data-comment-content');
    const buttonContent = element.textContent.trim();

    // Create a text area to edit the comment
    if(buttonContent === "Edytuj"){
        commentElement.innerHTML = "";
        const textArea = document.createElement('textarea');
        textArea.value = commentContent;
        commentElement.append(textArea);
        element.textContent = "Zapisz";
    }
    // Save the edited comment
    else{
        const textArea = commentElement.querySelector('textarea');
        if(textArea){
            const userInput = textArea.value;
            commentElement.setAttribute('data-comment-content', userInput);
            commentElement.innerHTML = userInput; 
            fetch(`/save/edit/comment/${commentID}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    content: userInput
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    // Successfully saved
                    element.textContent = 'Edytuj';
                } else {
                    // Handle error response
                    console.error(data.error);
                }
            });
        }    
    }
}