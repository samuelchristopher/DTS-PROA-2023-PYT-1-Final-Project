fetch('http://127.0.0.1:8000/books')
  .then((response) => response.json())
  .then((json) => {
    let li = `<tr><th>ID</th><th>Name</th><th>Year</th><th>Author</th><th>Publisher</th><th>Status</th><th colspan=2>Action</th></tr>`;

    console.log(json.books);
    if (json.books.length == 0) {
      li += `<tr>
        <td colspan=7>Empty Data</td>
      </tr>`;
    }
    json.books.forEach((book) => {
      if (book.deleted_at == null) {
        li += `<tr>
          <td>${book.id}</td>
          <td>${book.title} </td>
          <td>${book.year}</td>
          <td>${book.author}</td>
          <td>${book.publisher}</td>
          <td><span class="badge badge-success">Aktif</span></td>
          <td><a id="updateBtn" type="button" class="btn btn-primary">Update</a></td>
          <td><a id="deleteBtn" onclick="RESTDelete(${book.id})" type="button" class="btn btn-warning">Delete</a></td>
        </tr>`;
      } else {
        li += `<tr>
          <td>${book.id}</td>
          <td>${book.title} </td>
          <td>${book.year}</td>
          <td>${book.author}</td>
          <td>${book.publisher}</td>
          <td><span class="badge badge-secondary">Nonaktif</span></td>
          <td><a type="button" class="btn btn-secondary" disabled>Update</a></td>
          <td><a type="button" class="btn btn-secondary" disabled>Delete</a></td>
        </tr>`;
      }
    });

    // 4. DOM Display result
    document.getElementById('table_books').innerHTML = li;
  });

function RESTDelete(id) {
  fetch('http://127.0.0.1:8000/books/' + id, {
    method: 'DELETE',
  }).then(() => location.reload());
}
