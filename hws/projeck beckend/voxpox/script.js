let comments = [];
const perPage = 5;
let currentPage = 1;

document.getElementById('commentForm').addEventListener('submit', function (e) {
  e.preventDefault();
  const text = document.getElementById('commentText').value;
  const category = document.querySelector('input[name="category"]:checked').value;

  comments.unshift({ text, category, time: new Date() });
  document.getElementById('commentForm').reset();
  currentPage = 1;
  renderComments();
});

document.getElementById('loadMoreBtn').addEventListener('click', () => {
  currentPage++;
  renderComments();
});

function renderComments() {
  const container = document.getElementById('comments');
  container.innerHTML = '';

  const start = 0;
  const end = currentPage * perPage;
  const visibleComments = comments.slice(start, end);

  visibleComments.forEach(comment => {
    const div = document.createElement('div');
    div.className = comment.category;
    div.textContent = `[${comment.category.toUpperCase()}] ${comment.text}`;
    container.appendChild(div);
  });

  if (comments.length > end) {
    document.getElementById('loadMoreBtn').style.display = 'block';
  } else {
    document.getElementById('loadMoreBtn').style.display = 'none';
  }
}
