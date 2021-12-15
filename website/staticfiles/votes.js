function like(userId, postId, commentId, imgSource, altImgSource, oppImgSource) {
    let fetchURL = "/like";
    let actionRequest = JSON.stringify({ 
        postId: postId, 
        action: "like", 
        userId: userId
    });
    let likeImg = document.getElementById(`like-${postId}`);
    let voteCount = document.getElementById(`count-${postId}`);

    // If request is from a comment, change
    // fetch request variables
    if (commentId !== null) {
        fetchURL = "/like_comment";
        actionRequest = JSON.stringify({ 
            commentId: commentId, 
            action: "like", 
            userId: userId
        })
        likeImg = document.getElementById(`commentLike-${commentId}`);
        voteCount = document.getElementById(`commentCount-${commentId}`);
    }

    // If user clicks on upvote button again but
    // upvote already active, remove upvote
    if (likeImg.classList[0] === 'liked') {
        unlike(userId, postId, commentId, imgSource);
        return;
    }

    // If user clicks on upvote button but downvote
    // already active, remove downvote and activate upvote.
    if (voteCount.classList[0] === 'status-disliked') {
        undislike(userId, postId, commentId, oppImgSource);
    }

    // Ajax to server
    fetch(fetchURL, {
        method: "POST",
        body: actionRequest,
    }).then((_res) => {
        // Change vote count
        voteCount.textContent = String(Number(voteCount.textContent) + 1);
        voteCount.classList.add('status-liked');
        voteCount.style.color = '#5B7EDE';

        // Change board vote count
        changeBoardVotes("like");

        // Change upvote image to shaded upvote
        likeImg.src = altImgSource;
        likeImg.classList.add('liked');
    });
}

function dislike(userId, postId, commentId, imgSource, altImgSource, oppImgSource) {
    let fetchURL = "/like";
    let actionRequest = JSON.stringify({
        postId: postId,
        action: "dislike",
        userId: userId
    });
    let dislikeImg = document.getElementById(`dislike-${postId}`);
    let voteCount = document.getElementById(`count-${postId}`);

    // If request is from a comment, change
    // fetch request variables
    if (commentId !== null) {
        fetchURL = "/like_comment";
        actionRequest = JSON.stringify({ 
            commentId: commentId, 
            action: "dislike", 
            userId: userId
        })
        dislikeImg = document.getElementById(`commentDislike-${commentId}`);
        voteCount = document.getElementById(`commentCount-${commentId}`);
    }

    // If user clicks on downvote button again but
    // downvote already active, remove downvote
    if (dislikeImg.classList[0] === 'disliked') {
        undislike(userId, postId, commentId, imgSource);
        return;
    }

    // If user clicks on downvote button but upvote
    // already active, remove upvote and activate downvote
    if (voteCount.classList[0] === 'status-liked') {
        unlike(userId, postId, commentId, oppImgSource);
    }

    // Ajax to server
    fetch(fetchURL, {
        method: "POST",
        body: actionRequest,
    }).then((_res) => {
        // Change vote count
        voteCount.textContent = String(Number(voteCount.textContent) - 1);
        voteCount.classList.add('status-disliked');
        voteCount.style.color = '#DE5B5B';

        // Change board vote count
        changeBoardVotes("dislike");

        // Change downvote button to shaded downvote
        dislikeImg.src = altImgSource;
        dislikeImg.classList.add('disliked')
    });
}

function unlike(userId, postId, commentId, altImgSource) {
    let fetchURL = "/like";
    let actionRequest = JSON.stringify({
        postId: postId,
        action: "unlike",
        userId: userId
    });
    let likeImg = document.getElementById(`like-${postId}`);
    let voteCount = document.getElementById(`count-${postId}`);

    // If request is from a comment change
    // fetch request variables
    if (commentId !== null) {
        fetchURL = "/like_comment";
        actionRequest = JSON.stringify({ 
            commentId: commentId, 
            action: "unlike", 
            userId: userId
        });
        likeImg = document.getElementById(`commentLike-${commentId}`);
        voteCount = document.getElementById(`commentCount-${commentId}`);
    }

    // Ajax to server
    fetch(fetchURL, {
        method: "POST",
        body: actionRequest,
    }).then((_res) => {
        // Change vote count
        voteCount.textContent = String(Number(voteCount.textContent) - 1);
        voteCount.classList.remove('status-liked');
        voteCount.style.color = '#404040';

        // Change board vote count
        changeBoardVotes("unlike");

        // Change shaded upvote to unshaded upvote
        likeImg.src = altImgSource;
        likeImg.classList.remove('liked');
    });
}

function undislike(userId, postId, commentId, altImgSource) {
    let fetchURL = "/like";
    let actionRequest = JSON.stringify({
        postId: postId,
        action: "undislike",
        userId: userId
    });
    let dislikeImg = document.getElementById(`dislike-${postId}`);
    let voteCount = document.getElementById(`count-${postId}`);

    // If request is from a comment change
    // fetch request variables
    if (commentId !== null) {
        fetchURL = "/like_comment";
        actionRequest = JSON.stringify({ 
            commentId: commentId, 
            action: "undislike", 
            userId: userId
        })
        dislikeImg = document.getElementById(`commentDislike-${commentId}`);
        voteCount = document.getElementById(`commentCount-${commentId}`);
    }

    // Ajax to server
    fetch(fetchURL, {
        method: "POST",
        body: actionRequest,
    }).then((_res) => {
        // Change vote count
        voteCount.textContent = String(Number(voteCount.textContent) + 1);
        voteCount.classList.remove('status-disliked');
        voteCount.style.color = '#404040';

        // Change board vote count
        changeBoardVotes("undislike");

        // Change shaded downvote to unshaded downvote
        dislikeImg.src = altImgSource;
        dislikeImg.classList.remove('disliked'); 
    });
}

function changeBoardVotes(action) {
    const boardUpCount = document.getElementById('sideBarUpCount');
    const boardCloutCount  = document.getElementById('sideBarCloutCount');
    const boardDownCount = document.getElementById('sideBarDownCount');

    if (action === "like") {
        boardUpCount.textContent = String(Number(boardUpCount.textContent) + 1);
    } else if (action === "dislike") {
        boardDownCount.textContent = String(Number(boardDownCount.textContent) + 1);
    } else if (action === "unlike") {
        boardUpCount.textContent = String(Number(boardUpCount.textContent) - 1);
    } else {
        boardDownCount.textContent = String(Number(boardDownCount.textContent) - 1);
    }

    boardCloutCount.textContent = String(Number(boardUpCount.textContent) - Number(boardDownCount.textContent));
}
