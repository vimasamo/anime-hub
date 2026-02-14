const API_URL = 'https://latin-marlane-privado-42af8e44.koyeb.app/api';
let currentAnime = null;

// Selectors
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const genreSelect = document.getElementById('genreSelect');
const yearSelect = document.getElementById('yearSelect');
const resultsSection = document.getElementById('resultsSection');
const animeDetail = document.getElementById('animeDetail');
const playerSection = document.getElementById('playerSection');
const dashboard = document.getElementById('dashboard');

// Init
window.onload = init;

function resetToHome(e) {
    if (e) e.preventDefault();
    searchInput.value = '';
    genreSelect.value = '';
    yearSelect.value = '';
    showDashboard();
}

function scrollCarousel(id, direction) {
    const carousel = document.getElementById(id);
    const scrollAmount = carousel.offsetWidth * 0.8;
    carousel.scrollBy({ left: scrollAmount * direction, behavior: 'smooth' });
}

async function init() {
    loadLatest();
    loadOnAir();
    loadFilters();
}

async function loadFilters() {
    // Years
    const currentYear = new Date().getFullYear();
    for (let y = currentYear; y >= 1980; y--) {
        const opt = document.createElement('option');
        opt.value = y;
        opt.innerText = y;
        yearSelect.appendChild(opt);
    }

    // Genres
    try {
        const res = await fetch(`${API_URL}/genres`);
        const genres = await res.json();
        genres.forEach(g => {
            const opt = document.createElement('option');
            opt.value = g.toLowerCase();
            opt.innerText = g;
            genreSelect.appendChild(opt);
        });
    } catch (e) { console.error("Error loading genres", e); }
}

async function loadLatest() {
    const latestList = document.getElementById('latestEpisodes');
    latestList.innerHTML = '<p>Cargando...</p>';
    try {
        const res = await fetch(`${API_URL}/latest`);
        const data = await res.json();
        latestList.innerHTML = '';
        data.forEach(ep => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <img src="${ep.poster}" alt="${ep.title}">
                <div class="title">${ep.title} <br><small>Ep. ${ep.episode}</small></div>
            `;
            card.onclick = () => playEpisode(ep.slug, ep.episode);
            latestList.appendChild(card);
        });
    } catch (e) { latestList.innerHTML = '<p>Error al cargar</p>'; }
}

async function loadOnAir() {
    const onAirList = document.getElementById('onAirList');
    onAirList.innerHTML = '<p>Cargando...</p>';
    try {
        const res = await fetch(`${API_URL}/on-air`);
        const data = await res.json();
        onAirList.innerHTML = '';
        data.forEach(anime => {
            const card = document.createElement('div');
            card.className = 'on-air-card';
            card.innerHTML = `
                <div class="type-badge">${anime.type}</div>
                ${anime.poster ? `<img src="${anime.poster}" alt="${anime.title}">` : '<div style="height:200px; background:#2d3748; display:flex; align-items:center; justify-content:center; color:#718096">Sin Imagen</div>'}
                <div class="title">${anime.title}</div>
            `;
            card.onclick = () => loadAnime(anime.slug);
            onAirList.appendChild(card);
        });
    } catch (e) { onAirList.innerHTML = '<p>Error al cargar</p>'; }
}

searchBtn.onclick = () => performSearch();
searchInput.onkeyup = (e) => { if (e.key === 'Enter') performSearch(); };
genreSelect.onchange = () => performSearch();
yearSelect.onchange = () => performSearch();

async function performSearch() {
    const query = searchInput.value;
    const genre = genreSelect.value;
    const year = yearSelect.value;

    if (!query && !genre && !year) {
        showDashboard();
        return;
    }

    resultsSection.innerHTML = '<p>Buscando...</p>';
    showResults();

    try {
        let url = `${API_URL}/search?`;
        if (query) url += `q=${encodeURIComponent(query)}&`;
        if (genre) url += `genre=${genre}&`;
        if (year) url += `year=${year}&`;

        const res = await fetch(url);
        const data = await res.json();

        resultsSection.innerHTML = '';
        if (data.length === 0) {
            resultsSection.innerHTML = '<p>No se encontraron resultados.</p>';
            return;
        }

        data.forEach(anime => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <img src="${anime.poster}" alt="${anime.title}">
                <div class="title">${anime.title}</div>
            `;
            card.onclick = () => loadAnime(anime.slug);
            resultsSection.appendChild(card);
        });
    } catch (e) {
        resultsSection.innerHTML = '<p>Error al buscar.</p>';
    }
}

