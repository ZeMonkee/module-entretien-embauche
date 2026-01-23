import asyncio
import edge_tts

async def main():
    print("Recherche des voix françaises disponibles...")
    voices = await edge_tts.list_voices()

    # On filtre pour ne garder que le français (fr)
    french_voices = [v for v in voices if "fr-" in v["ShortName"]]

    for v in french_voices:
        print(f"Nom: {v['ShortName']} | Genre: {v['Gender']}")

if __name__ == "__main__":
    asyncio.run(main())
