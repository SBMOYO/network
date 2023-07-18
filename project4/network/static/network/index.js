/* function editPost(post_id) {
  const content = document.querySelector(`#textarea_${post_id}`).value;
  const postCommentElement = document.querySelector(`#post_${post_id}`);
  const modal = document.querySelector(`#modal_edit_post_${post_id}`);

  updatePost(content, post_id)
    .then((response) => {
      const post_comment = response["comment"];
      postCommentElement.textContent = post_comment;

      closeModal(modal);
    })
    .catch((error) => {
      console.error("Error updating post:", error);
      // Handle the error gracefully (e.g., show an error message to the user)
    });
}  */

async function editPost(postId) {
  const content = document.querySelector(`#textarea_${postId}`).value;
  const postElement = document.querySelector(`#post_${postId}`);
  const modal = document.querySelector(`#modal_edit_post_${postId}`);

  try {
    const response = await updatePost(content, postId);
    const postComment = response.comment;
    postElement.textContent = postComment;
    closeModal(modal);

  } catch (error) {
    console.error("Error updating post:", error);
  }
}

function closeModal(modal) {
  modal.classList.remove("show");
  modal.setAttribute("aria-hidden", "true");
  modal.setAttribute("style", "display: none");

  const modalsBackdrops = document.getElementsByClassName("modal-backdrop");
  for (let i = 0; i < modalsBackdrops.length; i++) {
    document.body.removeChild(modalsBackdrops[i]);
  }
}

async function updatePost(post, postId) {
  const url = "/updatePost";
  const method = "POST";
  const headers = {
    "Content-Type": "application/json",
  };
  const body = JSON.stringify({
    comment: post,
    post_id: postId,
  });

  const response = await fetch(url, {method,headers, body,});

  const data = await response.json();
  return data;
}

function postLikeExists(post_id, postsYouLike) {
  console.log(postsYouLike);
  return postsYouLike.indexOf(post_id) >= 0;
}

async function likeHandler(post_id, postsYouLike) {
  const btn = document.querySelector(`#like_${post_id}`);
  const likeCount = document.querySelector(`#like_count_${post_id}`);
  if (postLikeExists(post_id, postsYouLike)) {
    //remove like
    const response = await removePostLike(post_id);
    console.log(response.success);
    likeCount.textContent = response.like_count;
    btn.className = "btn btn-info fa fa-thumbs-up col-1";
  } else {
    //add like to collection
    const response = await addNewPostLike(post_id);
    console.log(response.success)
    likeCount.textContent = response.like_count;
    btn.className = "btn btn-info fa fa-thumbs-down col-1";
  }
}


async function addNewPostLike(post_id) {
  const url = "/addPostLike";
  const method = "POST";
  const headers = {
    "Content-Type": "application/json",
  };
  const body = JSON.stringify({
    post_id: post_id,
  });
  const response = await fetch(url, {method, headers, body});
  const data = await response.json();
  return data;
}

async function removePostLike(post_id) {
  const url = "/removePostLike";
  const method = "POST";
  const headers = {
    "Content-Type": "application/json",
  };
  const body = JSON.stringify({
    post_id: post_id,
  });
  const response = await fetch(url, {method, headers, body});
  const data = await response.json();
  return data;
}