async function loadAnime(slug) {
    animeDetail.innerHTML = '<p>Cargando detalles...</p>';
    showDetail();

    try {
        const res = await fetch(`${API_URL}/anime/${slug}`);
        currentAnime = await res.json();
        currentAnime.slug = slug;

        animeDetail.innerHTML = `
            <button class="back-btn" onclick="goBack()">← Volver</button>
            <div class="detail-header">
                <img src="${currentAnime.poster || ''}" alt="Poster">
                <div class="info">
                    <h2>${currentAnime.title}</h2>
                    <p>${currentAnime.synopsis}</p>
                </div>
            </div>
            <h3>Lista de Episodios</h3>
            <div class="episode-list-container">
                ${currentAnime.episodes.map(ep => {
            const thumbUrl = currentAnime.anime_id
                ? `https://cdn.animeflv.net/screenshots/${currentAnime.anime_id}/${ep.number}/th_3.jpg`
                : '';
            return `
                    <div class="episode-item" onclick="playEpisode('${slug}', ${ep.number})">
                        <div class="ep-thumb">
                            <img src="${thumbUrl}" alt="Ep ${ep.number}" onerror="this.src='https://via.placeholder.com/150x85?text=Ep+${ep.number}'">
                            <div class="play-overlay">▶</div>
                        </div>
                        <div class="ep-info">
                            <div class="ep-title">${currentAnime.title}</div>
                            <div class="ep-number">Episodio ${ep.number}</div>
                        </div>
                    </div>
                `}).join('')}
            </div>
        `;
    } catch (e) {
        animeDetail.innerHTML = '<p>Error al cargar el anime.</p>';
    }
}

async function playEpisode(slug, num) {
    showPlayer();
    document.getElementById('playingTitle').innerText = (currentAnime ? currentAnime.title : slug) + ` - Episodio ${num}`;

    const shield = document.getElementById('clickShield');
    shield.classList.remove('hidden');
    shield.onclick = () => {
        shield.classList.add('hidden');
    };

    try {
        const res = await fetch(`${API_URL}/episode/${slug}/${num}`);
        const data = await res.json();

        const select = document.getElementById('serverSelect');
        select.innerHTML = '';

        data.servers.forEach(srv => {
            const opt = document.createElement('option');
            opt.value = srv.url;
            opt.innerText = srv.title;
            select.appendChild(opt);
        });

        select.onchange = () => {
            document.getElementById('videoPlayer').src = select.value;
        };

        if (data.servers.length > 0) {
            document.getElementById('videoPlayer').src = data.servers[0].url;
        }
    } catch (e) {
        alert('Error al obtener servidores');
    }
}

function goBack() {
    if (searchInput.value || genreSelect.value || yearSelect.value) {
        showResults();
    } else {
        showDashboard();
    }
}

async function handleCast() {
    try {
        const videoSrc = document.getElementById('videoPlayer').src;
        if (!videoSrc) {
            alert("No hay un video cargando para transmitir.");
            return;
        }

        // Import Native Share if available (Android/iOS only)
        if (window.Capacitor && window.Capacitor.Plugins.Share) {
            await window.Capacitor.Plugins.Share.share({
                title: 'Transmitir Anime',
                text: 'Reproduciendo: ' + document.getElementById('playingTitle').innerText,
                url: videoSrc,
                dialogTitle: 'Compartir/Transmitir a Xbox/TV',
            });
        } else {
            // Fallback for browser
            await navigator.share({
                title: 'Transmitir Anime',
                text: 'Reproduciendo: ' + document.getElementById('playingTitle').innerText,
                url: videoSrc
            });
        }
    } catch (e) {
        if (e.name !== 'AbortError') {
            console.error("Error al compartir", e);
            alert("Para transmitir, abre esta opción en el menú de compartir de tu tablet.");
        }
    }
}

function showDashboard() {
    dashboard.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    animeDetail.classList.add('hidden');
    playerSection.classList.add('hidden');
}

function showResults() {
    dashboard.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    animeDetail.classList.add('hidden');
    playerSection.classList.add('hidden');
}

function showDetail() {
    dashboard.classList.add('hidden');
    resultsSection.classList.add('hidden');
    animeDetail.classList.remove('hidden');
    playerSection.classList.add('hidden');
}

function showPlayer() {
    dashboard.classList.add('hidden');
    resultsSection.classList.add('hidden');
    animeDetail.classList.add('hidden');
    playerSection.classList.remove('hidden');
}
