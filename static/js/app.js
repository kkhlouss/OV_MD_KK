const $ = (sel, el = document) => el.querySelector(sel);
const $$ = (sel, el = document) => Array.from(el.querySelectorAll(sel));

const state = {
  movies: [],
  reviews: [],
  selectedMovieId: null,
};

const API_KEY = 'ca2e4688';

async function api(path, options = {}) {
  const headers = Object.assign({ 'X-API-Key': API_KEY }, options.headers || {});
  const res = await fetch(path, Object.assign({}, options, { headers }));
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function movieCard(movie) {
  const el = document.createElement('article');
  el.className = 'card';
  el.innerHTML = `
    <div class="poster" style="background-image:url('${movie.poster}'); background-size: cover; background-position: center;"></div>
    <div class="body">
      <div class="title">${movie.title}</div>
      <div class="meta">${movie.year} · <span class="badge">${movie.rating}</span></div>
    </div>
  `;
  el.addEventListener('click', () => selectMovie(movie.id));
  return el;
}

function renderPopular(movies) {
  const grid = $('#popularGrid');
  grid.innerHTML = '';
  movies.slice(0, 6).forEach(m => grid.appendChild(movieCard(m)));
}

function renderCatalog(movies) {
  const grid = $('#catalogGrid');
  grid.innerHTML = '';
  movies.forEach(m => grid.appendChild(movieCard(m)));
}

function renderSelected(movie) {
  const wrap = $('#selectedMovie');
  if (!movie) { wrap.innerHTML = '<p class="muted">Izvēlieties filmu no kataloga.</p>'; return; }
  wrap.innerHTML = `
    <div class="poster" style="background-image:url('${movie.poster}'); background-size: cover; background-position: center;"></div>
    <div>
      <h3 class="title" style="font-size:16px;">${movie.title}</h3>
      <div class="meta">${movie.year} · Vērtējums <span class="badge">${movie.rating}</span></div>
      <p class="desc">${movie.description}</p>
      <div class="meta">Žanri: ${movie.genres.join(', ')}</div>
    </div>
  `;
}

function renderReviews(list) {
  const wrap = $('#reviewsList');
  wrap.innerHTML = '';
  list.forEach(r => {
    const el = document.createElement('article');
    el.className = 'review';
    const date = new Date(r.createdAt).toLocaleDateString('lv-LV');
    el.innerHTML = `
      <div class="head">
        <div class="author">${r.author}</div>
        <div class="date">${date}${r.rating ? ' · ' + r.rating + '/10' : ''}</div>
      </div>
      <div>${r.content}</div>
    `;
    wrap.appendChild(el);
  });
}

function renderSampleReviews(list) {
  const ul = $('#sampleReviews');
  ul.innerHTML = '';
  list.slice(0, 3).forEach(r => {
    const li = document.createElement('li');
    li.textContent = `“${r.content}” — ${r.author}`;
    ul.appendChild(li);
  });
}

async function loadPopular() {
  const data = await api('/api/movies/popular');
  renderPopular(data.movies);
}

async function loadCatalog() {
  const min = Number($('#minRating').value);
  const genre = $('#genre').value;
  const params = new URLSearchParams();
  if (min) params.set('min_rating', String(min));
  if (genre) params.set('genre', genre);
  const data = await api('/api/movies?' + params.toString());
  state.movies = data.movies;
  renderCatalog(state.movies);
  renderReviewMovieOptions(state.movies);
  if (!state.selectedMovieId && state.movies.length) selectMovie(state.movies[0].id);
}

async function loadReviews(movieId = null) {
  const qs = movieId ? `?movie_id=${movieId}` : '';
  const data = await api('/api/reviews' + qs);
  state.reviews = data.reviews;
  renderReviews(state.reviews);
  renderSampleReviews(state.reviews);
}

function renderReviewMovieOptions(movies) {
  const sel = $('#reviewMovie');
  const selected = state.selectedMovieId;
  sel.innerHTML = '';
  movies.forEach(m => {
    const opt = document.createElement('option');
    opt.value = String(m.id);
    opt.textContent = m.title;
    if (m.id === selected) opt.selected = true;
    sel.appendChild(opt);
  });
}

async function selectMovie(id) {
  state.selectedMovieId = id;
  const movie = state.movies.find(m => m.id === id) || (await api(`/api/movies/${id}`));
  renderSelected(movie);
  renderReviewMovieOptions(state.movies.length ? state.movies : [movie]);
  await loadReviews(id);
}

function bindFilters() {
  const min = $('#minRating');
  const out = $('#minRatingValue');
  out.textContent = min.value;
  min.addEventListener('input', () => { out.textContent = min.value; });
  min.addEventListener('change', loadCatalog);
  $('#genre').addEventListener('change', loadCatalog);
}

function bindForms() {
  $('#reviewForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = {
      movieId: Number($('#reviewMovie').value),
      author: $('#reviewAuthor').value.trim(),
      content: $('#reviewContent').value.trim(),
      rating: Number($('#reviewRating').value || 0) || null,
    };
    if (!body.author || !body.content) return;
    const res = await api('/api/reviews', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    $('#reviewContent').value = '';
    if (res && body.movieId === state.selectedMovieId) await loadReviews(state.selectedMovieId);
  });

  $('#contactForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = {
      name: $('#cName').value.trim(),
      email: $('#cEmail').value.trim(),
      message: $('#cMessage').value.trim(),
    };
    const status = $('#contactStatus');
    status.textContent = 'Sūtam…';
    try {
      await api('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      status.textContent = 'Paldies, ziņa nosūtīta!';
      $('#contactForm').reset();
    } catch (e) {
      status.textContent = 'Neizdevās nosūtīt. Lūdzu mēģiniet vēlreiz.';
    }
  });
}

async function init() {
  $('#year').textContent = new Date().getFullYear();
  bindFilters();
  bindForms();
  await Promise.all([loadPopular(), loadCatalog(), loadReviews()]);
}

window.addEventListener('DOMContentLoaded', init);
