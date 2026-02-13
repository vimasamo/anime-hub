from scraper import AnimeFLV
import json

def test_scraper():
    flv = AnimeFLV()
    
    print("--- Testing Search (One Piece) ---")
    results = flv.search("One Piece")
    print(f"Found {len(results)} results")
    if results:
        print(f"First result: {results[0]['title']} ({results[0]['slug']})")
        
        anime_slug = results[0]['slug']
        print(f"\n--- Testing Info ({anime_slug}) ---")
        info = flv.get_anime_info(anime_slug)
        print(f"Title: {info['title']}")
        print(f"Episodes: {len(info['episodes'])}")
        
        if info['episodes']:
            ep_num = info['episodes'][0]['number']
            print(f"\n--- Testing Videos (Episode {ep_num}) ---")
            videos = flv.get_episode_videos(anime_slug, ep_num)
            print(f"Found {len(videos)} servers")
            for v in videos:
                print(f"- {v['server']}: {v['url']}")

if __name__ == "__main__":
    test_scraper()
