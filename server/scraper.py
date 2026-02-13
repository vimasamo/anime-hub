import cloudscraper
from bs4 import BeautifulSoup
import json
import re

class AnimeFLV:
    def __init__(self):
        self.base_url = "https://www3.animeflv.net"
        self.scraper = cloudscraper.create_scraper()

    def get_latest_episodes(self):
        url = self.base_url
        response = self.scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        episodes = []
        # Latest episodes are usually in ul.ListEpisodios
        for li in soup.select('ul.ListEpisodios li'):
            title = li.select_one('strong.Title').text
            episode_text = li.select_one('span.Capi').text
            # Link looks like /ver/slug-number
            href = li.select_one('a')['href']
            slug_num = href.split('/')[-1]
            # Split slug and number
            match = re.search(r'^(.*)-(\d+)$', slug_num)
            slug = match.group(1) if match else slug_num
            number = match.group(2) if match else "0"
            
            poster = li.select_one('span.Image img')
            poster_url = poster.get('src') or poster.get('data-cfsrc') or ""
            if poster_url.startswith('/'):
                poster_url = self.base_url + poster_url

            episodes.append({
                "title": title,
                "slug": slug,
                "episode": number,
                "poster": poster_url
            })
        return episodes

    def get_on_air(self):
        url = self.base_url
        response = self.scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get on-air anime from sidebar
        on_air = []
        sidebar_items = soup.select('ul.ListSdbr li')
        
        for i, li in enumerate(sidebar_items):
            a = li.select_one('a')
            if not a: continue
            
            title = a.text.strip()
            type_span = a.select_one('span.Type')
            if type_span:
                title = title.replace(type_span.text, "").strip()
                type_name = type_span.text
            else:
                type_name = "Anime"
                
            slug = a['href'].split('/')[-1]
            poster = None
            
            # For the first 10 items, fetch the anime page to get the actual poster
            # This balances performance with having some images
            if i < 10:
                try:
                    anime_url = f"{self.base_url}/anime/{slug}"
                    anime_response = self.scraper.get(anime_url)
                    anime_soup = BeautifulSoup(anime_response.text, 'html.parser')
                    poster_el = anime_soup.select_one('div.AnimeCover img')
                    if poster_el:
                        poster_src = poster_el.get('src')
                        if poster_src:
                            if poster_src.startswith('/'):
                                poster = self.base_url + poster_src
                            else:
                                poster = poster_src
                except Exception as e:
                    print(f"Error fetching poster for {slug}: {e}")
            
            on_air.append({
                "title": title,
                "slug": slug,
                "type": type_name,
                "poster": poster
            })
        
        return on_air

    def search(self, query=None, genre=None, year=None, page=1):
        url = f"{self.base_url}/browse?"
        if query:
            url += f"q={query}&"
        if genre:
            url += f"genre[]={genre}&"
        if year:
            url += f"year[]={year}&"
        if page > 1:
            url += f"page={page}"
            
        response = self.scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for article in soup.select('ul.ListAnimes li article'):
            title_el = article.select_one('h3.Title')
            if not title_el: continue
            title = title_el.text
            href = article.select_one('a')['href']
            slug = href.split('/')[-1]
            poster_el = article.select_one('img')
            poster = poster_el.get('src') or poster_el.get('data-cfsrc') or ""
            
            if poster.startswith('/'):
                poster = self.base_url + poster
                
            results.append({
                "title": title,
                "slug": slug,
                "poster": poster
            })
        return results

    def get_genres(self):
        # Static list based on research
        return [
            "Acción", "Artes Marciales", "Aventuras", "Ciencia Ficción", "Comedia", 
            "Demencia", "Demonios", "Deportes", "Drama", "Ecchi", "Escolares", 
            "Fantasía", "Harem", "Histórico", "Josei", "Juegos", "Magia", "Mecha", 
            "Militar", "Misterio", "Música", "Parodia", "Policía", "Psicológico", 
            "Romance", "Samurái", "Sci-Fi", "Seinen", "Shoujo", "Shounen", 
            "Slice of Life", "Sobrenatural", "Space", "Superpoderes", "Suspenso", 
            "Terror", "Vampiros", "Yaoi", "Yuri"
        ]
    def get_anime_info(self, slug):
        url = f"{self.base_url}/anime/{slug}"
        response = self.scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Details
        title_el = soup.select_one('h1.Title')
        title = title_el.text if title_el else "Unknown"
        
        synopsis_el = soup.select_one('div.Description')
        synopsis = synopsis_el.text if synopsis_el else ""
        
        poster_el = soup.select_one('div.AnimeCover img')
        poster = poster_el['src'] if poster_el else ""
        if poster.startswith('/'):
            poster = self.base_url + poster
            
        # Extract anime ID from poster URL (e.g., .../covers/7.jpg)
        anime_id = None
        match_id = re.search(r'/covers/(\d+)\.jpg', poster)
        if match_id:
            anime_id = match_id.group(1)
        
        # Episode extraction from JS variable
        scripts = soup.select('script')
        episodes = []
        for script in scripts:
            if 'var episodes =' in script.text:
                ep_data = re.search(r'var episodes = (\[\[.*?\]\]);', script.text)
                if ep_data:
                    raw_episodes = json.loads(ep_data.group(1))
                    for ep in raw_episodes:
                        episodes.append({
                            "number": ep[0],
                            "id": ep[1]
                        })
                break
        
        return {
            "anime_id": anime_id,
            "title": title,
            "synopsis": synopsis,
            "poster": poster,
            "episodes": episodes
        }

    def get_episode_videos(self, anime_slug, episode_number):
        url = f"{self.base_url}/ver/{anime_slug}-{episode_number}"
        response = self.scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        scripts = soup.select('script')
        servers = []
        for script in scripts:
            if 'var videos =' in script.text:
                video_data = re.search(r'var videos = (\{.*?\});', script.text)
                if video_data:
                    raw_videos = json.loads(video_data.group(1))
                    if "SUB" in raw_videos:
                        for srv in raw_videos["SUB"]:
                            servers.append({
                                "server": srv["server"],
                                "title": srv["title"],
                                "url": srv["code"]
                            })
                break
        return servers
